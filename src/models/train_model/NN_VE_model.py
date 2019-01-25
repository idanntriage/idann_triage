##  NN model with entry attention layer for feature importance
##  Author: Zenobia Liendo
##  March 2018 
##  MIDS w210 


from keras import models
from keras import layers
from keras import optimizers
from keras.layers import  ZeroPadding1D, Lambda
from keras.layers import Dense, Dropout, Flatten, Input,  Embedding, Reshape
import keras.regularizers as kr
from sklearn.utils import class_weight
from sklearn.metrics import roc_auc_score
from sklearn import metrics
from keras.models import load_model
from keras.models import Sequential, Model
from keras.layers.merge import Concatenate
from keras.layers import LSTM
from sklearn.model_selection import StratifiedKFold
import pandas as pd
import numpy as np
from keras import backend
from keras.preprocessing.sequence import pad_sequences
from keras import regularizers
from sklearn.preprocessing import LabelEncoder
from keras.utils import np_utils
import attention_layer
import sys 
sys.path.append("../../src/features")
import build_features
import RFV_text_vectorizing
import pickle
from objdict import ObjDict

def create_model (l2=0.001, n_units =100, apply_attention=False, embedding_nh=30, n_layers =2, input_text_length=0, vocab_size=0,att_l2=0.0001, co_model=True):
    return create_att_model(l2=l2, n_units =n_units, nh=embedding_nh,  n_layers =n_layers ,
                                text_array_length=input_text_length,
                                vocab_size=vocab_size,att_l2=att_l2, co_model=co_model)



def create_att_model (l2=0.001, n_units =100 , nh=30,  n_layers =2, 
                      text_array_length=0,vocab_size=0,att_l2=0.0001, rfv_all=False, co_model=True): 
    
    #inputs
    #---------------------------------------
    input_list = []
    
    #binary
    sex_input = Input(shape =(1,))
    chf_input = Input (shape = (1,))

    
    #y2009_year_input   = Input(shape =(1,))
    #y2010_year_input   = Input(shape =(1,))
    #y2011_year_input   = Input(shape =(1,))
    #y2012_year_input   = Input(shape =(1,))
    #y2013_year_input   = Input(shape =(1,))
    #y2014_year_input   = Input(shape =(1,))
    #y2015_year_input   = Input(shape =(1,))

    
    #continuous
    age_input = Input(shape =(1,))
    pulse_input = Input (shape = (1,))
    sysbp_input = Input (shape = (1,))  
    resp_rate_input = Input (shape = (1,))
    oxygen_sat_input = Input (shape = (1,)) 
    temp_input = Input (shape = (1,))

    
    #categorical 
    rfv_digits_length = 29
    arrival_model_input = Input (shape = (1,))
    msa_input = Input (shape = (1,))
    diabetes_input = Input (shape = (1,))  
    rvf1_input = Input(shape=(5, ))
    rvf2_input = Input(shape=(5, ))
    rvf3_input = Input(shape=(5, )) 
    if rfv_all:
        rvf4_input = Input(shape=(5, )) 
        rvf5_input = Input(shape=(5, )) 
    #rfv_digits_input = Input(shape=(rfv_digits_length, ), name="rfv_digits_input")  # a vector of 29 elements
    if text_array_length > 0: 
        rfv_data_input = Input(shape=(text_array_length,),name="rfv_text_data_input")

    #additional inputs
    Hypothermia_input = Input(shape=(1,)) 
    Hyperthermia_input = Input(shape=(1,)) 
    Bradycardia_input = Input(shape=(1,)) 
    Mild_Tachycardia_input = Input(shape=(1,))
    Moderate_Tachycardia_input = Input(shape=(1,)) 
    Severe_Tachycardia_input = Input(shape=(1,)) 
    Hypotension_input = Input(shape=(1,)) 
    Hypertension_input = Input(shape=(1,)) 
    Bradypnea_input = Input(shape=(1,)) 
    Moderate_Tachypnea_input = Input(shape=(1,)) 
    Severe_Tachypnea_input = Input(shape=(1,)) 
    Mild_Hypoxia_input = Input(shape=(1,)) 
    Severe_Hypoxia_input = Input(shape=(1,))  
    
    Reason_Chest_Pain_input= Input(shape=(1,)) 
    Reason_Abdominal_Pain_input= Input(shape=(1,)) 
    Reason_Headache_input= Input(shape=(1,)) 
    Reason_Shortness_of_Breath_input= Input(shape=(1,)) 
    Reason_Cough_input= Input(shape=(1,)) 
    Reason_Nausea_Vomiting_input= Input(shape=(1,)) 
    Reason_Fever_Chills_input= Input(shape=(1,)) 
    Reason_Syncope_input= Input(shape=(1,)) 
    Reason_Dizziness_input= Input(shape=(1,)) 
    Reason_Psychiatric_Complaint_input= Input(shape=(1,)) 
    Reason_Nervous_System_input= Input(shape=(1,)) 
    Reason_Cardiovascular_Other_input= Input(shape=(1,)) 
    Reason_Ears_Eyes_Complaint_input= Input(shape=(1,)) 
    Reason_Respiratory_Other_input= Input(shape=(1,)) 
    Reason_Gastrointestinal_Other_input= Input(shape=(1,)) 
    Reason_Genitourinary_Other_input= Input(shape=(1,)) 
    Reason_Skin_Hair_Nails_Complaint_input= Input(shape=(1,)) 
    Reason_Musculoskeletal_Other_input= Input(shape=(1,)) 
    Reason_Injury_Poisoning_input= Input(shape=(1,)) 
    Reason_Other_input= Input(shape=(1,))
    Age_18_30_input= Input(shape=(1,))
    Age_31_40_input= Input(shape=(1,))
    Age_41_50_input= Input(shape=(1,))
    Age_51_60_input= Input(shape=(1,))
    Age_61_70_input= Input(shape=(1,))
    Age_71_80_input= Input(shape=(1,))
    Age_81_Above_input = Input(shape=(1,))
    
    
    input_list = [sex_input, age_input,arrival_model_input,msa_input, chf_input,
                 diabetes_input,temp_input,pulse_input,sysbp_input,resp_rate_input,oxygen_sat_input,
                  Hypothermia_input,
    Hyperthermia_input,
    Bradycardia_input,
    Mild_Tachycardia_input ,
    Moderate_Tachycardia_input,
    Severe_Tachycardia_input,
    Hypotension_input,
    Hypertension_input,
    Bradypnea_input,
    Moderate_Tachypnea_input,
    Severe_Tachypnea_input,
    Mild_Hypoxia_input,
    Severe_Hypoxia_input,  
    Reason_Chest_Pain_input, 
    Reason_Abdominal_Pain_input, 
    Reason_Headache_input, 
    Reason_Shortness_of_Breath_input, 
    Reason_Cough_input, 
    Reason_Nausea_Vomiting_input, 
    Reason_Fever_Chills_input, 
    Reason_Syncope_input, 
    Reason_Dizziness_input, 
    Reason_Psychiatric_Complaint_input, 
    Reason_Nervous_System_input, 
    Reason_Cardiovascular_Other_input, 
    Reason_Ears_Eyes_Complaint_input, 
    Reason_Respiratory_Other_input, 
    Reason_Gastrointestinal_Other_input, 
    Reason_Genitourinary_Other_input, 
    Reason_Skin_Hair_Nails_Complaint_input, 
    Reason_Musculoskeletal_Other_input, 
    Reason_Injury_Poisoning_input, 
    Reason_Other_input,
    Age_18_30_input,
     Age_31_40_input,
     Age_41_50_input,
     Age_51_60_input,
     Age_61_70_input,
     Age_71_80_input,
     Age_81_Above_input,
     #y2009_year_input,
     #y2010_year_input,
    #y2011_year_input,
    #y2012_year_input,
    #y2013_year_input,
    #y2014_year_input,
    #y2015_year_input,
    rvf1_input, rvf2_input, rvf3_input]
    
    if rfv_all:
        input_list.extend([rvf4_input,rvf5_input])
    
    if text_array_length > 0: 
        #including rfv text
        input_list.append(rfv_data_input)
        
    
    
    
    #attention conversion
        
    #binary indicators  
    chf_output = Dense(nh, name ="chf_indicator")(chf_input)
    sex_output = Dense(nh, name="sex_indicator")(sex_input)
    #y2009_year_output = Dense(nh, name="year_2009_indicator")(  y2009_year_input)
    #y2010_year_output = Dense(nh, name="year_2010_indicator")(  y2010_year_input)
    #y2011_year_output = Dense(nh, name="year_2011_indicator")(  y2011_year_input)
    #y2012_year_output = Dense(nh, name="year_2012_indicator")(  y2012_year_input)
    #y2013_year_output = Dense(nh, name="year_2013_indicator")(  y2013_year_input)
    #y2014_year_output = Dense(nh, name="year_2014_indicator")(  y2014_year_input)
    #y2015_year_output = Dense(nh, name="year_2015_indicator")(  y2015_year_input)
    
    # binary for vital signs
    Hypothermia_output =Dense(nh, name="Hypothermia")(Hypothermia_input)
    Hyperthermia_output =Dense(nh, name="Hyperthermia")(Hyperthermia_input)
    Bradycardia_output =Dense(nh, name="Bradycardia")(Bradycardia_input)
    Mild_Tachycardia_input = Dense(nh, name="Mild_Tachycardia")(Mild_Tachycardia_input)
    Moderate_Tachycardia_output =Dense(nh, name="Moderate_Tachycardia")(Moderate_Tachycardia_input)
    Severe_Tachycardia_output =Dense(nh, name="Severe_Tachycardia")(Severe_Tachycardia_input)
    Hypotension_output =Dense(nh, name="Hypotension")(Hypotension_input)
    Hypertension_output =Dense(nh, name="Hypertension")(Hypertension_input)
    Bradypnea_output =Dense(nh, name="Bradypnea")(Bradypnea_input)
    Moderate_Tachypnea_output =Dense(nh, name="Moderate_Tachypnea")(Moderate_Tachypnea_input)
    Severe_Tachypnea_output =Dense(nh, name="Severe_Tachypnea")(Severe_Tachypnea_input)
    Mild_Hypoxia_output =Dense(nh, name="Mild_Hypoxia")(Mild_Hypoxia_input)
    Severe_Hypoxia_output =Dense(nh, name="Severe_Hypoxia")(Severe_Hypoxia_input)
    
    # binary for rfv 
    Reason_Chest_Pain_output=Dense(nh, name="Reason_Chest_Pain")(Reason_Chest_Pain_input) 
    Reason_Abdominal_Pain_output=Dense(nh, name="Reason_Abdominal_Pain")(Reason_Abdominal_Pain_input) 
    Reason_Headache_output=Dense(nh, name="Reason_Headache")(Reason_Headache_input) 
    Reason_Shortness_of_Breath_output=Dense(nh, name="Reason_Shortness_of_Breath")(Reason_Shortness_of_Breath_input) 
    Reason_Cough_output=Dense(nh, name="Reason_Cough")(Reason_Cough_input) 
    Reason_Nausea_Vomiting_output=Dense(nh, name="Reason_Nausea_Vomiting")(Reason_Nausea_Vomiting_input) 
    Reason_Fever_Chills_output=Dense(nh, name="Reason_Fever_Chills")(Reason_Fever_Chills_input) 
    Reason_Syncope_output=Dense(nh, name="Reason_Syncope")(Reason_Syncope_input) 
    Reason_Dizziness_output=Dense(nh, name="Reason_Dizziness")(Reason_Dizziness_input)
    Reason_Psychiatric_Complaint_output=Dense(nh, name="Reason_Psychiatric_Complaint")(Reason_Psychiatric_Complaint_input) 
    Reason_Nervous_System_output=Dense(nh, name="Reason_Nervous_System")(Reason_Nervous_System_input) 
    Reason_Cardiovascular_Other_output=Dense(nh, name="Reason_Cardiovascular_Other")(Reason_Cardiovascular_Other_input) 
    Reason_Ears_Eyes_Complaint_output=Dense(nh, name="Reason_Ears_Eyes_Complaint")(Reason_Ears_Eyes_Complaint_input) 
    Reason_Respiratory_Other_output=Dense(nh, name="Reason_Respiratory_Other")(Reason_Respiratory_Other_input) 
    Reason_Gastrointestinal_Other_output=Dense(nh, name="Reason_Gastrointestinal_Other")(Reason_Gastrointestinal_Other_input) 
    Reason_Genitourinary_Other_output=Dense(nh, name="Reason_Genitourinary_Other")(Reason_Genitourinary_Other_input) 
    Reason_Skin_Hair_Nails_Complaint_output=Dense(nh, name="Reason_Skin_Hair_Nails_Complaint")(Reason_Skin_Hair_Nails_Complaint_input) 
    Reason_Musculoskeletal_Other_output=Dense(nh, name="Reason_Musculoskeletal_Other")(Reason_Musculoskeletal_Other_input) 
    Reason_Injury_Poisoning_output=Dense(nh, name="Reason_Injury_Poisoning")(Reason_Injury_Poisoning_input) 
    Reason_Other_output=Dense(nh, name="Reason_Other")(Reason_Other_input)
    
    #binary for Age buckets
    Age_18_30_output =Dense(nh, name="Age_18_30_range")(Age_18_30_input)
    Age_31_40_output =Dense(nh, name="Age_31_40_range")(Age_31_40_input)
    Age_41_50_output =Dense(nh, name="Age_41_50_range")(Age_41_50_input)
    Age_51_60_output =Dense(nh, name="Age_51_60_range")(Age_51_60_input)
    Age_61_70_output =Dense(nh, name="Age_61_70_range")(Age_61_70_input)
    Age_71_80_output =Dense(nh, name="Age_71_80_range")(Age_71_80_input)
    Age_81_Above_output =Dense(nh, name="Age_81_Above")(Age_81_Above_input )
    
        
    #categorical embeddings
    arrival_model_embedding =  Embedding(4, nh)(arrival_model_input) 
    arrival_model_output = Reshape(target_shape=(nh,), name="arrival_model")(arrival_model_embedding )
    
    msa_embedding  = Embedding(3, nh)(msa_input)
    msa_output = Reshape(target_shape=(nh,), name="msa_indicator")(msa_embedding )
        
    diabetes_embedding  = Embedding(3, nh)(diabetes_input)  
    diabetes_output = Reshape(target_shape=(nh,), name="diabetes_indicator")(diabetes_embedding )
    
    # rfv, each feature is a digit code        
    rfv1_output = Dense(nh,kernel_regularizer=kr.l2(l2),  activation='relu', name="reason1_for_visit")(rvf1_input )
    rfv2_output = Dense(nh,kernel_regularizer=kr.l2(l2),  activation='relu', name="reason2_for_visit")(rvf2_input )
    rfv3_output = Dense(nh,kernel_regularizer=kr.l2(l2),  activation='relu', name="reason3_for_visit")(rvf3_input )
    if rfv_all:
        rfv4_output = Dense(nh,kernel_regularizer=kr.l2(l2),  activation='relu', name="reason4_for_visit")(rvf4_input )
        rfv5_output = Dense(nh,kernel_regularizer=kr.l2(l2),  activation='relu', name="reason5_for_visit")(rvf5_input )
    #rfv_digits_output = Dense(nh,kernel_regularizer=kr.l2(l2),  activation='relu', name="reasons_for_visit")(rfv_digits_input )
    
    #all rfv digit codes consolidated in one vector
    #rfv_digits_embedding  = Embedding(11, nh, name="rfv_digits_embeddings")( rfv_input)  
    
    # text embeddings
    if text_array_length > 0:
        rfv_data_text_embedding  = Embedding(vocab_size + 1, nh, 
                                             embeddings_regularizer=regularizers.l2(0.001),
                                             name="rfv_text_embeddings")(  rfv_data_input)

    
    #continuous 
    age_output = Dense(nh,kernel_regularizer=kr.l2(l2),  activation='relu', name="Age")(age_input )
    temp_output = Dense(nh, kernel_regularizer=kr.l2(l2), activation='relu', name="Temperature")(temp_input)
    pulse_output = Dense(nh, kernel_regularizer=kr.l2(l2), activation='relu', name = "Pulse_Heart_rate")(pulse_input )
    sysbp_output = Dense(nh, kernel_regularizer=kr.l2(l2), activation='relu', name ="Systolic_blood_pressure")(sysbp_input )       
    resp_rate_output = Dense(nh, kernel_regularizer=kr.l2(l2), activation='relu', name ="Respiratory_rate")(resp_rate_input )
    oxygen_sat_output = Dense(nh,kernel_regularizer=kr.l2(l2),  activation='relu', name ="Oxygen_Saturation")(oxygen_sat_input )    

    #stack inputs 
    model_outputs = [sex_output, arrival_model_output,msa_output, chf_output, diabetes_output,
                  age_output, temp_output,pulse_output,sysbp_output,resp_rate_output,oxygen_sat_output,  
                      Hypothermia_output ,
    Hyperthermia_output ,
    Bradycardia_output ,
    Mild_Tachycardia_input , 
    Moderate_Tachycardia_output ,
    Severe_Tachycardia_output ,
    Hypotension_output ,
    Hypertension_output ,
    Bradypnea_output ,
    Moderate_Tachypnea_output ,
    Severe_Tachypnea_output ,
    Mild_Hypoxia_output ,
    Severe_Hypoxia_output ,
    Reason_Chest_Pain_output, 
    Reason_Abdominal_Pain_output, 
    Reason_Headache_output, 
    Reason_Shortness_of_Breath_output, 
    Reason_Cough_output, 
    Reason_Nausea_Vomiting_output, 
    Reason_Fever_Chills_output, 
    Reason_Syncope_output, 
    Reason_Dizziness_output, 
    Reason_Psychiatric_Complaint_output, 
    Reason_Nervous_System_output, 
    Reason_Cardiovascular_Other_output, 
    Reason_Ears_Eyes_Complaint_output, 
    Reason_Respiratory_Other_output, 
    Reason_Gastrointestinal_Other_output, 
    Reason_Genitourinary_Other_output, 
    Reason_Skin_Hair_Nails_Complaint_output, 
    Reason_Musculoskeletal_Other_output, 
    Reason_Injury_Poisoning_output, 
    Reason_Other_output,
     Age_18_30_output,
     Age_31_40_output,
     Age_41_50_output,
     Age_51_60_output,
     Age_61_70_output,
     Age_71_80_output,
     Age_81_Above_output,    
     #y2009_year_output ,
     #y2010_year_output , 
     #y2011_year_output ,
     #y2012_year_output , 
     #y2013_year_output ,
     #y2014_year_output ,
     #y2015_year_output ,
     rfv1_output, rfv2_output, rfv3_output]
    
    if rfv_all:
        model_outputs.extend([rfv4_output,rfv5_output])
 
    
    def model_stack(x):
        from keras import backend as k
        ax= len(x[0].shape) -1
        return k.stack(x, axis =ax  )
    input_stacked = Lambda( model_stack, name ="input_features")(model_outputs)
    
    if text_array_length > 0:
        # include text embeddings
        input_stacked = Concatenate(axis=1, name ="input_features_with_text")([input_stacked,rfv_data_text_embedding])
        input_seq_length = len(model_outputs)  + text_array_length  
    else:
        input_seq_length = len(model_outputs) 
  
    
    #attention layer
    att_layer = attention_layer.get_attention_layer(input_stacked, input_seq_length,att_l2=att_l2)


    x = Dense(units= n_units  ,  kernel_regularizer=kr.l2(l2), kernel_initializer='he_normal',
              activation='relu')(att_layer)
    for i in range (1, n_layers):
        x = Dense(units= n_units ,   kernel_regularizer=kr.l2(l2),kernel_initializer='he_normal',
                  activation='relu')(x)

    if co_model:
        #Critical Outcomes target
        model_output = Dense(units=1,  kernel_initializer=  'glorot_normal', activation='sigmoid')(x)    
        model = Model(inputs=input_list, outputs=model_output)   
        model.compile(loss='binary_crossentropy', # Cross-entropy
                    optimizer= 'nadam'  , 
                    metrics=['accuracy']) # Accuracy performance metric
    else:
        #Resource target
        model_output = Dense(units=3,  kernel_initializer=  'glorot_normal', activation='softmax')(x)    
        model = Model(inputs=input_list, outputs=model_output)   
        model.compile(loss='categorical_crossentropy', # Cross-entropy
                    optimizer= 'nadam'  , 
metrics=['accuracy']) # Accuracy performance metric

    return model

def train_full_model (X_train_list, y_train, num_epochs, l2, n_units, apply_attention,
                embedding_nh,  n_layers,
                input_text_length, vocab_size, att_l2, verbose = True ):
    #class weight
    class_weight_v = class_weight.compute_class_weight('balanced', np.unique(y_train), y_train)
    class_weight_dict = dict(enumerate(class_weight_v))
    #train model
    cdc_model= create_model(l2,n_units,apply_attention,
                            embedding_nh,  n_layers,
                            input_text_length, vocab_size,att_l2=att_l2)
    #print cdc_model.summary()
    cdc_model.fit(X_train_list, # Features
                      y_train, # Target vector
                      epochs=num_epochs, # Number of epochs
                      verbose=verbose, # Print description after each epoch
                      batch_size=1024,   
                      class_weight=class_weight_dict)
    return cdc_model
    
def train_model(X_train_list, y_train,X_dev_list, y_dev, num_epochs, l2=0.001, n_units=100, apply_attention=False,
                embedding_nh=30,  n_layers =2,
                input_text_length=0, vocab_size=0, att_l2=0.0001, verbose = True ):
    #class weight
    class_weight_v = class_weight.compute_class_weight('balanced', np.unique(y_train), y_train)
    class_weight_dict = dict(enumerate(class_weight_v))
    #train model
    cdc_model= create_model(l2,n_units,apply_attention,
                            embedding_nh,  n_layers,
                            input_text_length, vocab_size,att_l2=att_l2)
    #print cdc_model.summary()
    cdc_model.fit(X_train_list, # Features
                      y_train, # Target vector
                      epochs=num_epochs, # Number of epochs
                      verbose=verbose, # Print description after each epoch
                      batch_size=1024, # Number of observations per batch 512
                      validation_data=(X_dev_list, y_dev),
                      class_weight=class_weight_dict)
    y_pred = cdc_model.predict(X_dev_list, batch_size=100)
    fpr, tpr, thresholds = metrics.roc_curve(np.array(y_dev),y_pred, pos_label = 1)
    roc_auc = metrics.auc(fpr, tpr)
    print("%s: %.2f%%" % ("AUROC", roc_auc*100))
    return roc_auc, cdc_model


def cross_Validation (nepochs, predictors, target,l2=0.005,units_n = 50,apply_attention=False ,
                      embedding_nh=30,  n_layers =2,
                      input_text_length=0, vocab_size=0, att_l2=0.0001, file_name_years = 'yy'):
    seed = np.random.seed(0)
    kfold = StratifiedKFold(n_splits=10, shuffle=True, random_state=seed)
    cvscores = []
    count = 1
    for train, test in kfold.split(predictors, target):
        X_train = get_x_list(predictors.iloc[train])
        X_dev = get_x_list(predictors.iloc[test])
        y_train = target.iloc[train]
        y_dev = target.iloc[test]
        roc, model = train_model (X_train,y_train,X_dev,y_dev,  num_epochs=nepochs, l2=l2, n_units=units_n, 
                                  apply_attention=apply_attention ,
                                  embedding_nh=embedding_nh, n_layers=n_layers,
                                  input_text_length=input_text_length, vocab_size=vocab_size,att_l2=att_l2,
                                  verbose=False) 
        model_name = 'nn'
        if apply_attention:
            model_name += '_att'
        if input_text_length > 0:
            model_name += '_text_emb'
        model_name += '_' + file_name_years 
        model_name = 'models/' + model_name + '_' + str(count) +'.H5'
        #model.save (model_name)
        cvscores.append(roc)
        count += 1
    print("ROC AUC: %.2f%% (+/- %.2f%%)" % (np.mean(cvscores)*100, np.std(cvscores)))
    
def get_x_list(x): 
    def get_rfv_df(x,field):
        rfv_df = pd.DataFrame(x[field].values.tolist(), index= x[field].index)
        #rfv_df = pd.DataFrame(x[field].values.tolist())
        return rfv_df
    rfv1_df= get_rfv_df(x,'RFV1')
    rfv2_df= get_rfv_df(x,'RFV2')
    rfv3_df= get_rfv_df(x,'RFV3')
    #rfv_digits_df =  get_rfv_df(x,'RFV_digit_codes')


    
    input_list = [x['SEX'], x['AGE'],
                  x['ARREMS'],x['MSA'], x['CHF'],x['DIABETES'],
                 x ['Temp_Baseline'], x['Pulse_Baseline'],x['Sys_BP_Baseline'] ,
                  x['Resp_Rate_Baseline'],            x['Oxygen_Sat_Baseline'],
                 x['Hypothermia'], 
            x['Hyperthermia'], 
            x['Bradycardia'], 
            x['Mild_Tachycardia'],
            x['Moderate_Tachycardia'], 
            x['Severe_Tachycardia'], 
            x['Hypotension'], 
            x['Hypertension'], 
            x['Bradypnea'], 
            x['Moderate_Tachypnea'], 
            x['Severe_Tachypnea'], 
            x['Mild_Hypoxia'], 
            x['Severe_Hypoxia'],
            x['Reason_Chest_Pain'],
            x['Reason_Abdominal_Pain'],
            x['Reason_Headache'],
            x['Reason_Shortness_of_Breath'],
            x['Reason_Cough'],
            x['Reason_Nausea_Vomiting'],
            x['Reason_Fever_Chills'],
            x['Reason_Syncope'],
            x['Reason_Dizziness'],
            x['Reason_Psychiatric_Complaint'],
            x['Reason_Nervous_System'],
            x['Reason_Cardiovascular_Other'],
            x['Reason_Ears_Eyes_Complaint'],
        x['Reason_Respiratory_Other'],
        x['Reason_Gastrointestinal_Other'],
        x['Reason_Genitourinary_Other'],
        x['Reason_Skin_Hair_Nails_Complaint'],
        x['Reason_Musculoskeletal_Other'],
        x['Reason_Injury_Poisoning'],
        x['Reason_Other'],
        x['Age_18_30'],
     x['Age_31_40'],
     x['Age_41_50'],
     x['Age_51_60'],
     x['Age_61_70'],
     x['Age_71_80'],
     x['Age_81_Above'],                  
     #x['2009_year']  ,
     #x['2010_year']  ,  
     #x['2011_year']  ,  
     #x['2012_year']  ,  
     #x['2013_year']  , 
     #x['2014_year']  ,  
     #x['2015_year'], 
     rfv1_df, rfv2_df,rfv3_df]
    
    if 'RFV4'  in x:
        rfv4_df= get_rfv_df(x,'RFV4')
        input_list.append(rfv4_df)
    if 'RFV5'  in x:
        rfv5_df= get_rfv_df(x,'RFV5')
        input_list.append(rfv5_df)
           
    if 'RFV_data' in x:
        rfv_data_df = get_rfv_df(x,'RFV_data')
        input_list.append(rfv_data_df)
   

                          
    return input_list

def FNN_TE_ATT_model_training(config, filename):
    processedDirectory = config['dataDirectory'] + config['processedDirectory']
    cdc_input = pd.read_csv(processedDirectory + filename  )
    predictors, target = build_features.get_features(cdc_input, with_features_for_Embedding=True)
    predictors, max_seq_length, MAX_VOCAB, tokenizer =  RFV_text_vectorizing.vectorize_RFV_text (predictors,  debug=False)
    cross_Validation (40, predictors, target,l2=0.0001,units_n = 50,apply_attention= True,
                              embedding_nh=50,   n_layers =3, att_l2=0.0001,
                             input_text_length=max_seq_length,  vocab_size=MAX_VOCAB)

## for resources
#-----------------------------------------------------------------------
def train_RSS_model(X_train_list, y_train,X_dev_list, y_dev, num_epochs, l2=0.001, n_units=100, apply_attention=False,
                embedding_nh=30,  n_layers =2,
                input_text_length=0, vocab_size=0, att_l2=0.0001, verbose = True ):


    encoder = LabelEncoder()
    encoder.fit(y_train)
    encoded_Y = encoder.transform(y_train)
    # convert integers to dummy variables (i.e. one hot encoded)
    dummy_y = np_utils.to_categorical(encoded_Y)

    encoder = LabelEncoder()
    encoder.fit(y_dev)
    encoded_Y = encoder.transform(y_dev)
    # convert integers to dummy variables (i.e. one hot encoded)
    dev_y = np_utils.to_categorical(encoded_Y)

    #class weight
    class_weight_v = class_weight.compute_class_weight('balanced', np.unique(dummy_y[0]), dummy_y[0])
    class_weight_dict = dict(enumerate(class_weight_v))
    #train model
    cdc_model= create_model(l2,n_units,apply_attention,
                            embedding_nh,  n_layers,
                            input_text_length, vocab_size,att_l2=att_l2, co_model=False)
    #print cdc_model.summary()
    cdc_model.fit(X_train_list, # Features
                      dummy_y, # Target vector
                      epochs=num_epochs, # Number of epochs
                      verbose=verbose, # Print description after each epoch
                      batch_size=1024, # Number of observations per batch 512
                      validation_data=(X_dev_list, dev_y))
    y_pred = cdc_model.predict(X_dev_list, batch_size=100)
    fpr, tpr, thresholds = metrics.roc_curve(np.array(dev_y[:,0]),y_pred[:,0], pos_label = 1)
    roc_auc = [0.,0.,0.,0.]
    roc_auc[0] = metrics.auc(fpr, tpr)
    r = roc_auc[0]
    print("%s: %.2f%%" % ("AUROC[0]", roc_auc[0]*100))
    
    fpr, tpr, thresholds = metrics.roc_curve(np.array(dev_y[:,1]),y_pred[:,1], pos_label = 1)
    roc_auc[1] = metrics.auc(fpr, tpr)
    r += roc_auc[1]
    print("%s: %.2f%%" % ("AUROC[1]", roc_auc[1]*100))
    
    fpr, tpr, thresholds = metrics.roc_curve(np.array(dev_y[:,2]),y_pred[:,2], pos_label = 1)
    roc_auc[2] = metrics.auc(fpr, tpr)
    r += roc_auc[2]
    print("%s: %.2f%%" % ("AUROC[2]", roc_auc[2]*100))
    
    roc_auc[3] = r/3
    print("%s: %.2f%%" % ("Mean AUROC", roc_auc[3]*100))
    return roc_auc, cdc_model

def train_full_RSS_model(X_train_list, y_train, num_epochs, l2=0.001, n_units=100, apply_attention=False,
                embedding_nh=30,  n_layers =2,
                input_text_length=0, vocab_size=0, att_l2=0.0001, verbose = True ):


    encoder = LabelEncoder()
    encoder.fit(y_train)
    encoded_Y = encoder.transform(y_train)
    # convert integers to dummy variables (i.e. one hot encoded)
    dummy_y = np_utils.to_categorical(encoded_Y)

    #class weight
    class_weight_v = class_weight.compute_class_weight('balanced', np.unique(dummy_y[0]), dummy_y[0])
    class_weight_dict = dict(enumerate(class_weight_v))
    #train model
    cdc_model= create_model(l2,n_units,apply_attention,
                            embedding_nh,  n_layers,
                            input_text_length, vocab_size,att_l2=att_l2, co_model=False)
    #print cdc_model.summary()
    cdc_model.fit(X_train_list, # Features
                      dummy_y, # Target vector
                      epochs=num_epochs, # Number of epochs
                      verbose=verbose, # Print description after each epoch
                      batch_size=1024 # Number of observations per batch 512
           )
   
    return  cdc_model

#-----------------------------------------------------------------------
## batch predict of critical_outcomes and resource utilization 
#-----------------------------------------------------------------------
def batch_predict(modelConfig,fileConfig, fileName):
    # read tokenization values
    with open(modelConfig['tokenizer'], "rb") as f:
        tokenizer = pickle.load(f)
    with open(modelConfig['max_text_length'], "rb") as f:
        max_text_length= pickle.load(f) 
    # read co model
    co_model = load_model(modelConfig['co_model'],custom_objects={'backend': backend})
    # read rss model
    rss_model = load_model(modelConfig['rss_model'],custom_objects={'backend': backend})
    #read file
    fileLocation = fileConfig['dataDirectory'] + fileConfig['processedDirectory'] + fileName
    cdc_file = pd.read_csv(fileLocation)
    print len(cdc_file)
    #Build Features and vectorize words 
    predictors_pre,target,rss = build_features.get_features(cdc_file, with_features_for_Embedding=True,
                                                       with_target=True,with_rss_target=True)
    predictors = RFV_text_vectorizing.vectorize_RFV_text_prediction (predictors_pre, tokenizer,max_text_length)
    #critical outcomes prediction
    X_list = get_x_list(predictors)
    co_pred =co_model.predict(X_list).flatten()
    fpr, tpr, thresholds = metrics.roc_curve(np.array(target),co_pred, pos_label = 1)
    roc_auc = metrics.auc(fpr, tpr)
    print("%s: %.2f%%" % ("Critical Outcome AUROC", roc_auc*100))
    rss_pred = rss_model.predict(X_list)
    original_esi = cdc_file['IMMEDR']
    co_bin = cdc_file.apply(build_features.critical_outcome_binary,axis=1)
    co_type = cdc_file.apply(build_features.get_critical_outcome,axis=1)
    return co_pred, rss_pred , co_bin,co_type, original_esi, rss 

def createPredictionJsonFile (fileConfig,fileName, co_pred, rss_pred , co_bin,co_type, original_esi, rss):
    data = ObjDict()
    data.co_pred = np.float64(co_pred).tolist()
    data.rss_pred= rss_pred.tolist()
    data.ESI = original_esi.tolist()
    data.rss = rss.tolist()
    data.co_bin = co_bin.tolist()
    data.co_type = co_type.tolist()
    json_data = data.dumps()
    fileLocation = fileConfig['dataDirectory'] + fileConfig['resultDirectory'] + fileName
    with open(fileLocation, 'w') as outfile:
        outfile.write(json_data)