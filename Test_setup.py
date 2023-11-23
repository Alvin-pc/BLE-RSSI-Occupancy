import asyncio
from bleak import BleakScanner
import keras
import json
import numpy as np
np.set_printoptions(precision=1, suppress=True)
import random
import time

from paho.mqtt import client as mqtt_client

broker = 'broker.emqx.io'
port = 1883
# topic = "DESE,Zone0,confidence"
topics = ['dese/zone0', 'dese/zone1', 'dese/zone2', 'dese/zone3', 'dese/zone4', 'dese/zone5','dese/zoneconfident']
msgs = ['95%', '1%', '5%', '1%', '1%', '1%', '0']
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 1000)}'
username = 'Emqx'
password = 'password'

beacons = ["BlueCharm_BB0F", "BlueCharm_BB59", "Pixel 6a", "Mi 11X"]
lists = {"BlueCharm_BB0F": [], "BlueCharm_BB59": [], "Pixel 6a": [], "Mi 11X": []}
input_data=[]

BLE_model = keras.models.load_model("BLE_Windows.keras")


def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id,clean_session=True)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def publish(client): 
    # msg_count = 0
    # while True:
    global input_data, lists, beacons, msgs
    time.sleep(1)
    for topic, msg in zip(topics, msgs):
        result = client.publish(topic, msg)
        print('msg :', msg)
        status = result[0]
        if status == 0:
            print(f"Send message {msg} to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")




async def run_bleak(stop_event, client):
    def callback(device, advertising_data, client):
        global input_data, lists, beacons, msgs
        # print(device.name)
        if device.name in beacons:
            lists[device.name].append(advertising_data.rssi)
            if all(len(lists[beacon]) > 5 for beacon in beacons):
                mean_values = {key: sum(value) / len(value) for key, value in lists.items()}
                input_data.append([mean_values[beacon] for beacon in beacons])
                predictions = BLE_model.predict(input_data)[0]
                print(predictions)
                for i,prediction in enumerate(predictions):
                    msgs[i]= f'{str(np.round(prediction*100, decimals=2))}%'
                    # print("Predictions:\n", prediction)
                msgs[-1] = str(np.argmax(predictions))
                input_data.clear()
                for beacon in beacons:
                    lists[beacon].clear()
                publish(client)

            

    def inner_callback(device, advertising_data):
        callback(device, advertising_data, client)    

    async with BleakScanner(inner_callback) as scanner:
        await stop_event.wait()

async def main():
    client = connect_mqtt()
    client.loop_start()
    stop_event = asyncio.Event()
    asyncio.create_task(run_bleak(stop_event, client))
    await stop_event.wait()    
    

if __name__ == "__main__":
    asyncio.run(main())
