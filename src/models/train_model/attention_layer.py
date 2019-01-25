from keras.layers import Dense,  Input
from keras.layers import  Merge,TimeDistributed
from keras.layers.merge import Concatenate
from keras.layers.core import *
from keras.layers import merge, dot, add
from keras import backend as K
# based on paper: Hierarchical Attention networks for document classification
# starting code from:
# https://groups.google.com/forum/#!msg/keras-users/IWK9opMFavQ/AITppppfAgAJ

# note: there is a lot of sample codes in the internet that do not work, and their authors do mention that, 
# they don't see a difference when applying the attention mechanism
#
# I did have to review closely the formulas presented on the papers about Attention to figure it out what type of
# code will actually work
#
# Author: Zenobia Liendo

def get_attention_layer(inputs,  input_seq_length, att_l2= 0.001, i='1'):

    #(1) u_it: we first feed the word annotation through a one-layer MLP to get the hidden representation u_it
    #inputs= Dropout(0.5)(inputs)
    u_it = TimeDistributed(Dense(1, #kernel_initializer=  'he_normal' this is for relu
                                 activation='tanh', #'relu',
                                 kernel_regularizer=regularizers.l2(att_l2),
                                 name='u_it'+i))(inputs)

    #u_it= Dropout(0.5)(u_it)
    # (2) alpha_it: then we measure the importance of x as the similarity of u_it with a x level
    # context vector u_w and get a normalized importance weight alpha_it through a softmax function
    #alpha_it  = TimeDistributed(Dense(TIME_STEPS, activation='softmax',use_bias=False))(u_it)
    #att = TimeDistributed(Dense(1,  kernel_regularizer=regularizers.l2(att_l2), bias=False))(u_it)                         
    att = Reshape((input_seq_length,))( u_it)                                                       
    att_weights = Activation('softmax', name='attention_weights'+i)(att) 

    
    # (3) a context vector ct as the weighted mean of the state sequence h, using att weights
    context_vector =merge([att_weights, inputs], mode='dot', dot_axes=(1,1), name='context_vector_c'+i) 
    
    
    return context_vector

