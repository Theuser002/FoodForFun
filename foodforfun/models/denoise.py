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

# device = "cuda" if torch.cuda.is_available() else "cpu"
device = "cpu"
map_location = torch.device(device)
CUR_DIR = os.path.dirname(os.path.abspath(__file__))
BEST_STATE_PATH = os.path.join(CUR_DIR, "autoencoder/best_state.pth")
IMG_PATH = os.path.join(CUR_DIR, "encoder/31_s&p.png")
IMAGE_SHAPE = (300, 300)


autoencoder = Autoencoder()
autoencoder.load_state_dict(torch.load(BEST_STATE_PATH, map_location=map_location))


autoencoder = autoencoder.to(device)
cv2.imread(IMG_PATH)

train_transform = A.Compose([
    A.Resize(height = IMAGE_SHAPE[0], width = IMAGE_SHAPE[1]),
    ToTensorV2()
])



def clean (model, noised_img, transform):
    model.eval()
    img_height, img_width, img_channels = noised_img.shape
    
    noised_img = noised_img.astype('float32')/255.
    restore_transform = A.Compose([
        A.Resize(height = img_height, width = img_width)
    ])
    
    # img_dtype = noised_img.dtype 

    img = transform(image=noised_img)['image']
    img = img.to(device)

    torch_noised_img = torch.unsqueeze(img, 0)
    torch_noised_img = torch_noised_img.to(device)

    with torch.no_grad():
        
        output_img = model(torch_noised_img)
    # output_img = restore_transform(image=output_img)['image']
    output_img = output_img.cpu().squeeze().numpy()
    output_img = output_img.transpose(1, 2, 0)
    return output_img

def clean_image(noised_img):
    return clean(model=autoencoder, noised_img=noised_img, transform=train_transform)