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

sys.path.append("../../src/models/predict_model")
import prediction_util
sys.path.append("../../src/features")
import build_features
import RFV_text_vectorizing
sys.path.append("../../src/models/predict_model")
import NN_VE_model




def predict_ESI(c,r):
    #Optimized Thresholds
    ESI1,ESI2=0.89018136, 0.65703756

    if c > ESI1:
        esi = 1
    elif c > ESI2:
        esi = 2
    else:
        if r == 1:
            esi = 4
        
        elif r == 0:
            esi = 5
        else:
            esi = 3
    return esi

def predict_rss(rmax,r0,r1,r2):       
    ESI4 =0.35
    if r1 > ESI4:
        rss = 1
    else:
        rss = rmax
    return rss

def predict(data, tokenizer, max_seq_length, vocabulary, cdc_model, rss_model):

    pd.options.mode.chained_assignment = None  # default='warn'
    pd.set_option('display.max_rows', None)
    pd.options.display.max_columns = None
    
    '''# read tokenization values
    with open("../modeling/ATTNN/models/cdc_2009_att_text_tokenizer.pickle", "rb") as f:
        tokenizer = pickle.load(f)
    with open("../modeling/ATTNN/models/cdc_2009_att_text_max_length.pickle", "rb") as f:
        max_seq_length= pickle.load(f) 
    with open("../modeling/ATTNN/models/cdc_2009_att_text_vocabulary.pickle", "rb") as f:
        vocabulary= pickle.load(f) 


    # read models
    cdc_model = load_model('../modeling/ATTNN/models/cdc_2009_nn_att_text_embedding.H5',custom_objects={'backend': backend})


    rss_model = load_model('models/cdc_rss_2009_nn_att_text_embedding.H5',custom_objects={'backend': backend})
    '''

    sample_record = pd.read_json(data,typ='frame')
    sample_record = sample_record
    try:
        sample_record=sample_record.drop(['RFV5'], axis=1)
        sample_record=sample_record.drop(['RFV4'], axis=1)
    except:
        pass

    #Preprocess data
    reload(build_features)
    reload(RFV_text_vectorizing)
    predictors_pre = build_features.get_features(sample_record, with_features_for_Embedding=True, with_target=False)
    
    predictors = RFV_text_vectorizing.vectorize_RFV_text_prediction (predictors_pre, tokenizer,max_seq_length)

    
    #Optimized Thresholds
    ESI1,ESI2,ESI4 =0.89018136, 0.65703756, 0.35

    #predictions
    X_list = NN_VE_model.get_x_list(predictors)
    y_pred =cdc_model.predict(X_list).flatten()

    X_list2 = NN_VE_model.get_x_list(predictors)
    y_rss = rss_model.predict(X_list)

    #Apply ESI predictors

    rss_max = [np.argmax(r) for r in y_rss]
    predicted_rss = predict_rss(rss_max,y_rss[0,0],y_rss[0,1],y_rss[0,2])[0]
    predicted_ESI = predict_ESI(y_pred[0],predicted_rss)

    #Interpretability

    #get features and attention weights from the models

    reload(prediction_util)
    feature_importance_df, feature_name_list, attention_weights   = \
    prediction_util.get_feature_importance (cdc_model,X_list,sample_record,predictors)
    text_embeddings_start_post = len(feature_name_list)

    rss_feature_importance_df, rss_feature_name_list, rss_attention_weights   = \
    prediction_util.get_feature_importance (rss_model,X_list,sample_record,predictors)
    rss_text_embeddings_start_post = len(rss_feature_name_list)

    TOP = 15
    feature_importance_sorted = feature_importance_df.sort_values(by=['attention_weight'], ascending=False).head(TOP)
    min_weight = feature_importance_sorted.iloc[TOP-1]["attention_weight"]
    word_heat_map = prediction_util.get_rfv_text_heatmap(tokenizer,predictors, \
                                                         attention_weights,min_weight,text_embeddings_start_post )

    rss_feature_importance_sorted = rss_feature_importance_df.sort_values(by=['attention_weight'], ascending=False).head(TOP)
    rss_min_weight = rss_feature_importance_sorted.iloc[TOP-1]["attention_weight"]
    word_heat_map2 = prediction_util.get_rfv_text_heatmap(tokenizer,predictors, \
                                                         rss_attention_weights,rss_min_weight,
                                                          rss_text_embeddings_start_post )


    #build JSON data
    
    data = ObjDict()
    data.co = np.float64(y_pred[0])
    data.rss= predicted_rss
    data.esi = predicted_ESI
    data.co_fi=feature_importance_df.sort_values(by=['attention_weight'], ascending=False).head(15).to_dict(('records'))
    data.word_heat=word_heat_map.to_dict()
    data.rss_fi=rss_feature_importance_df.sort_values(by=['attention_weight'], ascending=False).head(15).to_dict(('records'))
    json_data = data.dumps()

    return json_data

