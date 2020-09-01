'''
@ Sehwa Moon
@ 2020.01.17 extract radiomic features using pyradiomics
'''
from radiomics import featureextractor
import SimpleITK as sitk
import numpy as np

def get_feature_list(list_path):
    with open(list_path, 'r') as f:
        features = f.readlines()
    features = [f[:-1] for f in features]
    return features

# get image and label
def extract_radiomic_feature(center_img_path, label_img_path):

    if isinstance(center_img_path, str):
        center_img_2d = sitk.ReadImage(center_img_path)
        label_img_2d = sitk.ReadImage(label_img_path)

    img = sitk.JoinSeries(center_img_2d)
    lbl = sitk.JoinSeries(label_img_2d)
    
    params = 'model/params.yaml'
    extractor = featureextractor.RadiomicsFeatureExtractor(params)
    extractor.enableAllImageTypes()
    features = get_feature_list('model/selected.txt')

    result = extractor.execute(img, lbl)
    features_list = []
    for f in features:
        features_list.append(result.get(f))
    '''
    for i, j in zip(features, features_list):
        print(i, j)
    '''
    return features_list
