import numpy as np
import sys 
sys.path.append("../../src/models/predict_model")
import predict_esi

def countX(lst, x):
    return lst.count(x)
 
def get_esi_counts(ESI, new_esi):
    categories = [1, 2, 3, 4, 5]
    old_counts = []
    new_counts = []
    for c in categories:
        old_counts.append(countX(ESI, c))
        new_counts.append(countX(new_esi, c))
    return old_counts, new_counts


def show_tp_fp_rates( cdc_info):
    #Get baseline true positive rate
    true_co_cases = cdc_info.loc[cdc_info['co_type'] != 'None']
    base_true_pos = 100*(((true_co_cases['ESI'] == 1).sum() + \
                      (true_co_cases['ESI'] == 2).sum())\
                     / (1.0 *len(true_co_cases['ESI'])))
    print('Baseline true positive rate: %f' % base_true_pos + '%')

    #Get true positive rate
    true_pos = 100*(((true_co_cases['new_esi'] == 1).sum() + \
                 (true_co_cases['new_esi'] == 2).sum())\
                /(1.0 *len(true_co_cases['new_esi'])))
    print('True positive rate: %f' % true_pos + '%')

    #Get baseline false positive rate
    non_co_cases = cdc_info.loc[cdc_info['co_type'] == 'None']
    base_false_pos = 100*(((non_co_cases['ESI'] == 1).sum() + \
                       (non_co_cases['ESI'] == 2).sum())
                      / (1.0* len(non_co_cases['ESI'])))
    print('Baseline false positive rate: %f' % base_false_pos + '%')

    #Get false positive rate
    false_pos = 100*(((non_co_cases['new_esi'] == 1).sum() + \
                  (non_co_cases['new_esi'] == 2).sum())\
                 /(1.0*len(non_co_cases['new_esi'])))
    print('False positive rate: %f' % false_pos + '%')
    
def show_co_caught_counts(cdc_info):
    cdc_co = cdc_info.loc[cdc_info['co_bin'] == 1]
    CO_esi = cdc_co.groupby([ 'ESI']).size().reset_index(name='original_esi_counts')
    CO_new_esi = cdc_co.groupby([ 'new_esi']).size().reset_index(name='idann_esi_counts')
    CO_esi_compare =CO_esi.set_index('ESI').join(CO_new_esi.set_index('new_esi'))
    print CO_esi_compare
    print 'number of critical outcomes: ', len (cdc_co)
    original_co_caught =CO_esi_compare.loc[[1]]['original_esi_counts'].item() + \
                         CO_esi_compare.loc[[2]]['original_esi_counts'].item()
    print 'original critical outcomes identified:' , original_co_caught
    original_co_caught =CO_esi_compare.loc[[1]]['idann_esi_counts'].item() + \
                         CO_esi_compare.loc[[2]]['idann_esi_counts'].item()
    print 'IDANN critical outcomes identified:' , original_co_caught
