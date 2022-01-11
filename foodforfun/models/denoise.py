import os
import torch
import cv2


from foodforfun.models.autoencoder import Autoencoder

device = "cuda" if torch.cuda.is_available() else "cpu"

CUR_DIR = os.path.dirname(os.path.abspath(__file__))
BEST_STATE_PATH = os.path.join(CUR_DIR, "encoder/best_state.pth")
IMG_PATH = os.path.join(CUR_DIR, "encoder/31_s&p.png")
autoencoder = Autoencoder()
autoencoder.load_state_dict(torch.load(BEST_STATE_PATH))


autoencoder = autoencoder.to(device)
cv2.imread(IMG_PATH)

