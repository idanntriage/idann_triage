from keras import models
from keras import layers
from keras import optimizers
from keras.layers import  Dropout
import keras.regularizers as kr
from sklearn.utils import class_weight
import numpy as np
from sklearn.metrics import roc_auc_score
from sklearn import metrics
from keras.models import load_model
from keras.models import Sequential
from keras.layers import Dense
import keras.regularizers as kr
from sklearn.model_selection import StratifiedKFold
import pandas as pd
import sys 
sys.path.append("../../src/features")
import build_features



def create_model(input_shape, l2=0.005, units_n = 100, n_layers = 3):
    network = models.Sequential()
    # Add fully connected layer with a softmax activation function
    network.add(layers.Dense(units=units_n,  kernel_regularizer=kr.l2(l2), activation='relu', input_shape=(input_shape)))
    for i in range (1, n_layers):
        network.add(layers.Dense(units=units_n,   kernel_regularizer=kr.l2(l2),activation='relu'))
    network.add(layers.Dense(units=1,  activation='sigmoid'))
    network.compile(loss='binary_crossentropy', # Cross-entropy
                    optimizer= 'nadam'  , 
                    metrics=['accuracy']) # Accuracy performance metric
    return network

def train_cdc_model ( X_train, y_train, X_dev, y_dev, num_epochs ,  network , verbose_flag=False):
    verbose = 1 if verbose_flag else 0 
    #class weight
    class_weight_v = class_weight.compute_class_weight('balanced', np.unique(y_train), y_train)
    class_weight_dict = dict(enumerate(class_weight_v))
    # Fit the model
    history = network.fit(np.array(X_train), # Features
                      y_train, # Target vector
                      epochs=num_epochs, # Number of epochs
                      verbose=verbose, # Print description after each epoch
                      batch_size=1024, # Number of observations per batch 512
                      validation_data=(np.array(X_dev), np.array(y_dev)),
                      class_weight=class_weight_dict) 
    scores = network.evaluate(np.array(X_dev), np.array(y_dev), verbose=0)
    y_pred = network.predict_proba(np.array(X_dev), batch_size=50)
    fpr, tpr, thresholds = metrics.roc_curve(np.array(y_dev),y_pred, pos_label = 1)
    roc_auc = metrics.auc(fpr, tpr)
    print("%s: %.2f%%" % ("AUROC", roc_auc*100))
    return roc_auc

def cross_Validation (nepochs, predictors, target,l2=0.005,units_n = 100, n_layers = 3):
    seed = np.random.seed(0)
    kfold = StratifiedKFold(n_splits=10, shuffle=True, random_state=seed)
    cvscores = []
    for train, test in kfold.split(predictors, target):
        X_train_cv = np.array(predictors)[train]
        X_dev_cv = np.array(predictors)[test]
        y_train_cv = np.array (target)[train]
        y_dev_cv = np.array(target)[test]
        network = create_model(X_train_cv.shape[1:],l2,units_n , n_layers)
        roc = train_cdc_model (X_train_cv, y_train_cv, X_dev_cv, y_dev_cv,num_epochs= nepochs,  network=network, verbose_flag=False)
        cvscores.append(roc)
    print("ROC AUC: %.2f%% (+/- %.2f%%)" % (np.mean(cvscores)*100, np.std(cvscores)))

    
def train_cdc_model_true_positive ( X_train, y_train, X_dev, y_dev, num_epochs ,  network , verbose_flag=False):
    verbose = 1 if verbose_flag else 0 
    #class weight
    class_weight_v = class_weight.compute_class_weight('balanced', np.unique(y_train), y_train)
    class_weight_dict = dict(enumerate(class_weight_v))
    # Fit the model
    history = network.fit(np.array(X_train), # Features
                      y_train, # Target vector
                      epochs=num_epochs, # Number of epochs
                      verbose=verbose, # Print description after each epoch
                      batch_size=1024, # Number of observations per batch 512
                      validation_data=(np.array(X_dev), np.array(y_dev)),
                      class_weight=class_weight_dict) 
    scores = network.evaluate(np.array(X_dev), np.array(y_dev), verbose=0)
    y_pred = network.predict_classes(np.array(X_dev), batch_size=50)
    return y_pred

def FNN_model_training(config, filename):
    processedDirectory = config['dataDirectory'] + config['processedDirectory']
    cdc_input = pd.read_csv(processedDirectory + filename  )
    predictors, target = build_features.get_all_features (cdc_input, normalize=True  )
    # Hyperparameters tuned using notebook
    cross_Validation (nepochs=100, predictors=predictors, target=target,l2=0.01,units_n = 100, n_layers = 3)
    