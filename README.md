# BLE-RSSI-Occupancy
Use BLE beacons(transmitters) -{4 beacons in our case}, to identify the region or zone-{6 zones in a rectangular space in our case} where the agent(receiver) is located using logistics regression.

Steps:
1.  Run the file 'data_collection.py' to print the Mean RSSI-{100 samples in our case} at a point and annotate manually.
2.  The values are stored in 'ROUND_1.txt' manually (Check file for format).In each Round n, the values of all the zones{6} are stored sequentially. This is how 'Train_setup.py' uses it to generate the 'BLE.Keras' file.
3.  After training is done, in deployment use just the 'Test_setup.py' with the generated 'BLE.Keras' file.

Note: pip packages like Tensorflow, Keras etc needs to be installed on the host agent to process the RSSI values and generate zone.
Note: The Keras model can work accross devices without additional training, but the Keras binaries may not be OS portable. To run on Linux or Mac, retrain the model and you are good to go.
