'''
@ Sehwa Moon
@ 2020.01.17
@ predict recurrence with radiomic and clinical features
  thorugh using PCA and random forest model
'''

#from sklearn.preprocessing import StandardScaler
#from sklearn.decomposition import PCA
from sklearn.externals import joblib
import numpy as np


def predict_recurrence(data_to_pred):

    loaded_scaler = joblib.load('model/scaler.pkl')
    loaded_PCA_model = joblib.load('model/pca.pkl')
    loaded_RF_model = joblib.load('model/rf.sav')

    scaled_data = loaded_scaler.transform(data_to_pred)
    pca_data = loaded_PCA_model.transform(scaled_data)
    pred = loaded_RF_model.predict_proba(pca_data)
    print(pred)
    return pred[0][1]*100
