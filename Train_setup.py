import numpy as np
from keras.models import Sequential
from keras.layers import Dense
import sklearn.preprocessing
import json
import numpy as np


zones = 0
input_data = []
with open('ROUND_1.txt', 'r') as file:
  line = file.readline()
  while(line):
    if(line.find("{") != -1):
      line = line.replace('\'', '\"')
      l1 = list(json.loads(line[line.find('{'):]).values())
      l1.append(zones)
      zones = (zones + 1)%6
      input_data.append(l1)
    line = file.readline()
input_data = np.array(input_data)
# print((input_data))

# Generate some random data for demonstration purposes
np.random.seed(42)
num_samples = 2
label = input_data[:,-1]
# print(label)
input_data = input_data[:, :4] # 4 input features
# print(input_data)
label_binarizer = sklearn.preprocessing.LabelBinarizer()
label_binarizer.fit(range(6))
encoded_arr = label_binarizer.transform(label)

labels = np.random.randint(6, size=(num_samples,))  # 6 classes

# Convert labels to one-hot encoding
labels_one_hot = encoded_arr
print(encoded_arr)

# Build the neural network model
model = Sequential()
model.add(Dense(8, input_dim=4, activation='relu'))
model.add(Dense(6, activation='softmax'))

# Compile the model
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Train the model
model.fit(input_data, labels_one_hot, epochs=1000, batch_size=1)
model.save('BLE.keras')

# You can now use the trained model to make predictions on new data
# For example:
# new_data = np.random.rand(5, 4)  # 5 new samples
# predictions = model.predict(new_data)
# print("Predictions:\n", predictions)
