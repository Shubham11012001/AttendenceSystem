import _pickle as cPickle
import numpy as np
from scipy.io.wavfile import read
from sklearn import mixture
from sklearn.mixture import GaussianMixture
import warnings
from . import featureExctrection


def training_data(username0):
    username = username0
    warnings.filterwarnings("ignore")
    source = ''
    dest = "userRecognition/speakermodels/"
    train_files = "userRecognition/textFiles/"+username+".txt"
    file_paths= open(train_files,'r')
    count=1
    features = np.asarray(())
    for path in file_paths:
        path = path.strip()
        print(path)
        
        sr,audio = read(source + path)
        vector = featureExctrection.extract_features(audio,sr)
        
        if features.size == 0:
            features = vector
        else:
            features = np.vstack((features, vector))
            
        if count == 15:
            #gmm = mixture.GMM(n_componenets = 16, n_iter = 200, covariance_type = 'diag', n_init=3)
            #gmm.fit(features)
            gmm = GaussianMixture(n_components=16,covariance_type='diag', n_init=3)
            gmm.fit(features)
            
            picklefile = username+".gmm"
            print(picklefile)
            cPickle.dump(gmm,open(dest+picklefile,'wb'))
            print("modeling completed for speaker",picklefile,"with data point",features.shape)
            features = np.asarray(())
            count = 0
        count +=1
        
    print("Done..!")