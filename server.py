import os
import warnings
from datetime import datetime
from foodforfun.const import dictionary

# Flask Imports
from flask import Flask, flash, request, redirect, url_for, send_from_directory, render_template
from flask_cors import CORS
# from werkzeug.utils import secure_filename

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
app.config['IMAGES_FOLDER'] = IMAGES_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024
CORS(app)

# Model
# MODEL_PATH = os.path.join(CUR_DIR, "xception/best-model/best_model.h5")
# model = load_model(MODEL_PATH)

# API
@app.route('/predict', methods=['POST'])
def predict():
    print('predict')
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)

    file = request.files['file']

    # if user does not select file, browser also submit an empty part without filename
    if file.filename == '':
        flash('No selected file')
        return redirect('/')

    if file and allowed_file(file.filename):
        # Save uploaded file
        new_name = f'{int(datetime.now().timestamp())}_{model_type}_{file.filename}'
        # filename = secure_filename(new_name)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
		
		# Predict
		# with open(filepath, 'wb') as handler:
  		# 	handler.write(online_image)

		# online_image = cv2.imread(filepath)
		# online_image = cv2.cvtColor(online_image, cv2.COLOR_BGR2RGB)
		# online_image = prepareImage(online_image)
		# prediction = model.predict(online_image)
		# result = np.argmax(prediction)
		# print(result, prediction[0][result])		
        input_url = url_for('uploaded_file', filename=filename)

        return render_template('result.html', image=input_url, prediction=dictionary[result])

    flash('Invalid')
    return redirect('/')


@app.route('/', methods=['GET'])
def upload_file():
    print('index')
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

def prepareImage(image):
  image = cv2.resize(image, (300, 300))
  image = image/255.
  image = np.expand_dims(image, axis = 0)
  return image

# Main
if __name__ == '__main__':
	app.run(host=HOST, port=PORT, debug=DEBUG)