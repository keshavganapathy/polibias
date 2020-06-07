# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 14:53:27 2020

@author: Keshav Ganapathy
"""

#import statements
import os
os.environ['KERAS_BACKEND'] = 'theano'
from keras import models
from keras.preprocessing.text import Tokenizer
from keras import preprocessing
import numpy as np

class Network:
    text = ""
    value = 0
    bias = ""
    def __init__(self, string):
        self.text = string
        self.value, self.bias = self.predict()

    def preprocessData(self):
        string = [self.text]
        max_features = 50000
        max_length = 500
        tokenizer = Tokenizer(num_words=max_features)
        tokenizer.fit_on_texts(string)
        tokens = tokenizer.texts_to_sequences(string)
        x =  preprocessing.sequence.pad_sequences(tokens, max_length)
        return np.asarray(x).astype("float32")
    
    def predict(self):
        political_model = models.load_model("PoliticalBias.h5")
        data = self.preprocessData()
        prediction = political_model.predict(data)[0][0]
        prediction_str = ""
        if prediction>=0 and prediction<=.2:
            prediction_str = "Radically Liberal"
        elif prediction>.2 and prediction<.4:
            prediction_str = "Moderately Liberal"
        elif prediction>=.4 and prediction<=.6:
            prediction_str = "Moderate"
        elif prediction>.6 and prediction<.8:
            prediction_str = "Moderately Conservative"
        else:
            prediction_str ="Radically Conservative"
        #print(prediction_str)
        return [prediction, prediction_str]
    
    def getVal(self):
        return self.value
    
    def getBias(self):
        return self.bias