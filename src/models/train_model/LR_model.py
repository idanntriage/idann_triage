from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn import metrics
import numpy as np
import pandas as pd
import sys 
from sklearn.cross_validation import train_test_split
from sklearn.cross_validation import StratifiedKFold
sys.path.append("../../src/features")
import build_features

def LR_modeling(X_train, y_train, X_dev, y_dev):
    c_test = [0.00001, 0.0001, 0.001, 0.005, 0.01, 0.05,  0.1, 0.5,  1.0, 2.0, 4.0, 6.0, 8.0, 10.0]
    for m in c_test:
        logit = LogisticRegression(C = m, penalty = 'l2',class_weight='balanced')
        logit.fit(X_train, y_train)
        predicted_prob = logit.predict_proba(X_dev)
        fpr, tpr, thresholds = metrics.roc_curve(y_dev,predicted_prob[:,1], pos_label = 1)
        roc_auc = metrics.auc(fpr, tpr)        
        print('C= %1.4f, ROC_AUC = %1.4f ' % (m, roc_auc))
        
def cross_LR_Validation (predictors, target, c=1.0):
    seed = np.random.seed(0)
    #kfold = StratifiedKFold(n_splits=10, shuffle=True, random_state=seed)
    kfold = StratifiedKFold(target, n_folds=10, shuffle=True)
    cvscores = []
    #for train, test in kfold.split(predictors, target):
    for train, test in kfold:
        X_train = np.array(predictors)[train]
        X_dev = np.array(predictors)[test]
        y_train = np.array (target)[train]
        y_dev = np.array(target)[test]
        logit = LogisticRegression(C = c, penalty = 'l2',class_weight='balanced')
        logit.fit(X_train, y_train)
        predicted_prob = logit.predict_proba(X_dev)
        fpr, tpr, thresholds = metrics.roc_curve(y_dev,predicted_prob[:,1], pos_label = 1)
        roc_auc = metrics.auc(fpr, tpr)
        print('ROC_AUC = %1.4f ' % (roc_auc))
        cvscores.append(roc_auc)
    print("ROC AUC: %.4f%% (+/- %.2f%%" % (np.mean(cvscores), np.std(cvscores)))
    
def LR_modeling_test(X_train, y_train, X_dev, y_dev, c):
    logit = LogisticRegression(C = c, penalty = 'l2',class_weight='balanced')
    logit.fit(X_train, y_train)
    predicted_prob = logit.predict_proba(X_dev)
    y_pred =logit.predict(X_dev)
    fpr, tpr, thresholds = metrics.roc_curve(y_dev,predicted_prob[:,1], pos_label = 1)
    roc_auc = metrics.auc(fpr, tpr)        
    print('C= %1.4f, ROC_AUC = %1.4f ' % (c, roc_auc))
    return y_pred

def LR_BAS_model_training(fileConfig, filename) :
    processedDirectory = fileConfig['dataDirectory'] + fileConfig['processedDirectory']
    cdc_input = pd.read_csv(processedDirectory + filename  )
    predictors, target = build_features.get_baseline_features (cdc_input )
    # Hyperparameter tunned using notebook
    cross_LR_Validation ( predictors, target, c=1.0) 
    
def LR_RMH_model_training(fileConfig, filename) :
    processedDirectory = fileConfig['dataDirectory'] + fileConfig['processedDirectory']
    cdc_input = pd.read_csv(processedDirectory +  filename )
    predictors, target = build_features.get_all_features (cdc_input )
    # Hyperparameter tunned using notebook
    cross_LR_Validation ( predictors, target, c=1.0)