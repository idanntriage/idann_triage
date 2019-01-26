import numpy as np
from collections import Counter 
import pandas as pd



def predict_ESI(c,r,ESI1, ESI2):

    if c > ESI1:
        ESI = 1
    elif c > ESI2:
        ESI = 2
    else:
        if r == 1:
            ESI = 4        
        elif r == 0:
            ESI = 5
        else:
            ESI = 3
    return ESI

def get_new_esi(rss_pred,co_pred,RSS_threshold,ESI1, ESI2):
    rss_p = predict_resources (rss_pred, RSS_threshold)
    new_esi = []
    for i in range(len(co_pred)):
        new_esi.append(predict_ESI(co_pred[i],rss_p[i],ESI1, ESI2))
    return new_esi

def predict_resources (rss_pred, RSS_threshold):
    rss_max = [np.argmax(r) for r in rss_pred]
    rss_comp = np.column_stack((rss_max,rss_pred))
    rss_p = [predict_rss(rmax,r0,r1,r2, RSS_threshold) for rmax,r0,r1,r2 in rss_comp]
    return rss_p 
    

def predict_rss(rmax,r0,r1,r2, RSS_threshold):       
    if r1 >RSS_threshold:# and rmax==0:
        rss = 1
    else:
        rss = rmax
    return rss



def print_distribution (co_pred,co_type, ESI,  threshold_top_10_perc ):
    #Define ESI 1 and 2, and examine critical outcomes within that group
    esi_1_2_flag = []

    for i in range(len(co_pred)):
        if co_pred[i] >= threshold_top_10_perc:# this was a hardcoded value: 0.717968, where it camem from?
            esi_1_2_flag.append(1)
        else:
            esi_1_2_flag.append(0)
    
    #looks like about 10% of cases have successfully made it into this flag
    print  ('mean of esi_1_2_flag: ', np.mean(esi_1_2_flag))

    #Distribution of CO type

    co_type_esi_1_2=[]
    for i in range(len(co_pred)):
        if co_pred[i] >= threshold_top_10_perc: # harcoded value was here 0.717968:
            co_type_esi_1_2.append(co_type[i])
        else:
            pass
    print('CO type for co_pred in potential esi 1 and 2:', Counter(co_type_esi_1_2))

    
    #Distribution of ESI
    old_esi_esi_1_2=[]
    for i in range(len(co_pred)):
        if co_pred[i] >= threshold_top_10_perc: # harcoded value was here 0.717968:
            old_esi_esi_1_2.append(ESI[i])
        else:
            pass
    print('Assigned ESI for co_pred in potential esi 1 and 2:', Counter(old_esi_esi_1_2))
    print '-' * 50
    print pd.crosstab(pd.Series(co_type_esi_1_2), pd.Series(old_esi_esi_1_2))
    print '-' * 50
    
def get_threshold_top_n_perc (co_pred, top_n):
    co_pred_sorted= sorted(range(len(co_pred)), key=lambda i: co_pred[i], reverse=True)
    top_n_perc = co_pred_sorted[0:int(len(co_pred)*top_n)]
    bottom_perc = co_pred_sorted[int(len(co_pred)*top_n)+1 : len(co_pred_sorted)]

    highest_prob = co_pred[top_n_perc[0]]
    threshold_top_n_perc  = co_pred[top_n_perc[len(top_n_perc)-1]]
    print('Top CO probability value: %f' % highest_prob)
    print('Bottom of new ESI 2 range: %f' % threshold_top_n_perc)
    print('Top of new ESI 3 range: %f' % co_pred[bottom_perc[0]])
    print('Bottom CO probability value: %f' % co_pred[bottom_perc[len(bottom_perc)-1]])
    print '-' * 50
    return threshold_top_n_perc, top_n_perc

def get_ESI_thresholds( co_pred, co_type, ESI, rss_p, top_n, esi1_ratio_top_n_perc) :    
    
    threshold_top_n_perc, top_n_perc = get_threshold_top_n_perc (co_pred, top_n)
    print_distribution (co_pred,co_type,ESI, threshold_top_n_perc )
    new_esi_1 = top_n_perc[0:int(len(top_n_perc)*esi1_ratio_top_n_perc)]
    new_esi_2 = top_n_perc[int(len(top_n_perc)*esi1_ratio_top_n_perc)+1 : len(top_n_perc)]

    ESI_1_threshold = co_pred[new_esi_1[len(new_esi_1)-1]]
    ESI_2_threshold = co_pred[new_esi_2[len(new_esi_2)-1]]

    #print('Top CO probability value: %f' % co_pred[new_esi_1[0]])
    print('Bottom of new ESI 1 range: %f' % ESI_1_threshold)
    #print('Top of new ESI 2 range: %f' % co_pred[new_esi_2[0]])
    print('Bottom of new ESI 2 range %f' % ESI_2_threshold)
    print '-' * 50 
    new_esi = []
    for i in range(len(co_pred)):
        new_esi.append(predict_ESI(co_pred[i],rss_p[i],ESI_1_threshold,ESI_2_threshold ))
    
    print('New ESI:', Counter(new_esi))
    return ESI_1_threshold, ESI_2_threshold, new_esi