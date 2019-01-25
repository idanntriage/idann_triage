import pandas as pd
import numpy as np
import age_features
import vital_signs_features
import RFV_features

from keras.preprocessing.sequence import pad_sequences
from keras.preprocessing.text import Tokenizer

def get_base_features (cdc_input,normalize=False,with_features_for_Embedding=False ):
    predictors = pd.DataFrame()
    
    # vital signs and fills missing values with median 
    predictors = vital_signs_features.get_vital_signs(cdc_input, predictors, normalize)
    
    # creates categories for vital signs and RVF (reason for visit) 
    predictors = RFV_features.get_rfv_group_features (cdc_input, predictors)
    predictors = vital_signs_features.get_vital_signs_group_features(cdc_input, predictors)

    # creates age categories
    predictors = age_features.get_age_categories(cdc_input, predictors)
    
    return predictors

def get_baseline_features (cdc_input, normalize=False ):
    # vital signs and fills missing values with median 
    # creates categories for vital signs and RVF (reason for visit) 
    # creates age categories
    predictors = get_base_features (cdc_input , normalize=normalize)  
    # creates categories for sex indicators 
    predictors = get_sex_indicators(cdc_input,predictors)
    # creates categories for arrival mode indicators
    predictors = get_arrival_mode_indicators(cdc_input,predictors)    
    
    target = cdc_input.apply(critical_outcome_binary, axis=1)
    target = target.reset_index(drop=True)
    return predictors, target 

def get_all_features (cdc_input, normalize=False,with_features_for_Embedding = False):
    predictors, target = get_baseline_features(cdc_input,normalize)
    predictors = RFV_features.make_rfv_digit_features (predictors, cdc_input,normalize)
    if with_features_for_Embedding:  
        predictors = RFV_features.get_RFV_text(predictors, cdc_input)
    predictors = add_MSA_feature(predictors, cdc_input)
    predictors = get_medical_history_indicators( cdc_input, predictors)  
    return predictors, target


# used by NN model with attention 
def get_features(cdc_input,with_features_for_Embedding=False, with_target=True,with_rss_target=False):   
    
    predictors, target = get_baseline_features (cdc_input,with_features_for_Embedding )
    
    # Arrival Ambulance mode 
    predictors['ARREMS'] = cdc_input.ARREMS.apply(get_Ambulance_Arrival_index)
    
    # demographics 
    predictors = age_features.get_age_normalize(cdc_input, predictors) 
    predictors['SEX'] =  cdc_input['SEX'] - 1  # to make it binary       
    
    # RFV  Reason for visit codes   
    predictors = RFV_features.get_RFV_features(cdc_input, predictors,with_features_for_Embedding)
    
    # other fields   
    predictors['MSA'] = cdc_input.MSA.apply(get_MSA_index)
    predictors = get_medical_history( cdc_input, predictors)
    #predictors = get_year_ind(cdc_input, predictors)
    
    predictors = predictors.reset_index(drop=True)

    #target
    if with_target:
        target = cdc_input.apply(critical_outcome_binary, axis=1)
        target = target.reset_index(drop=True)
        if with_rss_target:
            rss = cdc_input.apply(get_resources, axis=1)
            rss = rss.reset_index(drop=True) 
            return predictors, target, rss
        else:
            return predictors, target
    else:
        return predictors    
    
    
#-----------------------------------------------------------------------------------------------------
# methods to build individual features
#------------------------------------------------------------------------------------------------------
    
def critical_outcome_binary (x):
    if x['DIEDED'] == 1 or x['HDSTAT'] == 2 or x['ADMIT'] == 1 or x['ADMIT']== 2 or x['ADMIT']== 3 or x['ADMIT']== 5:
        return 1
    else:
        return 0  

def get_critical_outcome (x):
    if x['DIEDED'] == 1 or x['HDSTAT'] == 2:
        return 'Mortality'
    elif x['ADMIT'] == 1 or x['ADMIT'] == 2 :
        return 'ICU'
    elif x['ADMIT']== 3 or x['ADMIT']== 5:
        return'OR_CATH'
    else:
        return 'None' 

# MSA indicators
#--------------------------------
def get_MSA_index(i): 
    if i == -9 :
        return 0
    else:
        return i 

def add_MSA_feature(predictors, cdc_input): 
    # Metropolitean Statistical Area 
    def MSA_1(i):
        return 1 if i == 1 else 0
    def MSA_2(i):
        return 1 if i == 2 else 0
    predictors['MSA_1'] = cdc_input.MSA.apply(MSA_1)
    predictors['MSA_2'] = cdc_input.MSA.apply(MSA_2)
    return predictors
# Medical History
#--------------------------------------

def get_diabetes_1(x):
        if "DIABTYP0" in x:        
            if x.DIABETES == 1 or x.DIABTYP0 == 1 or  x.DIABTYP1 == 1 or x.DIABTYP2 == 1:
                return 1
            else:
                return 0
        else:
            if x.DIABETES == 1:
                return 1
            else:
                return 0
def get_diabetes_0(x):
        if "DIABTYP0" in x: 
            if x.DIABETES == 0 :
                return 1
            elif x.DIABETES == -9 and ( x.DIABTYP0 == 0 and  x.DIABTYP1 == 0 and x.DIABTYP2 == 0):
                return 1 
            else:
                return 0 
        else:
            if x.DIABETES == 0:
                return 1
            else:
                return 0  
            
def get_diabetes_1(x):
        if "DIABTYP0" in x:        
            if x.DIABETES == 1 or x.DIABTYP0 == 1 or  x.DIABTYP1 == 1 or x.DIABTYP2 == 1:
                return 1
            else:
                return 0
        else:
            if x.DIABETES == 1:
                return 1
            else:
                return 0
            
def get_medical_history_indicators( cdc_input, predictors):
    predictors['CHF'] = cdc_input['CHF']    
    predictors['DIABETES_1'] = cdc_input.apply(get_diabetes_1, axis=1)
    predictors['DIABETES_0'] = cdc_input.apply(get_diabetes_0, axis=1)
    return predictors

def get_medical_history( cdc_input, predictors):
    predictors['DIABETES'] = cdc_input.apply(get_diabetes_1, axis=1)
    predictors['CHF']= cdc_input['CHF'] 
    return predictors 

# year indicators
#----------------------------------------------------------------
def get_year_ind(cdc_input, predictors):
     # indicators for year
    def year_2009(i):
        return 1 if i == 2009 else 0
    def year_2010(i):
        return 1 if i == 2010 else 0
    def year_2011(i):
        return 1 if i == 2011 else 0
    def year_2012(i):
        return 1 if i == 2012 else 0
    def year_2013(i):
        return 1 if i == 2013 else 0
    def year_2014(i):
        return 1 if i == 2014 else 0
    def year_2015(i):
        return 1 if i == 2015 else 0

    predictors['2009_year'] = cdc_input.VYEAR.apply(year_2009)
    predictors['2010_year'] = cdc_input.VYEAR.apply(year_2010)
    predictors['2011_year'] = cdc_input.VYEAR.apply(year_2011)
    predictors['2012_year'] = cdc_input.VYEAR.apply(year_2012)
    predictors['2013_year'] = cdc_input.VYEAR.apply(year_2013)
    predictors['2014_year'] = cdc_input.VYEAR.apply(year_2014)
    predictors['2015_year'] = cdc_input.VYEAR.apply(year_2015)
    return predictors




#Sex 
#---------------------------------------------------
def Male_Flag(i):
    if i==2:
        return 1
    else:
        return 0

def Female_Flag(i):
    if i==1:
        return 1
    else:
        return 0
    
def get_sex_indicators(cdc_input,predictors):
    predictors['Male_Flag'] = cdc_input.SEX.apply(Male_Flag)
    predictors['Female_Flag'] = cdc_input.SEX.apply(Female_Flag)  
    return predictors

#Mode of arrival: ambulance
#-------------------------------------------------------

def get_Ambulance_Arrival_index(i):
    if i==1 or i ==2:
        return i -1
    elif  i== -8:
        return 2
    else:
        return 3
    
def Ambulance_Arrival(i):
    if i==1:
        return 1
    else:
        return 0
def Other_Arrival(i):
    if i==2:
        return 1
    else:
        return 0
def Unknown_Arrival(i):
    if i==-9 or i==-8:
        return 1
    else:
        return 0
def get_arrival_mode_indicators(cdc_input,predictors):
    predictors['Ambulance_Arrival'] = cdc_input.ARREMS.apply(Ambulance_Arrival)
    predictors['Other_Arrival'] = cdc_input.ARREMS.apply(Other_Arrival)
    predictors['Unknown_Arrival'] = cdc_input.ARREMS.apply(Unknown_Arrival) 
    return predictors

# calculate number of resources 
# --------------------------------------------------------
#Calculte RSS required
def get_resources (x):
    #rss = None
    rss = 0
    temp = 0
    fields = ['DIAGSCRN','CBC','BUNCREAT','CARDENZ','ELECTROL','GLUCOSE','LFT','ABG','PTTINR','BLOODCX','BAC','OTHERBLD','CARDMON','EKG','HIVTEST','FLUTEST',
        'PREGTEST','TOXSCREN','URINE','WOUNDCX','OTHRTEST','ANYIMAGE','XRAY','CATSCAN','CTHEAD','CTNHEAD','CTNUNK','MRI','ULTRASND','OTHIMAGE','PROC',
        'IVFLUIDS','CAST','SPLINT','SUTURE','INCDRAIN','FBREM','NEBUTHER','BLADCATH','PELVIC','CENTLINE','CPR','ENDOINT','OTHPROC','PREGTEST','URINE','INCDRAIN',
        'PELVIC','BNP','DDIMER','LACTATE','URINECX','IVCONTRAST','CTAB','CTCHEST','BPAP','CASTSPLINT','LUMBAR','SKINADH','DIAGSCRN','ABG','BAC','BUNCREAT','CARDENZ',
        'CBC','ELECTROL','PTTINR','URINECX','CATSCAN','CTAB','CTCHEST','CTOTHER','CTUNK','CTCONTRAST','MRI','MRICONTRAST','PROC','BPAP','BMP','CMP','TRTCX','OTHCX']
    for i in fields:
        try:

            if x[i] == -9:
                x[i]=0
        except:
            pass

    #diagnostic resources
    if x['TOTDIAG'] <> -9:
        temp = x['CBC']+x['BUNCREAT']+x['CARDENZ']+x['ELECTROL']+x['GLUCOSE']+\
        x['LFT']+x['ABG']+x['PTTINR']+x['BLOODCX']+x['BAC']+x['OTHERBLD']
        if temp > 0:
            temp = 1
        temp = temp + x['CARDMON']+ x['EKG']+ \
        max(x['TOXSCREN'],x['URINE'])\
        +x['WOUNDCX']+x['OTHRTEST']+x['FLUTEST']+\
        x['ANYIMAGE']

    if temp >0:
        rss = temp
        
    #procedures
    if x['TOTPROC'] <> -9:
        temp = x['IVFLUIDS']+ x['CAST']+x['INCDRAIN']+x['FBREM']+\
        x['BLADCATH']+x['CENTLINE']+x['ENDOINT'] #x['NEBUTHER']+
        
    if temp >0:
        if rss is None:
            rss = temp
        else:
            rss = rss+ temp
    
    if x['DIAGSCRN'] ==0 and x['PROC'] == 0:
            return 0
    
    if rss > 2:
        return 2
    return rss