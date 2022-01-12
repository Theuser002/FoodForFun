import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
import torch
import torch.nn as nn
import torch.optim as optim
import albumentations as A
import matplotlib.pyplot as plt
import torchvision

from skimage.util import random_noise
from torch.utils.data import DataLoader, Dataset
from itertools import repeat
from tqdm import tqdm
from albumentations.pytorch.transforms import ToTensorV2
from sklearn.model_selection import train_test_split
from torch.nn import Linear, ReLU, Sigmoid, Conv2d, ConvTranspose2d, MaxPool2d, BatchNorm2d, MSELoss
from torch.optim import Adam
from foodforfun.models.autoencoder import Autoencoder


class Denoise:
    def __init__(self):
        self.device = "cpu"
        self.map_location = torch.device(self.device)
        self.CUR_DIR = os.path.dirname(os.path.abspath(__file__))
        self.BEST_STATE_PATH = os.path.join(self.CUR_DIR, "autoencoder/best_state.pth")
        self.IMG_PATH = os.path.join(self.CUR_DIR, "encoder/31_s&p.png")
        self.IMAGE_SHAPE = (300, 300)
        self.autoencoder = Autoencoder()
        self.autoencoder.load_state_dict(torch.load(self.BEST_STATE_PATH, map_location=self.map_location))
        self.autoencoder = self.autoencoder.to(self.device)

        self.train_transform = A.Compose([
            A.Resize(height = self.IMAGE_SHAPE[0], width = self.IMAGE_SHAPE[1]),
            ToTensorV2()
        ])

    def clean_image(self, noised_img):
        return self.clean(noised_img=noised_img)
    
    def clean (self, noised_img):
        self.autoencoder.eval()
        img_height, img_width, img_channels = noised_img.shape
    
        noised_img = noised_img.astype('float32')/255.
        print(noised_img.shape)
    
        # restore_transform = A.Compose([
        #     A.Resize(height = img_height, width = img_width)
        # ])
    
        # img_dtype = noised_img.dtype 
        img = self.train_transform(image=noised_img)['image']
        print(img.shape)
        img = img.to(self.device)
        torch_noised_img = torch.unsqueeze(img, 0)
        torch_noised_img = torch_noised_img.to(self.device)
        print(torch_noised_img.shape)
    
        with torch.no_grad():
            output_img = self.autoencoder(torch_noised_img)
    
        # output_img = restore_transform(image=output_img)['image']
        output_img = output_img.cpu().squeeze().numpy()
        print(output_img.shape)
        output_img = output_img.transpose(1, 2, 0)
        print(output_img.shape)
        return (output_img*255.).astype('uint8')