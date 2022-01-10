import os
import warnings
from datetime import datetime
from foodforfun.const.dictionary import dictionary

# Flask Imports
from flask import Flask, flash, request, redirect, url_for, send_from_directory, render_template
from flask_cors import CORS
# from werkzeug.utils import secure_filename

# Model imports 
from foodforfun.models.model import Xception

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
model = Xception()

# API
@app.route('/predict', methods=['POST'])
def predict():

    print('predict')
    if 'file' not in request.files:
        print('No file part')
        return redirect('/')

    file = request.files["file"]
    print("Filename: " + file.filename)
    print("Args")
    print(request.args)
    # if user does not select file, browser also submit an empty part without filename
    if file.filename == '':
        print('No selected file')
        file.filename == 'default.jpg'
        # return redirect('/')
        
    if file and allowed_file(file.filename):
        # Save uploaded file
        print("Save uploaded file")

        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)
		# Predict
	    
        result = model.predict(filepath)
        input_url = url_for('uploaded_file', filename=file.filename)
        # return render_template('result.html', image=input_url, prediction=dictionary[result])
        return render_template('result.html', image=input_url, prediction=dictionary[result])

    flash('Invalid')
    return redirect('/')


@app.route('/', methods=['GET'])
def upload_file():
    return render_template('index.html')


@app.route('/results', methods=['GET'])
def show_results():
    return render_template('result.html')

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