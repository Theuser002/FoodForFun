import tensorflow as tf
import tensorflow.keras
import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import sklearn

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

IMAGE_SHAPE = (300, 300)
N_CHANNELS = 3

n_classes = 22

class Xception_2():
    
    def __init__(self):
        # Load the pre-trained model
        self.pretrained_nn = Xception(input_shape = (IMAGE_SHAPE[0], IMAGE_SHAPE[1], N_CHANNELS), weights = 'imagenet', include_top=False) # [1] 
        # Define network architecture
        self.feature_logits = Flatten()(self.pretrained_nn.output)
        self.last_output = self.pretrained_nn.output
        x = GlobalAveragePooling2D()(self.last_output)
        x = Dense(512, activation='relu')(x)
        x = Dropout(0.2)(x)
        self.outputs = Dense(n_classes, activation='softmax')(x)
        self.model = Model(inputs=self.pretrained_nn.input, outputs=self.outputs)

        self.model = self.model.compile(
                        loss = 'categorical_crossentropy',
                        optimizer = 'rmsprop',
                        metrics = ['accuracy']
                    )

    def get_model(self):
        return self.model