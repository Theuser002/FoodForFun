import os
import warnings
from datetime import datetime

# Flask Imports
from flask import Flask, flash, request, redirect, url_for, send_from_directory, render_template
from flask_cors import CORS
from werkzeug.utils import secure_filename

# General config
warnings.filterwarnings("ignore")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_FOLDER = os.path.join(BASE_DIR, 'template')
IMAGES_FOLDER = os.path.join(TEMPLATE_FOLDER, 'images')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'gif'}

# Flask config
HOST = '0.0.0.0'
PORT = 4321
DEBUG = True
app = Flask(__name__)
app.config['IMAGES_FOLDER'] = IMAGES_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024
CORS(app)

# Main
if __name__ == '__main__':
	app.run(host=HOST, port=PORT, debug=DEBUG)