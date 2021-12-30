import os
import cv2
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
from tensorflow import keras
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping
from tensorflow.keras.models import Model, load_model
from sklearn.utils import class_weight
from tqdm import tqdm
from collections import Counter
from math import ceil
from tensorflow.keras.optimizers import Adam, SGD
import requests

CUR_DIR = os.getcwd()
MODEL_PATH = os.path.join(CUR_DIR, "xception/fine-tune")
model = load_model(MODEL_PATH)

def prepareImage(image):
  image = cv2.resize(image, (300, 300))
  image = image/255.
  image = np.expand_dims(image, axis = 0)
  return image

URL = "https://cdn.beptruong.edu.vn/wp-content/uploads/2018/05/bo-nuong-la-lot.jpg"
online_image = requests.get(URL).content
with open('image.jpg', 'wb') as handler:
  handler.write(online_image)

online_image = cv2.imread('image.jpg')
online_image = cv2.cvtColor(online_image, cv2.COLOR_BGR2RGB)
plt.imshow(online_image)
online_image = prepareImage(online_image)

prediction = model.predict(online_image)
result = np.argmax(prediction)
print(result, prediction[0][result])
