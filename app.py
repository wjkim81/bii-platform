from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
from werkzeug import secure_filename
from werkzeug.exceptions import HTTPException, default_exceptions, _aborter
from tifffile import imread, imsave
import numpy as np
import os

from radio_feature_extraction_app import extract_radiomic_feature
from predict_recurrence import predict_recurrence
import datetime

import logging


UPLOAD_FOLDER = '/uploads'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

logging.basicConfig(filename = './fileinfo.log', level = logging.DEBUG)
logger = logging.getLogger(__name__)
formatter = logging.Formatter('[%(asctime)s][%(levelname)s|%(filename)s:%(lineno)s] >> %(message)s')
fileHandler = logging.FileHandler('./fileinfo.log')
fileHandler.setFormatter(formatter)
logger.setLevel(logging.DEBUG)
logger.addHandler(fileHandler)

access_log_file = "access_log.txt"

#trusted_addrs = ['210.222.87.154','192.168.94.46']

def file_log():
    if os.path.exists('LUAD-075.tif'):
        logger.info("Image file exists.")
        
    else:
        logger.info("Image file does not exist.")
        


def get_trusted_addrs():
    lines = []
    with open("trusted_addr.txt", "r") as file:
        for line in file:
            line = line.strip()
            lines.append(line)
    return lines

""" Uncomment this when you need to limit the access from untrusted ip
@app.before_request
def limit_remote_addr():
    trusted_addrs = get_trusted_addrs()

    dt = datetime.datetime.now()
    date = dt.strftime("%Y-%m-%d-%H:%M:%S")
    if request.remote_addr in trusted_addrs:
        with open(access_log_file, "a") as f:
            f.write("{} accessed from {}\n".format(date, request.remote_addr))
        pass
    else:
        with open(access_log_file, "a") as f:
            f.write("{} access denied {}\n".format(date, request.remote_addr))
        return '<html><body><h4> Not allowed for accessing this site. <br/> Ask site administrator. </h4></body></html>'
"""


@app.route('/')
def index():
    return redirect(url_for('home'))

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/disclaimer')
def disclaimer():
    return render_template('disclaimer.html')

@app.route('/algorithm')
def algorithm():
    return render_template('algorithm.html')

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

@app.route('/predict', methods = ['POST'])
def get_data_and_predict_prob():

    clinic_features = []

    #AD/SC
    if request.form['adsc'] == 'ad':
        clinic_features.append(1)
        clinic_features.append(0)
    elif request.form['adsc'] == 'sc':
        clinic_features.append(0)
        clinic_features.append(1)

    #AGE
    clinic_features.append(request.form['age'])

    #T Stage
    if request.form['tstage'] == 't1':
        clinic_features.append(1)
        clinic_features.append(0)
        clinic_features.append(0)
    elif request.form['tstage'] == 't2':
        clinic_features.append(0)
        clinic_features.append(1)
        clinic_features.append(0)
    elif request.form['tstage'] == 't3':
        clinic_features.append(0)
        clinic_features.append(0)
        clinic_features.append(1)

    #Residual tumor
    if request.form['tumor'] == 'r0':
        clinic_features.append(1)
        clinic_features.append(0)
    elif request.form['tumor'] == 'r1':
        clinic_features.append(0)
        clinic_features.append(1)

    #N Stage
    if request.form['nstage'] == 'n0':
        clinic_features.append(1)
        clinic_features.append(0)
        clinic_features.append(0)
    elif request.form['nstage'] == 'n1':
        clinic_features.append(0)
        clinic_features.append(1)
        clinic_features.append(0)
    elif request.form['nstage'] == 'n2':
        clinic_features.append(0)
        clinic_features.append(0)
        clinic_features.append(1)

    clinic_features.append(request.form['nlr'])
    clinic_features.append(request.form['pnr'])
    clinic_features.append(request.form['hg'])
    #clinic_features.append(request.form['alt'])

    #Visceral pleural invasion
    if request.form['pleural'] == 'plus':
        clinic_features.append(1)
        clinic_features.append(0)
    elif request.form['pleural'] == 'minus':
        clinic_features.append(0)
        clinic_features.append(1)

    #Lymphovascular space invasion
    if request.form['lymphovascular'] == 'plus':
        clinic_features.append(1)
        clinic_features.append(0)
    elif request.form['lymphovascular'] == 'minus':
        clinic_features.append(0)
        clinic_features.append(1)

    clinic_features.append(request.form['lymph_node'])
    clinic_features.append(request.form['sodium'])
    clinic_features.append(request.form['albumin'])

    img_file = request.files['img_file']
    label_file = request.files['label_file']

    if img_file and label_file:
        img = secure_filename(img_file.filename)
        img_file.save(img)
        label = secure_filename(label_file.filename)
        label_file.save(label)


    # extract features
    radiomic_features = extract_radiomic_feature(img, label)
    features = clinic_features + radiomic_features 
    
    file_log()
    #업로드한 이미지를 삭제한다.
    os.remove(img)
    os.remove(label)

    file_log()
    # predict
    prob = predict_recurrence((np.asarray(features)).reshape(1, -1))

    return jsonify({'result': prob }),200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888, debug=True)
