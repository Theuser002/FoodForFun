# IT4342E - Computer Vision Project
## Contributor

| NAME                | STUDENT ID | ROLE                                  |
| ------------------- | ---------- | ------------------------------------- |
| Nguyen Thi Hong Anh | 20176679   | Back-end                              |
| Nguyen Viet Hoang   | 20176762   | Gaussian Noise, Report, Documentation |
| Tran Phi Hung       | 20176774   | MobileNet, Xception                   |
| Nguyen Tri Hung     | 20176773   | MobileNet, Xception, Autoencoder      |
| Nguyen Manh Phuc    | 20176845   | Front-end, Salt and Pepper Noise      |



## Project description

Vietnamese Food Recoginition is a website that helps people from all over the world classify the type of food from their input image. 

To build this project, we use Flask micro-framework.

This project follows the below structure:

```
    .
    ├── foodforfun						    		# Include model files, const
    │   ├── const         
    │	│   │── dictionary.py			            # Label index and description
    │   └── models      
    │	   	│── autoencoder				            # Autoencoder model weights
    │	   	│	│── best_state.pth		            
    │	   	│── mobilenet				            # MobileNet model weights
    │	   	│	│── best-model
    │	   	│		│── best_model.h5		        
    │	   	│── xception			                # Xception model weights
    │	   	│	│── best-model
    │	   	│		│── best_model.h5	
    │	   	│── autoencoder.py		                # Autoencoder model for Noise reduction
    │	   	│── mobilenet.py		                # MobileNet model for Classification
    │	   	│── xception.py			                # Xception model for Noise reduction
    ├── static                    	                # Images, CSS, Javascript
    │	   	│── css					                # CSS files
    │	   	│── js					                # JavaScript files
    │	   	│── uploads				                # Folder to save images from user
    ├── templates                                   # HTML template
    │	   	│── index.html			                # Home page
    │	   	│── result.html			                # Result page
    ├── deploy.sh                                   # Script to run the project
    ├── Dockerfile                                  # Script to build Docker image
    ├── README.md           
    ├── requirements.txt			                # Installation requirements
    └── server.py					                # Server configuration and API definition
```



For the server configuration, we need to specify Flask configurations and API endpoints :

* Flask config:

```python
HOST = '0.0.0.0'
PORT = 4321
DEBUG = True
app = Flask(__name__)
app.secret_key = 'foodforfun'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['IMAGES_FOLDER'] = IMAGES_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024
```



* API:

```python
@app.route('/predict', methods=['POST'])
def predict():
	return render_template('result.html', image, prediction, accuracy)
	
@app.route('/', methods=['GET'])
def upload_file():
    return render_template('index.html')

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
```



The predict API will apply Autoencoder model for image cleaning if user demands, and one model between MobileNet and Xception for image prediction based on user's choice:

* Autoencoder:

```python
class Autoencoder (nn.Module):
    def __init__(self):
        super(Autoencoder, self).__init__()
        self.encoder = nn.Sequential(...)
        self.decoder = nn.Sequential(...)

    def forward(self, x):
        x = self.encoder(x)
        x = self.decoder(x)
        x = torch.sigmoid(x)
        return x
```



* Mobilenet:

```python
class MobileNet:
    def __init__(self):
        self.CUR_DIR = os.path.dirname(os.path.abspath(__file__))
        self.MODEL_PATH = os.path.join(self.CUR_DIR, "mobilenet/best-model/comb_best_model.h5")
        self.model = load_model(self.MODEL_PATH)

    def predict(self, image_path):
        return result, accuracy
```



* Xception:

```python
class Xception:
    def __init__(self):
        self.CUR_DIR = os.path.dirname(os.path.abspath(__file__))
        self.MODEL_PATH = os.path.join(self.CUR_DIR, "xception/best-model/best_model.h5")
        self.model = load_model(self.MODEL_PATH)
    def predict:
        return result, accuracy
```



## Installation Guide

### Requirements:

* Docker: 20.10.11

### Installation

* Git clone the project : `git clone https://github.com/Theuser002/FoodForFun.git`

* Move to the repository: `cd FoodForFun`

* Run `bash -x ./deploy.sh <version> <port>` 

  Where: 

  * `version`: Tag number for the image you want to build

  * `port`: Bind port


Follow this link to access the website: 0.0.0.0:4321



