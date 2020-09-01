from flask import Flask
from flask import request

from radio_feature_extraction_app import extract_radiomic_feature
from predict_recurrence import predict_recurrence
from werkzeug import secure_filename
from tifffile import imread, imsave
import numpy as np

app = Flask(__name__)

def check_extension(file_name):
    return '.' in file_name and file_name.split('.', 1)[1] in ['tif', 'tiff']
     
@app.route('/api/predict', methods = ['POST', 'GET'])
def get_data_and_return_prob():

    clinic_features = []
    if request.method == 'POST':
        clinic_features.append(request.form['ad'])
        clinic_features.append(request.form['sc'])
        clinic_features.append(request.form['age'])
        clinic_features.append(request.form['t1'])
        clinic_features.append(request.form['t2'])
        clinic_features.append(request.form['t3'])
        clinic_features.append(request.form['r0'])
        clinic_features.append(request.form['r1'])
        clinic_features.append(request.form['n0'])
        clinic_features.append(request.form['n1'])
        clinic_features.append(request.form['n2'])
        clinic_features.append(request.form['nlr'])
        clinic_features.append(request.form['pnr'])
        clinic_features.append(request.form['hg'])
        clinic_features.append(request.form['alt'])
        clinic_features.append(request.form['pleural+'])
        clinic_features.append(request.form['pleural-'])
        clinic_features.append(request.form['lymphovascular+'])
        clinic_features.append(request.form['lymphovascular-'])
        clinic_features.append(request.form['lymph_node'])
        
        # 
        img_file = request.files['img_file']
        label_file = request.files['label_file']
        if img_file and label_file:
            img = imread(img_file)
            label = imread(label_file)
            
        # extract features 
        radiomic_features = extract_radiomic_feature(img, label)        
        features = radiomic_features + clinic_features

        # predict
        prob = predict_recurrence((np.asarray(features)).reshape(1, -1))
        return prob

        
if __name__=='__main__':
    app.run(debug=True)
    
