# Code based on /modeling/cdc_model_processing.py
import pandas as pd
import numpy as np

#All vital signs baselines
def Temp_Baseline_NaN(i):
    if i==-9:
        return np.nan
    else:
        return i
#Heart rate - Doppler pulse not applicable since none in dataset (<18 years removed)
def Pulse_Baseline_NaN(i):
    if i==-9:
        return np.nan
    else:
        return i
#Systolic blood pressure
def Sys_BP_NaN(i):
    if i==-9:
        return np.nan
    else:
        return i
#Respiratory rate
def Resp_Rate_NaN(i):
    if i==-9:
        return np.nan
    else:
        return i
#Oxygen Saturation (Pulse Oximetry)
def Oxygen_Sat_NaN(i):
    if i==-9:
        return np.nan
    else:
        return i

def get_vital_signs(cdc_input, predictors, normalize = True) :
     #Baseline temperature
    cdc_input['Temp_Baseline'] = cdc_input['TEMPF']
    cdc_input['Temp_Baseline'] = cdc_input.Temp_Baseline.apply(Temp_Baseline_NaN)
    #Heart rate - Doppler pulse not applicable since none in dataset (<18 years removed)
    cdc_input['Pulse_Baseline'] = cdc_input['PULSE']
    cdc_input['Pulse_Baseline'] = cdc_input.PULSE.apply(Pulse_Baseline_NaN)
    #Systolic blood pressure
    cdc_input['Sys_BP_Baseline'] = cdc_input['BPSYS']
    cdc_input['Sys_BP_Baseline'] = cdc_input.Sys_BP_Baseline.apply(Sys_BP_NaN)
    #Respiratory rate
    cdc_input['Resp_Rate_Baseline'] = cdc_input['RESPR']
    cdc_input['Resp_Rate_Baseline'] = cdc_input.Resp_Rate_Baseline.apply(Resp_Rate_NaN)
    #Oxygen Saturation (Pulse Oximetry)
    cdc_input['Oxygen_Sat_Baseline'] = cdc_input['POPCT']
    cdc_input['Oxygen_Sat_Baseline'] = cdc_input.Resp_Rate_Baseline.apply(Oxygen_Sat_NaN)
    
    #Median replacement
    #Temp_Baseline, Pulse_Baseline, Sys_BP_Baseline, Resp_Rate_Baseline, Oxygen_Sat_Baseline
    #Will update replacement later
    predictors['Temp_Baseline'] = cdc_input['Temp_Baseline'].fillna(cdc_input['Temp_Baseline'].median())
    predictors['Pulse_Baseline'] = cdc_input['Pulse_Baseline'].fillna(cdc_input['Pulse_Baseline'].median())
    predictors['Sys_BP_Baseline'] = cdc_input['Sys_BP_Baseline'].fillna(cdc_input['Sys_BP_Baseline'].median())
    predictors['Resp_Rate_Baseline'] = cdc_input['Resp_Rate_Baseline'].fillna(cdc_input['Resp_Rate_Baseline'].median())
    predictors['Oxygen_Sat_Baseline'] = cdc_input['Oxygen_Sat_Baseline'].fillna(cdc_input['Oxygen_Sat_Baseline'].median())
    
    def normalize_field(field, min_value, max_value):
        return (predictors[field]-min_value) /( max_value-min_value)
    
    if normalize:
        predictors['Temp_Baseline'] = normalize_field('Temp_Baseline', min_value =827.0  , max_value = 1099.0)
        predictors['Pulse_Baseline'] = normalize_field('Pulse_Baseline', min_value =0  , max_value = 998.0)
        predictors['Sys_BP_Baseline'] = normalize_field('Sys_BP_Baseline', min_value =0  , max_value = 290.0)
        predictors['Oxygen_Sat_Baseline'] = normalize_field('Oxygen_Sat_Baseline', min_value =0  , max_value = 148.0)
        predictors['Resp_Rate_Baseline'] = normalize_field('Resp_Rate_Baseline', min_value =0  , max_value = 148.0)
    
    return predictors

#----------------------------------------------------------------------------------------------
# CATEGORIES
#----------------------------------------------------------------------------------------------

#Vital signs
def Hypothermia(i):
    if i<=950:
        return 1
    else:
        return 0
def Hyperthermia(i):
    if i>=1005:
        return 1
    else:
        return 0
#Heart rate - Doppler pulse not applicable since none in dataset (<18 years removed)
def Bradycardia(i):
    if i<50:
        return 1
    else:
        return 0
def Mild_Tachycardia(i):
    if i>=110 and i<=119:
        return 1
    else:
        return 0
def Moderate_Tachycardia(i):
    if i>=120 and i<=129:
        return 1
    else:
        return 0
def Severe_Tachycardia(i):
    if i>=130:
        return 1
    else:
        return 0
#Systolic blood pressure
def Hypotension(i):
    if i<100:
        return 1
    else:
        return 0
def Hypertension(i):
    if i>200:
        return 1
    else:
        return 0
#Respiratory rate
def Bradypnea(i):
    if i<14:
        return 1
    else:
        return 0
def Moderate_Tachypnea(i):
    if i>=20 and i<=27:
        return 1
    else:
        return 0
def Severe_Tachypnea(i):
    if i>=28:
        return 1
    else:
        return 0
#Oxygen Saturation (Pulse Oximetry)
def Mild_Hypoxia(i):
    if i>=90 and i<=94:
        return 1
    else:
        return 0
def Severe_Hypoxia(i):
    if i<90:
        return 1
    else:
        return 0


def get_vital_signs_group_features(cdc_input, predictors) :
    #Vital signs
    predictors['Hypothermia'] = cdc_input.Temp_Baseline.apply(Hypothermia)
    predictors['Hyperthermia'] = cdc_input.Temp_Baseline.apply(Hyperthermia)
    #Heart rate - Doppler pulse not applicable since none in dataset (<18 years removed)
    predictors['Bradycardia'] = cdc_input.Pulse_Baseline.apply(Bradycardia)
    predictors['Mild_Tachycardia'] = cdc_input.Pulse_Baseline.apply(Mild_Tachycardia)
    predictors['Moderate_Tachycardia'] = cdc_input.Pulse_Baseline.apply(Moderate_Tachycardia)
    predictors['Severe_Tachycardia'] = cdc_input.Pulse_Baseline.apply(Severe_Tachycardia)
    #Systolic blood pressure
    predictors['Hypotension'] = cdc_input.Sys_BP_Baseline.apply(Hypotension)
    predictors['Hypertension'] = cdc_input.Sys_BP_Baseline.apply(Hypertension)
    #Respiratory rate
    predictors['Bradypnea'] = cdc_input.Resp_Rate_Baseline.apply(Bradypnea)
    predictors['Moderate_Tachypnea'] = cdc_input.Resp_Rate_Baseline.apply(Moderate_Tachypnea)
    predictors['Severe_Tachypnea'] = cdc_input.Resp_Rate_Baseline.apply(Severe_Tachypnea)
    #Oxygen Saturation (Pulse Oximetry)
    predictors['Mild_Hypoxia'] = cdc_input.Oxygen_Sat_Baseline.apply(Mild_Hypoxia)
    predictors['Severe_Hypoxia'] = cdc_input.Oxygen_Sat_Baseline.apply(Severe_Hypoxia)
    
    
    return predictors 
