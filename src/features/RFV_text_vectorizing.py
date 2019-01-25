from keras.preprocessing.sequence import pad_sequences
from keras.preprocessing.text import Tokenizer
import numpy as np


def set_RFV_text(x):
    text = ""
    if x['RFV1_text'] != 'blank entry':
        text += "<s> " +x['RFV1_text']  + " <s>"
    if x['RFV2_text'] != 'blank entry':
        text += "<s> " +x['RFV2_text']  + " <s>"
    if x['RFV3_text'] != 'blank entry':
        text += "<s> " +x['RFV3_text']  + " <s>"
    if 'RFV4_text' in x and x['RFV4_text'] !='blank entry':
        text += "<s> " +x['RFV4_text']  + " <s>"
    if 'RFV5_text' in x and x['RFV5_text'] != 'blank entry':
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
    data = pad_sequences(data, maxlen = MAX_SEQ_LENGTH,  padding='post')
    return data

def vectorize_RFV_text (predictors, debug=False, in_predictors = True):
    # append all RFVn_text  into RFV_text
    predictors['RFV_text'] = predictors.apply(set_RFV_text, axis=1)
    predictors =predictors.drop(['RFV1_text','RFV2_text','RFV3_text',
                                 'RFV4_text','RFV5_text'], axis=1,errors='ignore')
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
    
    if in_predictors:
        predictors['RFV_data'] =rfv_data.tolist()
        return  predictors,  max_seq_length, MAX_VOCAB,  tokenizer 
    else:
        return predictors, rfv_data,  max_seq_length, MAX_VOCAB,  tokenizer

#------------------------------------------------------------------------------------
# For Prediction
#------------------------------------------------------------------------------------
def vectorize_RFV_text_prediction(predictors, tokenizer,max_length):
    predictors['RFV_text'] = predictors.apply(set_RFV_text, axis=1)
    predictors =predictors.drop(['RFV1_text','RFV2_text','RFV3_text',
                                 'RFV4_text','RFV5_text'], axis=1, errors='ignore')
    rfv_data_vectorized = tokenizer.texts_to_sequences( predictors['RFV_text'])  
    rfv_data = pad_rfv_text(rfv_data_vectorized, max_length)
    predictors =predictors.drop(['RFV_text'], axis=1)
    predictors['RFV_data'] =rfv_data.tolist()
    return predictors
