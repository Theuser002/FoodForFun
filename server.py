import os
import warnings
import requests
import numpy as np
import cv2

from datetime import datetime
from foodforfun.const.dictionary import dictionary

# Flask Imports
from flask import Flask, flash, request, redirect, url_for, send_from_directory, render_template
from flask_cors import CORS
# from werkzeug.utils import secure_filename

# Model imports 
from foodforfun.models.xception import Xception
from foodforfun.models.mobilenet import MobileNet
from foodforfun.models.denoise import Denoise
from foodforfun.const.count import Count

# General config
warnings.filterwarnings("ignore")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_FOLDER = os.path.join(BASE_DIR, 'templates')
IMAGES_FOLDER = os.path.join(TEMPLATE_FOLDER, 'images')
STATIC_FOLDER = os.path.join(BASE_DIR, 'static')
UPLOAD_FOLDER = os.path.join(STATIC_FOLDER, 'uploads')
CSS_FOLDER = os.path.join(STATIC_FOLDER, 'css')
JS_FOLDER = os.path.join(STATIC_FOLDER, 'js')
OUTPUT_FOLDER = os.path.join(STATIC_FOLDER, 'outputs')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Flask config
HOST = '0.0.0.0'
PORT = 4321
DEBUG = True
app = Flask(__name__)
app.secret_key = 'foodforfun'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['IMAGES_FOLDER'] = IMAGES_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024
CORS(app)

# Model config
xception = Xception()
mobilenet = MobileNet()
autoencoder = Denoise()
count = Count()

# API
@app.route('/predict', methods=['POST'])
def predict():

    print('predict')
    if 'file' not in request.files:
        print('No file part')
        return redirect('/')

    # for file
    file = request.files["file"]
    # for drop and url: image url
    image_url = request.form.get('imageURL')
    # for denoise image
    isDenoise = request.form.get('denoise')
    chosen_model = request.form.get('model')
    # isDenoise = request.form['denoiseCheckbox']
    print("Denoise:\n-- ")
    print(isDenoise)
    
    # if user does not select file, browser also submit an empty part without filename
    

    # if image_url not null
    if image_url != '' and file.filename == '' :
        file = requests.get(image_url)
        if file.status_code == 200:
            
            cnt = count.increment_count()
            image_name = "online_image" + str(cnt) + ".jpg"
            filepath = os.path.join(UPLOAD_FOLDER, image_name)
            if os.path.isfile(filepath):
                os.remove(filepath)
            with open(filepath, 'wb') as handler:
                img = file.content
                handler.write(img)
                
            if isDenoise == 'true':
                img = cv2.imread(filepath)
                # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                clean_img = autoencoder.clean_image(img)
                # clean_img = cv2.cvtColor(clean_img, cv2.COLOR_BGR2RGB)
                cnt_cln = count.increment_count_clean()
                clean_filename = "cleaned_image" + str(cnt_cln) + ".jpg"
                clean_filepath = os.path.join(UPLOAD_FOLDER, clean_filename)
                cv2.imwrite(clean_filepath, clean_img)
                filepath = clean_filepath
                image_name = clean_filename

            result = "1"
            accuracy = 0
            if chosen_model == 'Xception':
                result, accuracy = xception.predict(filepath)
            elif chosen_model == 'MobileNetV2': 
                result, accuracy = mobilenet.predict(filepath)

            input_url = url_for('uploaded_file', filename=image_name)
            # return render_template('result.html', image=input_url, prediction=dictionary[result])
            return render_template('result.html', image=input_url, prediction=dictionary[result], accuracy=str(round(accuracy*100, 2)))

    # Save and predict image
    if file and allowed_file(file.filename):
        # Save uploaded file
        print("Save uploaded file")

        filepath = os.path.join(UPLOAD_FOLDER, file.filename)  
        file.save(filepath)
        if isDenoise == 'true':
            cnt_cln = count.increment_count_clean()
            img = cv2.imread(filepath)
            # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            clean_img = autoencoder.clean_image(img)
            # clean_img = cv2.cvtColor(clean_img, cv2.COLOR_BGR2RGB)

            clean_filename = "cleaned_image" + str(cnt_cln) + ".jpg"
            clean_filepath = os.path.join(UPLOAD_FOLDER, clean_filename)
            # with open(clean_filepath, 'wb') as handler:
            #     handler.write(clean_img)
            cv2.imwrite(clean_filepath, clean_img)
            file.filename = clean_filename
            filepath = clean_filepath
		# Predict
        result = "1"
        accuracy = 0
        if chosen_model == 'Xception':
            result, accuracy = xception.predict(filepath)
        elif chosen_model == 'MobileNetV2': 
            result, accuracy = mobilenet.predict(filepath)
        input_url = url_for('uploaded_file', filename=file.filename)
        # return render_template('result.html', image=input_url, prediction=dictionary[result])
        return render_template('result.html', image=input_url, prediction=dictionary[result], accuracy=str(round(accuracy*100, 2)))

    if file.filename == '' and image_url == '':
        print('No selected file')
        render_template('index.html')

    flash('Invalid')
    return redirect('/')


@app.route('/', methods=['GET'])
def upload_file():
    return render_template('index.html')


@app.route('/results', methods=['GET'])
def show_results():
    return render_template('result.html')

@app.route('/test', methods=['GET'])
def test():
    return render_template('test.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


@app.route('/outputs/<filename>')
def generated_file(filename):
    return send_from_directory(OUTPUT_FOLDER, filename)


@app.route('/css/<filename>')
def css_file(filename):
    return send_from_directory(CSS_FOLDER, filename)

@app.route('/js/<filename>')
def js_file(filename):
    return send_from_directory(JS_FOLDER, filename)

@app.route('/images/<filename>')
def image_file(filename):
    return send_from_directory(STATIC_FOLDER + "/images", filename)

# ------------------ Helper functions --------------------- #

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



# Main
if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug=DEBUG)