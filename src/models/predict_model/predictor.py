#adapted from prediction notebook by Zenobia, added RSS pieces
import pandas as pd
import numpy as np
import random
import pickle
import sys
from keras.models import load_model
from keras import backend
import simplejson as json
from objdict import ObjDict

import predict_esi
sys.path.append("../../src/models/predict_model")
import prediction_util
sys.path.append("../../src/features")
import build_features
import RFV_text_vectorizing
sys.path.append("../../src/models/predict_model")
import NN_VE_model

def predict_and_get_att(modelConfig,thresholdsConfig,  att_top, sample_record):
    # read tokenization values
    with open(modelConfig['tokenizer'], "rb") as f:
        tokenizer = pickle.load(f)
    with open(modelConfig['max_text_length'], "rb") as f:
        max_text_length= pickle.load(f) 
    # read co model
    co_model = load_model(modelConfig['co_model'],custom_objects={'backend': backend})
    # read rss model
    rss_model = load_model(modelConfig['rss_model'],custom_objects={'backend': backend})
    #Build Features and vectorize words 
    predictors_pre,target,rss = build_features.get_features(sample_record, with_features_for_Embedding=True,
                                                       with_target=True,with_rss_target=True)
    predictors = RFV_text_vectorizing.vectorize_RFV_text_prediction (predictors_pre, tokenizer,max_text_length)
    #critical outcomes and resources prediction
    X_list = NN_VE_model.get_x_list(predictors)
    co_pred =co_model.predict(X_list).flatten()
    rss_pred = rss_model.predict(X_list)
    
    #Optimized Thresholds
    RSS_threshold = thresholdsConfig['rss_threshold']
    ESI1 =thresholdsConfig['esi1_threshold']
    ESI2 = thresholdsConfig['esi2_threshold']

    #Apply ESI predictors  
    pred_rss = predict_esi.predict_resources (rss_pred, RSS_threshold)
    pred_ESI = predict_esi.get_new_esi(rss_pred,co_pred,RSS_threshold,ESI1, ESI2)

    #Interpretability

    #get features and attention weights from the models

    feature_importance_df, feature_name_list, attention_weights   = \
    prediction_util.get_feature_importance (co_model,X_list,sample_record ,predictors)
    text_embeddings_start_post = len(feature_name_list)

    rss_feature_importance_df, rss_feature_name_list, rss_attention_weights   = \
    prediction_util.get_feature_importance (rss_model,X_list,sample_record,predictors)
    rss_text_embeddings_start_post = len(rss_feature_name_list)

    co_feature_importance = feature_importance_df.sort_values(by=['attention_weight'], ascending=False).head(att_top)
    min_weight = co_feature_importance.iloc[att_top-1]["attention_weight"]
    co_word_heat_map = prediction_util.get_rfv_text_heatmap(tokenizer,predictors, \
                                                         attention_weights,min_weight,text_embeddings_start_post )

    rss_feature_importance = rss_feature_importance_df.sort_values(by=['attention_weight'], ascending=False).head(att_top)
    rss_min_weight = rss_feature_importance.iloc[att_top-1]["attention_weight"]
    rss_word_heat_map = prediction_util.get_rfv_text_heatmap(tokenizer,predictors, \
                                                         rss_attention_weights,rss_min_weight,
                                                          rss_text_embeddings_start_post )
    return co_pred, pred_rss, pred_ESI, co_feature_importance, co_word_heat_map, rss_feature_importance, rss_word_heat_map

def predict(modelConfig,thresholdsConfig, json_data, att_top):
    
    # converting from json to dataframe
    sample_record = pd.read_json(json_data,typ='frame')
    
    # getting probabilities predicted and co_model for interpretability
    co_pred, pred_rss, pred_esi, co_feature_importance, co_word_heat_map, rss_feature_importance, rss_word_heat_map =  \
        predict_and_get_att(modelConfig,thresholdsConfig,  att_top, sample_record)
    
    #build JSON data    
    data = ObjDict()
    data.co = np.float64(co_pred[0])
    data.rss= pred_rss
    data.esi = pred_esi
    data.co_fi=co_feature_importance.to_dict(('records'))
    data.word_heat=co_word_heat_map.to_dict()
    data.rss_fi=rss_feature_importance.to_dict(('records'))
    json_data = data.dumps()

    return json_data

