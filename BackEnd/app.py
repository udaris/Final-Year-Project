from flask import Flask,render_template, request,redirect,flash
from werkzeug.utils import secure_filename
from main import getPrediction, getPlantDetails
import os
from main2 import getPrediction2
from main3 import getPrediction_03
from main4 import prediction_03

UPLOAD_FOLDER='static/images'

app=Flask(__name__, static_folder="static")

app.secret_key="secret key"

app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER


@app.route('/plant')
def index():
    return render_template('index.html')


@app.route('/largeplant', methods=['POST'])
def submit_file_large_leaves_module():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file=request.files['file']
        if file.filename=='':
            flash('No file selected for uploading')
            return redirect(request.url)
        if file:
            filename=secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            label=getPrediction(filename)
            flash(label)   
            full_filename=os.path.join(app.config['UPLOAD_FOLDER'], filename)
            flash(full_filename)
            plant_details = getPlantDetails( label)
            if plant_details:
                flash(f"Good for: {plant_details['Treatment For']}")
                flash(f"Parts Used in Treatment: {plant_details['Parts Used in Treatment']}")
            else:
                print("Plant details not found.")
            return redirect('/plant')
        
@app.route('/smallLeaves', methods=['POST'])
def submit_file_flower_module():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file=request.files['file']
        if file.filename=='':
            flash('No file selected for uploading')
            return redirect(request.url)
        if file:
            filename=secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            label=getPrediction_03(filename)
            
            flash(label)   
            full_filename=os.path.join(app.config['UPLOAD_FOLDER'], filename)
            flash(full_filename)
            plant_details = getPlantDetails( label)
            if plant_details:
                flash(f"Good for: {plant_details['Treatment For']}")
                flash(f"Parts Used in Treatment: {plant_details['Parts Used in Treatment']}")
            else:
                print("Plant details not found.")
            return redirect('/plant')

@app.route('/flowers', methods=['POST'])
def submit_file_small_leaves_module():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file=request.files['file']
        if file.filename=='':
            flash('No file selected for uploading')
            return redirect(request.url)
        if file:
            filename=secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            label=getPrediction2(filename)
            #label = label.tolist()  # Convert ndarray to list
            flash(label)   
            full_filename=os.path.join(app.config['UPLOAD_FOLDER'], filename)
            flash(full_filename)
            plant_details = getPlantDetails( label)
            if plant_details:
                flash(f"Good for: {plant_details['Treatment For']}")
                flash(f"Parts Used in Treatment: {plant_details['Parts Used in Treatment']}")
            else:
                print("Plant details not found.")
            return redirect('/plant')
        
@app.route('/details.html')
def details():
    return render_template('details.html')
        
if __name__=="__main__":
    app.run()

