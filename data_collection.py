import asyncio
import pandas as pd
from bleak import BleakScanner
import time

name = 'Sample'
beacons = ["BlueCharm_BB0F", "BlueCharm_BB59", "Pixel 6a", "Mi 11X"]
lists = {"BlueCharm_BB0F": [], "Pixel 6a": [], "BlueCharm_BB59": [], "Mi 11X": []}
beacon_used = beacons[0:4]
selected_lists = {beacon: [] for beacon in beacon_used}

async def main():
    stop_event = asyncio.Event()

    def callback(device, advertising_data):
        if device.name in beacon_used:
            selected_lists[device.name].append(advertising_data.rssi)

            # Check if any list has grown beyond 100 values
            if all(len(selected_lists[beacon]) > 50 for beacon in beacon_used):
                # print(selected_lists)
                # Calculate the mean of all lists
                mean_values = {
                    key: sum(value) / len(value) for key, value in selected_lists.items()
                }
                print("Mean RSSI values:", mean_values)
                time.sleep(3)
                for beacon in beacon_used:
                    selected_lists[beacon].clear()

    async with BleakScanner(callback) as scanner:
        await stop_event.wait()


asyncio.run(main())



 # with open('0F_D.csv', 'a') as the_file:
            #     the_file.write(device.name + ',' +str(device.rssi)+ '\n')