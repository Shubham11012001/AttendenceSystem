import os
import _pickle as cPickle
import numpy as np
from scipy.io.wavfile import read
import warnings
from . import featureExctrection
import time




def testing_recorded_audio(audio_path):
    print("got hit here")
    warnings.filterwarnings("ignore")
    source = ""
    modelpath = "userRecognition/speakermodels/"
    path = audio_path
    gmm_files = [os.path.join(modelpath,fname)for fname in os.listdir(modelpath) if fname.endswith('.gmm')]

    models = [cPickle.load(open(fname,'rb')) for fname in gmm_files]
    print(len(models))
    speaker = [fname.split('/')[-1].split(".gmm")[0] for fname in gmm_files]
    sr,audio = read(source+path)
    vector = featureExctrection.extract_features(audio,sr)
    log_likelihood = np.zeros(len(models))
    for i in range(len(models)):
        gmm = models[i]
        scores = np.array(gmm.score(vector))
        log_likelihood[i] = scores.sum()
    winner = np.argmax(log_likelihood)
    print("Detected as", speaker[winner])
    time.sleep(1.0)
    os.remove(audio_path)
    return speaker[winner]
    


    


"""warnings.filterwarnings("ignore")
source = "trainingData"
modelpath = "userRecognspeakermodels/"
gmm_files = [os.path.join(modelpath,fname)for fname in os.listdir(modelpath) if fname.endswith('.gmm')]

models = [cPickle.load(open(fname,'rb')) for fname in gmm_files]
print(len(models))
speaker = [fname.split('/')[-1].split(".gmm")[0] for fname in gmm_files]

error = 0
total_sample = 0.0

print("Do you want to test a single audio: Press '1' or The complete Test Audio Sample: Press '0'")
take = int(input())
if take ==1:
    print("Enter the file name for test audio")
    path = input()
    print("Testing Audio:",path)
    sr,audio = read(source+path)
    vector = featureExctrection.extract_features(audio,sr)
    log_likelihood = np.zeros(len(models))
    for i in range(len(models)):
        gmm = models[i]
        scores = np.array(gmm.score(vector))
        log_likelihood[i] = scores.sum()
    winner = np.argmax(log_likelihood)
    print("Detected as", speaker[winner])
    time.sleep(1.0)
 
elif take == 0:
    test_file = "testSamplePath.txt"
    with open(test_file,'r') as files_paths:
    #print(files_paths.read())
        for path in files_paths:
            total_sample +=1.0
            path = path.split()
            print("Testing Audio:", path[0])
            sr, audio = read(source+path[0])
            vector = featureExctrection.extract_features(audio,sr)
            log_likelihood = np.zeros(len(models))
            for i in range(len(models)):
                gmm = models[i]
                scores = np.array(gmm.score(vector))
                log_likelihood[i] = scores.sum()
                winner = np.argmax(log_likelihood)
                checker_name= path[0]
                if speaker[winner] != checker_name:
                    error+=1
                time.sleep(1.0)
            print('Detected as',speaker[winner])
        print(error,total_sample)
        #print(checker_name)
        
        accuracy = ((total_sample-error)/total_sample)*100
        print("The Accuracy percentage for the current testing performance with MFCC+ GMM is:",
             accuracy,"%")
        print("Speaker recognised")"""
            
        
    