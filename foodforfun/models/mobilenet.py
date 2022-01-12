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
from math import ceil

class MobileNet:
    def __init__(self):
        self.CUR_DIR = os.path.dirname(os.path.abspath(__file__))
        self.MODEL_PATH = os.path.join(self.CUR_DIR, "mobilenet/best-model/best_model.h5")
        self.model = load_model(self.MODEL_PATH)
    
    def prepareImage(self, image):
        image = cv2.resize(image, (300, 300))
        image = image/255.
        image = np.expand_dims(image, axis = 0)
        return image

    def predict(self, image_path):
        # with open('image.jpg', 'wb') as handler:
        #     handler.write(image)
        online_image = cv2.imread(image_path)
        online_image = cv2.cvtColor(online_image, cv2.COLOR_BGR2RGB)
        plt.imshow(online_image)
        online_image = self.prepareImage(online_image)
        prediction = self.model.predict(online_image)
        result = np.argmax(prediction)
        accuracy = prediction[0][result]

        return result, accuracy