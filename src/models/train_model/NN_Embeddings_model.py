from keras.preprocessing.sequence import pad_sequences
from keras.preprocessing.text import Tokenizer

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
from keras.models import Sequential, Model
from keras.layers import Dense, Dropout, Flatten, Input,  Embedding,BatchNormalization,Activation
from keras.layers.merge import Concatenate
from keras import regularizers
import keras.regularizers as kr
import pandas as pd
import sys 
sys.path.append("../../src/features")
import build_features
import RFV_text_vectorizing

def set_RFV_text(x):
    text = ""
    if x['RFV1_text'] != 'blank entry':
        text += "<s> " +x['RFV1_text']  + " <s>"
    if x['RFV2_text'] != 'blank entry':
        text += "<s> " +x['RFV2_text']  + " <s>"
    if x['RFV3_text'] != 'blank entry':
        text += "<s> " +x['RFV3_text']  + " <s>"
    if x['RFV4_text'] !='blank entry':
        text += "<s> " +x['RFV4_text']  + " <s>"
    if x['RFV5_text'] != 'blank entry':
        text += "<s> " +x['RFV5_text']  + " <s>"
    return text 

def vectorize_words(col_text, MAX_NB_WORDS, verbose = True):
    """Takes a note column and encodes it into a series of integer
        Also returns the dictionnary mapping the word to the integer"""
    tokenizer = Tokenizer(num_words = MAX_NB_WORDS)
    tokenizer.fit_on_texts(col_text)
    data = tokenizer.texts_to_sequences(col_text)
    note_length =  [len(x) for x in data]
    vocab = tokenizer.word_index
    MAX_VOCAB = len(vocab)
    max_length = np.max(note_length)
    if verbose == True:
        print('Vocabulary size: %s' % MAX_VOCAB)
        print('Average text length: %s' % np.mean(note_length))
        print('Max text length: %s' %  max_length)
    return data, vocab, MAX_VOCAB, tokenizer,  max_length

def pad_rfv_text(data, MAX_SEQ_LENGTH):
    data = pad_sequences(data, maxlen = MAX_SEQ_LENGTH)
    return data

def vectorize_RFV_text (predictors, debug=False):
    # append all RFVn_text  into RFV_text
    predictors['RFV_text'] = predictors.apply(set_RFV_text, axis=1)
    predictors =predictors.drop(['RFV1_text','RFV2_text','RFV3_text',
                                 'RFV4_text','RFV5_text'], axis=1)
    if debug:
        print('-' * 100)
        print('RFV_text appended from RFV1_text,RFV2_text,RFV3_text,RFV4_text,RFV5_text')
        print('-'* 100) 
        print(predictors[:5][['RFV_text'] ])
        print('-'* 100) 
    
    #vectorize, get a number_id for each word 
    MAX_VOCAB = None # to limit original number of words (None if no limit)
    rfv_data_vectorized, dictionary, MAX_VOCAB, tokenizer,  max_seq_length = \
              vectorize_words(predictors['RFV_text'], MAX_VOCAB, verbose = True)
    if debug:
        print('-' * 100)
        print("data vectorized")
        print('-'* 100) 
        print(rfv_data_vectorized [:5])

    #make each rfv_data_vectorized the same length, appending zeroes      
    rfv_data = pad_rfv_text(rfv_data_vectorized, max_seq_length)
    
    predictors =predictors.drop(['RFV_text'], axis=1)
    return predictors, rfv_data, max_seq_length, MAX_VOCAB, dictionary, tokenizer 
    
def create_e_model(input_shape,   input_text_length, vocab_size, embedding_size, l2=0.005 , units=100, n_layers = 3):    

    data_input = Input(shape =input_shape)
    text_input = Input(shape=(input_text_length, ))  
    
    #embeddings
    text_embeddings = Embedding(vocab_size + 1, 
                                embedding_size, 
                                input_length=input_text_length,
                                embeddings_regularizer=regularizers.l2(0.001),)( text_input)
    text_embeddings = Flatten () (text_embeddings)
    
    #text_embeddings = BatchNormalization()(text_embeddings)

    input_merged = Concatenate(axis=-1)([data_input,text_embeddings])
    x = Dense(units=units,  kernel_regularizer=kr.l2(l2), kernel_initializer='he_normal',
              activation='relu')(input_merged)
   
    for i in range (1, n_layers):
        x =  Dense(units=units,   kernel_regularizer=kr.l2(l2),kernel_initializer='he_normal',
                   activation='relu')(x)

    model_output = Dense(units=1,kernel_initializer=  'glorot_normal',
                         activation='sigmoid')(x)
    
    model = Model(inputs=[data_input, text_input], outputs=model_output)   
    model.compile(loss='binary_crossentropy', # Cross-entropy
                    optimizer= 'nadam'  , 
                    metrics=['accuracy']) # Accuracy performance metric
    #model.summary()
    return model

def create_e_model_4_layers(input_shape,   input_text_length, vocab_size, embedding_size, l2=0.005, units=100 ):    

    model = create_e_model(input_shape,   input_text_length, vocab_size, embedding_size, l2=l2, units=units, n_layers = 4)
    #model.summary()
    return model

def train_cdc_e_model ( X_train, rfv_train,  y_train,X_dev,rfv_dev, y_dev,
                       num_epochs,  network, verbose_flag=False ):
    verbose = 1 if verbose_flag else 0 
    #class weight
    class_weight_v = class_weight.compute_class_weight('balanced', np.unique(y_train), y_train)
    class_weight_dict = dict(enumerate(class_weight_v))
    # Fit the model
    history = network.fit([X_train,rfv_train], # Features
                      y_train, # Target vector
                      epochs=num_epochs, # Number of epochs
                      verbose=verbose, # Print description after each epoch
                      batch_size=1024, # Number of observations per batch 512
                      validation_data=([X_dev, rfv_dev], y_dev),
                      class_weight=class_weight_dict) 
    #scores = network.evaluate([np.array(X_dev),np.array(rfv_dev)], np.array(y_dev), verbose=0)
    y_pred = network.predict([X_dev,rfv_dev], batch_size=1024)
    fpr, tpr, thresholds = metrics.roc_curve(y_dev,y_pred, pos_label = 1)
    roc_auc = metrics.auc(fpr, tpr)
    print("%s: %.2f%%" % ("AUROC", roc_auc*100))
    return roc_auc

def cross_e_Validation (nepochs, predictors, rfv_text, target,max_seq_length,MAX_VOCAB,l2,
                        embedding_size=100,units=100):
    # the default was embedding_size = 100 and units = 100
    seed = np.random.seed(0)
    kfold = StratifiedKFold(n_splits=10, shuffle=True, random_state=seed)
    cvscores = []
    for train, test in kfold.split(predictors, target):    
        X_train = np.array(predictors)[train]
        X_dev = np.array(predictors)[test]
        rfv_train = np.array(rfv_text)[train]
        rfv_dev = np.array(rfv_text)[test]
        y_train = np.array (target)[train]
        y_dev= np.array(target)[test]
        model_cdc = create_e_model(X_train.shape[1:],input_text_length= max_seq_length, 
                         vocab_size = MAX_VOCAB, embedding_size=embedding_size,l2=l2,units=units)
        roc_auc = train_cdc_e_model ( X_train, rfv_train, y_train, X_dev, rfv_dev,  y_dev,
                                   nepochs, model_cdc, verbose_flag= False )
        cvscores.append(roc_auc)
    print("ROC AUC: %.4f%% (+/- %.2f%%)" % (np.mean(cvscores)*100, np.std(cvscores)*100))

    
def train_cdc_e_model_true_positive ( X_train, rfv_train,  y_train,X_dev,rfv_dev, y_dev,
                       num_epochs,  network, verbose_flag=False ):
    verbose = 1 if verbose_flag else 0 
    #class weight
    class_weight_v = class_weight.compute_class_weight('balanced', np.unique(y_train), y_train)
    class_weight_dict = dict(enumerate(class_weight_v))
    # Fit the model
    history = network.fit([X_train,rfv_train], # Features
                      y_train, # Target vector
                      epochs=num_epochs, # Number of epochs
                      verbose=verbose, # Print description after each epoch
                      batch_size=1024, # Number of observations per batch 512
                      validation_data=([X_dev, rfv_dev], y_dev),
                      class_weight=class_weight_dict) 
    #scores = network.evaluate([np.array(X_dev),np.array(rfv_dev)], np.array(y_dev), verbose=0)
    y_pred = network.predict([X_dev,rfv_dev], batch_size=1024)
    fpr, tpr, thresholds = metrics.roc_curve(y_dev,y_pred, pos_label = 1)
    roc_auc = metrics.auc(fpr, tpr)
    return roc_auc, y_pred
#------------------------------------------------------------------------------------
# Training FNN_TE model and showing 10 fold cross validation 
#------------------------------------------------------------------------------------
def FNN_TE_model_training(config, filename):
    processedDirectory = config['dataDirectory'] + config['processedDirectory']
    cdc_input = pd.read_csv(processedDirectory + filename  )
    # it includes the textual descriptions for the RFV (Reason for Visit) codes 
    predictors, target = build_features.get_all_features (cdc_input, normalize=True,with_features_for_Embedding = True ) 
    # vectorizing text for embedding training 
    predictors, rfv_data, max_seq_length, MAX_VOCAB,  tokenizer =  RFV_text_vectorizing.vectorize_RFV_text (predictors,  debug=False,in_predictors = False)
    # Hyperparameters tuned using notebook
    cross_e_Validation (20, predictors, rfv_data, target,max_seq_length,MAX_VOCAB,l2 =0.005,
                                        embedding_size=30, units =100)
    
#------------------------------------------------------------------------------------
# For Prediction
#------------------------------------------------------------------------------------
def vectorize_RFV_text_prediction(predictors, tokenizer,max_length):
    predictors['RFV_text'] = predictors.apply(set_RFV_text, axis=1)
    predictors =predictors.drop(['RFV1_text','RFV2_text','RFV3_text',
                                 'RFV4_text','RFV5_text'], axis=1)
    rfv_data_vectorized = tokenizer.texts_to_sequences( predictors['RFV_text'])  
    rfv_data = pad_rfv_text(rfv_data_vectorized, max_length)
    predictors =predictors.drop(['RFV_text'], axis=1)
    return predictors,rfv_data

