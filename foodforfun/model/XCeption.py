import tensorflow as tf
import tensorflow.keras
import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import sklearn
import requests

from sklearn.preprocessing import OneHotEncoder
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Model, load_model
from tensorflow.keras.applications.efficientnet import EfficientNetB2, EfficientNetB0, preprocess_input
from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input
from tensorflow.keras.applications import Xception
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, Dense, Flatten, Dropout, Activation, BatchNormalization, GlobalMaxPooling2D, GlobalAveragePooling2D
from tensorflow.keras.optimizers import Adam, SGD
from tensorflow.keras.losses import categorical_crossentropy
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping
from sklearn.utils import class_weight
from tqdm import tqdm
from collections import Counter
from math import ceil
from const import dictionary

class Xception:
    CUR_DIR = os.getcwd()
    MODEL_PATH = os.path.join(CUR_DIR, "xception/best-model/best_model.h5")
    model = load_model(MODEL_PATH)

    def prepareImage(image):
        image = cv2.resize(image, (300, 300))
        image = image/255.
        image = np.expand_dims(image, axis = 0)
        return image

    def identify(image):
        with open('image.jpg', 'wb') as handler:
            handler.write(image)
        online_image = cv2.imread('image.jpg')
        online_image = cv2.cvtColor(online_image, cv2.COLOR_BGR2RGB)
        plt.imshow(online_image)
        online_image = prepareImage(online_image)
        prediction = model.predict(online_image)
        result = np.argmax(prediction)
        print(result, prediction[0][result])

        identified_class = dictionary['result']
        return identified_class
