from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
from main import getPrediction, getPlantDetails

UPLOAD_FOLDER = 'static/images'

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}

app = Flask(__name__, static_folder="static")
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Function to check if the file has an allowed extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Route to handle the image upload
@app.route('/plant', methods=['POST'])
def submit_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        predicted_class = getPrediction(filename)
        plant_details = getPlantDetails(predicted_class)

        if plant_details:
            return jsonify({
                'predicted_class': predicted_class,
                'plant_details': plant_details
            })
        else:
            return jsonify({'error': 'Plant details not found'})

    return jsonify({'error': 'Invalid file'})

if __name__ == "__main__":
    app.run()
