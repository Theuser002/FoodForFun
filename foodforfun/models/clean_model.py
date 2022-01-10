import os

class CleanModel:
    def __init__(self):
        self.CUR_DIR = os.path.dirname(os.path.abspath(__file__))
        # self.MODEL_PATH = os.path.join(self.CUR_DIR, "xception/best-model/best_model.h5")
        # self.model = load_model(self.MODEL_PATH)
