import sys
from keras import backend
from keras.models import  Model
from keras import layers
import numpy as np
import pandas as pd
sys.path.append("../modeling/modules/feature_engineering")
import rfv_text_lookup


def get_model_features_weights(cdc_model,X_list, input_feature_layer_name="input_features"):
    attention_layer=cdc_model.get_layer("attention_weights1")
    intermediate_layer_model = Model(inputs=cdc_model.input,
                                 outputs=attention_layer.output)
    attention_weights = intermediate_layer_model.predict(X_list)
    features_layer=cdc_model.get_layer(input_feature_layer_name)
    feature_name_list = []
    for feature in features_layer.input:
        feature_name = feature.name[:feature.name.find ("/")]
        #print feature_name 
        index1 = feature_name.rfind ("_")
        if index1 >=0:
            tag = feature_name[index1 +1:]
            if tag.isdigit():
                feature_name = feature_name[:index1]
                #print feature_name
        feature_name_list.append(feature_name )
    return feature_name_list, attention_weights

def  get_desc (feature_name, value):
    if feature_name == "reason1_for_visit" or feature_name == "reason2_for_visit"  \
        or feature_name == "reason3_for_visit" or feature_name == "reason4_for_visit" \
        or feature_name == "reason5_for_visit":
        desc_value = rfv_text_lookup.RFVtext(int(value))
        if desc_value == "other":
            desc_value = ""
        value = value + ": " + desc_value
        
    if feature_name == "arrival_model":
        feature_name = "arrival_mode"
        if value == '1':
            desc_value = "by ambulance"
        else:
            desc_value = "NOT by ambulance"
        value = value + ": " + desc_value
        
    if feature_name == "sex_indicator":
        if value == '1':
            desc_value = 'female'
        else:
            desc_value = 'male'
        value = value + ": " + desc_value
    return feature_name, value
    

def get_related_input_values(feature_name_list, record,predictor_record):
    rfv_list = []
    for rfv in ['RFV1','RFV2','RFV3','RFV4','RFV5']:
        if rfv in record.keys() and record[rfv] != -9:
            rfv_list.append(int(record[rfv]))
    field_name_list =[]
    value_list=[]
    df_field_lookup = get_field_lookup() 
    for feature_name in feature_name_list:
        input_field_name = df_field_lookup[feature_name]
        if input_field_name in record.keys():
            value = record[input_field_name]  
        elif input_field_name in predictor_record.keys():
            value = predictor_record[input_field_name] 
        else:
            value = predictor_record[feature_name]
        
        if value == -9:
            value = None
        else: 
            value = str(int(value))
            feature_name, value = get_desc(feature_name, value)
        value_list.append(value)        
        field_name_list.append(feature_name)

    return field_name_list, value_list 

def get_rfv_text_heatmap(tokenizer,predictors, attention_weights,min_weight,text_embeddings_start_post ):
    #get weights for words text
    attention_weights_for_text =  attention_weights[0][text_embeddings_start_post:]
    reverse_word_map = dict(map(reversed, tokenizer.word_index.items()))
    # get list of words
    text_index_list = predictors.iloc[0]['RFV_data']
    word_list =[]
    for index in text_index_list:
        if index == 0:
            break
        word_list.append(reverse_word_map[index])
    # get weights for each word
    word_list_weight = attention_weights_for_text [0:len(word_list)]
    word_list = word_list[1:len(word_list)-1] 
    word_list_weight = word_list_weight [1:len(word_list_weight)-1] 
    word_heat_map = pd.DataFrame()
    for i in range(0,len(word_list)):
        high_weight_in = " "
        if word_list_weight[i] > min_weight:
            high_weight_in ="*"
        word_heat_map["pos_"+ str(i+1)] = [word_list[i], word_list_weight[i],high_weight_in ]
    return word_heat_map

def get_feature_importance (cdc_model,X_list,sample_record,predictors):
    #get features and attention weights from the model
    feature_name_list, attention_weights = get_model_features_weights(cdc_model,X_list)
    list_length = len(feature_name_list)
    #get related values from the input 
    record = sample_record.iloc[0]
    predictor_record = predictors.iloc[0]                            
    field_name_list, value_list = get_related_input_values(feature_name_list,record, predictor_record)
    weights_list_f1 = attention_weights[0][0:list_length]
    #build dataframe 
    feature_importance_df  = pd.DataFrame({'featureName': feature_name_list, 'attention_weight': weights_list_f1,
                                      'input_value':value_list })
    return feature_importance_df,feature_name_list, attention_weights 

def get_field_lookup():
   return {"sex_indicator":"SEX",  "arrival_model":"ARREMS",
"msa_indicator":"MSA",
"chf_indicator":"CHF",
"diabetes_indicator":"DIABETES",
"Age":"AGE",
"Temperature":"TEMPF",
"Pulse_Heart_rate":"PULSE",
"Systolic_blood_pressure":"BPSYS",
"Respiratory_rate":"RESPR",
"Oxygen_Saturation":"POPCT",
"reason1_for_visit":"RFV1",
"reason2_for_visit":"RFV2",
"reason3_for_visit":"RFV3",
"reason4_for_visit":"RFV4",
"reason5_for_visit":"RFV5",
"Hypothermia":"Hypothermia",
"Hyperthermia":"Hyperthermia",
"Bradycardia":"Bradycardia",
"Mild_Tachycardia":"Mild_Tachycardia",
"Moderate_Tachycardia":"Moderate_Tachycardia",
"Severe_Tachycardia":"Severe_Tachycardia",
"Hypotension":"Hypotension",
"Hypertension":"Hypertension",
"Bradypnea":"Bradypnea",
"Moderate_Tachypnea":"Moderate_Tachypne",
"Severe_Tachypnea":"Severe_Tachypnea",
"Mild_Hypoxia":"Mild_Hypoxia",
"Severe_Hypoxia":"Severe_Hypoxia",
"Reason_Chest_Pain":"RFV",
"Reason_Abdominal_Pain":"RFV",
"Reason_Headache":"RFV",
"Reason_Shortness_of_Breath":"RFV",
"Reason_Cough":"RFV",
"Reason_Nausea_Vomiting":"RFV",
"Reason_Fever_Chills":"RFV",
"Reason_Syncope":"RFV",
"Reason_Dizziness":"RFV",
"Reason_Psychiatric_Complaint":"RFV",
"Reason_Nervous_System":"RFV",
"Reason_Cardiovascular_Other":"RFV",
"Reason_Ears_Eyes_Complaint":"RFV",
"Reason_Respiratory_Other":"RFV",
"Reason_Gastrointestinal_Other":"RFV",
"Reason_Genitourinary_Other":"RFV",
"Reason_Skin_Hair_Nails_Complaint":"RFV",
"Reason_Musculoskeletal_Other":"RFV",
"Reason_Injury_Poisoning":"RFV",
"Reason_Other":"RFV",
"Age_18_30_range":"Age_18_30",
"Age_31_40_range":"Age_31_40",
"Age_41_50_range":"Age_41_50",
"Age_51_60_range":"Age_51_60",
"Age_61_70_range":"Age_61_70",
"Age_71_80_range":"Age_71_80",
"Age_81_Above":"Age_81_Above",
"year_2009_indicator":"2009_year",
"year_2010_indicator":"2010_year",
"year_2011_indicator":"2011_year",
"year_2012_indicator":"2012_year",
"year_2013_indicator":"2013_year",
"year_2014_indicator":"2014_year",
"year_2015_indicator":"2015_year"}