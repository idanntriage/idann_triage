import rfv_text_lookup    
import RFV_text_vectorizing
import pandas as pd

# Based on Roseanna's code (refactored)

def get_RFV_vector(i):
    if int(i) != -9 :
        myList = list(str(int(i)))
        newList = [int(x)*1.0 / 10 for x in myList]
        return newList
    else:
        return [0,0,0,0,0] 
    
    
def set_RFV_codes(x):
    codes = []
    codes.extend(get_RFV_vector2(x.RFV1))
    codes.append(10)
    codes.extend(get_RFV_vector2(x['RFV2']))
    codes.append(10)
    codes.extend(get_RFV_vector2(x['RFV3']))
    codes.append(10)
    codes.extend(get_RFV_vector2(x['RFV4']))
    codes.append(10)
    codes.extend(get_RFV_vector2(x['RFV5']))
    return codes

def get_all_RFV_codes(x):
    codes = []
    codes.extend(get_RFV_vector(x.RFV1))
    codes.append(1)
    codes.extend(get_RFV_vector(x['RFV2']))
    codes.append(1)
    codes.extend(get_RFV_vector(x['RFV3']))
    codes.append(1)
    codes.extend(get_RFV_vector(x['RFV4']))
    codes.append(1)
    codes.extend(get_RFV_vector(x['RFV5']))
    return codes

def get_RFV_vector2(i):    
    if i != -9 :
        myList = list(str(int(i)))
        newList = [int(x)  for x in myList]
        return newList
    else:
        return [0,0,0,0,0] 
    
    
def get_RFV_text(predictors, cdc_input):
    print ("Creating text for embeddings")
    predictors['RFV1_text'] = cdc_input.RFV1.apply(rfv_text_lookup.RFVtext)
    predictors['RFV2_text'] = cdc_input.RFV2.apply(rfv_text_lookup.RFVtext)
    predictors['RFV3_text'] = cdc_input.RFV3.apply(rfv_text_lookup.RFVtext)
    if 'RFV4'  in cdc_input:
        predictors['RFV4_text'] = cdc_input.RFV4.apply(rfv_text_lookup.RFVtext)
    if 'RFV5'  in cdc_input:
        predictors['RFV5_text'] = cdc_input.RFV5.apply(rfv_text_lookup.RFVtext)
    return predictors
        

def get_RFV_features(cdc_input, predictors, with_features_for_Embedding = False):
    
    #if 'RFV4' not in cdc_input:
    #    cdc_input ['RFV4'] = -9
    #if 'RFV5' not in cdc_input:
    #    cdc_input ['RFV5'] = -9
    
    predictors['RFV1']= cdc_input['RFV1'].apply(get_RFV_vector)
    predictors['RFV2']= cdc_input['RFV2'].apply(get_RFV_vector)
    predictors['RFV3']= cdc_input['RFV3'].apply(get_RFV_vector) 
    if 'RFV4'  in cdc_input:
        predictors['RFV4']= cdc_input['RFV4'].apply(get_RFV_vector)
    if 'RFV5'  in cdc_input:
        predictors['RFV5']= cdc_input['RFV5'].apply(get_RFV_vector)
    #predictors['RFV_codes'] = cdc_input.apply(set_RFV_codes, axis=1)
    #predictors['RFV_digit_codes'] = cdc_input.apply(get_all_RFV_codes, axis=1)
    
    if with_features_for_Embedding:  
        predictors = get_RFV_text(predictors, cdc_input)
    
    return predictors

#---------------------------------------------------------------------------
# converting RFV codes to a list of digits, each digit a feature
#---------------------------------------------------------------------------

def get_RFV_field_names(cdc_input):
    field_names = []
    if 'RFV4'  in cdc_input:
        limit_range = 6
    else:
        limit_range = 4
    for i in range(1,limit_range):
        for j in range(1,6):
            field_names.append('rfv' + str(i) + '_' + str(j))
    return field_names

def make_rfv_digit_features (predictors, cdc_input, normalize=False):
    def get_RFV_items(x):
        fields = ['RFV1','RFV2','RFV3','RFV4','RFV5']
        vector = []
        for field in fields:
            if field  not in cdc_input:
                continue
            if x [field] != -9 :
                vector.extend( list(str(int(x [field]))))
            else :
                vector.extend([0,0,0,0,0])
        return vector
    # Each RFV code follows a hierarchy, there is knowledge represented in the digits that are part 
    # of the RFV code, those digits represent which RFV are similar (like embeddings)
    #Here we make a RFV code, like '10302' to 5 inputs 1,0.3,0,2 
    field_RFV_field_names = get_RFV_field_names(cdc_input)
    #print field_names
    rfv_matrix = cdc_input.apply(get_RFV_items, axis=1)
    predictors[field_RFV_field_names] = pd.DataFrame(rfv_matrix.values.tolist(), index= rfv_matrix.index)
    if normalize:
        field_names = get_RFV_field_names(cdc_input)
        for field in field_names:
            predictors[field] = pd.to_numeric(predictors[field]) * 1.0/10    
    return predictors 

# ---------------------------------------------------------------
# Reasons for Visits  CATEGORIES
# ---------------------------------------------------------------
#Missing RFV code
def Reason_NaN(i):
    if i==-9:
        return numpy.nan
    else:
        return i
    
#All Reason For Visit Codes
def Reason_Chest_Pain(i):
    if i == 10500:
        return 1
    else:
        return 0
def Reason_Abdominal_Pain(i):
    if i == 15450:
    #if i>=15450 and i <= 15453:
        return 1
    else:
        return 0
def Reason_Headache(i):
    if i==12100:
        return 1
    else:
        return 0
def Reason_Shortness_of_Breath(i):
    if i ==14150:
        return 1
    else:
        return 0    
def Reason_Back_Pain(i):
    if i==19050 or i==19100:
        return 1
    else:
        return 0    
def Reason_Cough(i):
    if i==14400:
        return 1
    else:
        return 0 
def Reason_Nausea_Vomiting(i):
     if i==15250 or i==15300:
        return 1
     else:
        return 0    
def Reason_Fever_Chills(i):
    if i==10050 or i==10100:
        return 1
    else:
        return 0
def Reason_Syncope(i):
    if i==10300:
        return 1
    else:
        return 0    
def Reason_Dizziness(i):
    if i==12250:
        return 1
    else:
        return 0    
def Reason_Psychiatric_Complaint(i):
    if ((i>=11000 and i<=11990) or (i>=23000 and i<=23490)):
        return 1
    else:
        return 0   
def Reason_Nervous_System(i):
    if (((i>=12000 and i<=12590) or (i>=23500 and i<=23990)) and i!=12100 and i!=12250):
        return 1
    else:
        return 0
def Reason_Cardiovascular_Other(i):
    if ((i>=12600 and i<=12990) or (i>=25000 and i<=25990)):
        return 1
    else:
        return 0    
def Reason_Ears_Eyes_Complaint(i):
    if ((i>=13000 and i<=13990) or (i>=24000 and i<=24990)):
        return 1
    else:
        return 0    
def Reason_Respiratory_Other(i):
    if (((i>=14000 and i<=14990) or (i>=26000 and i<=26490)) and i!=14150 and i!=14400):
        return 1
    else:
        return 0    
def Reason_Gastrointestinal_Other(i):
    if (((i>=15350 and i<=16390) or (i>=26500 and i<=26990)) and i!=15450):
        return 1
    else:
        return 0    
def Reason_Genitourinary_Other(i):
    if ((i>=16400 and i<=18290) or (i>=27000 and i<=27990)):
        return 1
    else:
        return 0   
def Reason_Skin_Hair_Nails_Complaint(i):
    if ((i>=18300 and i<=18990) or (i>=28000 and i<=28990)):
        return 1
    else:
        return 0    
def Reason_Musculoskeletal_Other(i):
    if (((i>=19000 and i<=19990) or (i>=29000 and i<=29490)) and i!=19050 and i!=19100):
        return 1
    else:
        return 0    
def Reason_Injury_Poisoning(i):
    if i>=50010 and i<=59990:
        return 1
    else:
        return 0   
def Reason_Other(i):
    if i==0:
        return 1
    else:
        return 0 

def get_rfv_group_features (cdc_input, predictors) :
        #Creating binary RFV codes based on Dugas et al.
    drop4_5 = False
    if 'RFV4' not in cdc_input:
        cdc_input ['RFV4'] = -9
        drop4_5 = True

    if 'RFV5' not in cdc_input:
        cdc_input ['RFV5'] = -9
        drop4_5 = True
    cdc_input['Reason_Chest_Pain'] = cdc_input.RFV1.apply(Reason_Chest_Pain) + \
    cdc_input.RFV2.apply(Reason_Chest_Pain) + cdc_input.RFV3.apply(Reason_Chest_Pain) + \
    cdc_input.RFV4.apply(Reason_Chest_Pain) + cdc_input.RFV5.apply(Reason_Chest_Pain)
    predictors['Reason_Chest_Pain'] = cdc_input['Reason_Chest_Pain'].apply(lambda x: 1 if x >= 1 else 0)

    cdc_input['Reason_Abdominal_Pain'] = cdc_input.RFV1.apply(Reason_Abdominal_Pain) + \
    cdc_input.RFV2.apply(Reason_Abdominal_Pain) +  cdc_input.RFV3.apply(Reason_Abdominal_Pain) + \
    cdc_input.RFV4.apply(Reason_Abdominal_Pain) +  cdc_input.RFV5.apply(Reason_Abdominal_Pain)
    predictors['Reason_Abdominal_Pain'] = cdc_input['Reason_Abdominal_Pain'].apply(lambda x: 1 if x >= 1 else 0)
    
    cdc_input['Reason_Headache'] = cdc_input.RFV1.apply(Reason_Headache) + \
    cdc_input.RFV2.apply(Reason_Headache) +  cdc_input.RFV3.apply(Reason_Headache) + \
    cdc_input.RFV4.apply(Reason_Headache) +  cdc_input.RFV5.apply(Reason_Headache)
    predictors['Reason_Headache'] = cdc_input['Reason_Headache'].apply(lambda x: 1 if x >= 1 else 0)
    
    cdc_input['Reason_Shortness_of_Breath'] = cdc_input.RFV1.apply(Reason_Shortness_of_Breath) + \
    cdc_input.RFV2.apply(Reason_Shortness_of_Breath) + cdc_input.RFV3.apply(Reason_Shortness_of_Breath) + \
    cdc_input.RFV4.apply(Reason_Shortness_of_Breath) + cdc_input.RFV5.apply(Reason_Shortness_of_Breath)
    predictors['Reason_Shortness_of_Breath'] = cdc_input['Reason_Shortness_of_Breath'].apply(lambda x: 1 if x >= 1 else 0)
 
    cdc_input['Reason_Back_Pain'] = cdc_input.RFV1.apply(Reason_Back_Pain) + cdc_input.RFV2.apply(Reason_Back_Pain) +\
    cdc_input.RFV3.apply(Reason_Back_Pain) +\
    cdc_input.RFV4.apply(Reason_Back_Pain) + cdc_input.RFV5.apply(Reason_Back_Pain)
    predictors['Reason_Back_Pain'] =  cdc_input['Reason_Back_Pain'].apply(lambda x: 1 if x >= 1 else 0)
    
    cdc_input['Reason_Cough'] = cdc_input.RFV1.apply(Reason_Cough) + cdc_input.RFV2.apply(Reason_Cough) +\
    cdc_input.RFV3.apply(Reason_Cough) +\
    cdc_input.RFV4.apply(Reason_Cough) + cdc_input.RFV5.apply(Reason_Cough)
    predictors['Reason_Cough'] = cdc_input['Reason_Cough'].apply(lambda x: 1 if x >= 1 else 0)    
    
    cdc_input['Reason_Nausea_Vomiting'] = cdc_input.RFV1.apply(Reason_Nausea_Vomiting) + \
    cdc_input.RFV2.apply(Reason_Nausea_Vomiting) + cdc_input.RFV3.apply(Reason_Nausea_Vomiting) + \
    cdc_input.RFV4.apply(Reason_Nausea_Vomiting) + cdc_input.RFV5.apply(Reason_Nausea_Vomiting) 
    predictors['Reason_Nausea_Vomiting'] = cdc_input['Reason_Nausea_Vomiting'].apply(lambda x: 1 if x >= 1 else 0)    
    
    cdc_input['Reason_Fever_Chills'] = cdc_input.RFV1.apply(Reason_Fever_Chills)  + \
    cdc_input.RFV2.apply(Reason_Fever_Chills) + cdc_input.RFV3.apply(Reason_Fever_Chills) +\
    cdc_input.RFV4.apply(Reason_Fever_Chills) + cdc_input.RFV5.apply(Reason_Fever_Chills)
    predictors['Reason_Fever_Chills'] = cdc_input['Reason_Fever_Chills'].apply(lambda x: 1 if x >= 1 else 0)
    
    cdc_input['Reason_Syncope'] = cdc_input.RFV1.apply(Reason_Syncope) +\
    cdc_input.RFV2.apply(Reason_Syncope) + cdc_input.RFV3.apply(Reason_Syncope) +\
    cdc_input.RFV4.apply(Reason_Syncope) + cdc_input.RFV5.apply(Reason_Syncope)
    predictors['Reason_Syncope'] = cdc_input['Reason_Syncope'].apply(lambda x: 1 if x >= 1 else 0)    
    
    cdc_input['Reason_Dizziness'] = cdc_input.RFV1.apply(Reason_Dizziness) +\
    cdc_input.RFV2.apply(Reason_Dizziness)  +  cdc_input.RFV3.apply(Reason_Dizziness) +\
    cdc_input.RFV4.apply(Reason_Dizziness)  +  cdc_input.RFV5.apply(Reason_Dizziness)
    predictors['Reason_Dizziness'] = cdc_input['Reason_Dizziness'].apply(lambda x: 1 if x >= 1 else 0)
    
    cdc_input['Reason_Psychiatric_Complaint'] = cdc_input.RFV1.apply(Reason_Psychiatric_Complaint) + \
    cdc_input.RFV2.apply(Reason_Psychiatric_Complaint) + cdc_input.RFV3.apply(Reason_Psychiatric_Complaint)+ \
    cdc_input.RFV4.apply(Reason_Psychiatric_Complaint) + cdc_input.RFV5.apply(Reason_Psychiatric_Complaint)
    predictors['Reason_Psychiatric_Complaint'] = cdc_input['Reason_Psychiatric_Complaint'].apply(lambda x: 1 if x >= 1 else 0) 
    
    cdc_input['Reason_Nervous_System'] = cdc_input.RFV1.apply(Reason_Nervous_System) + \
    cdc_input.RFV2.apply(Reason_Nervous_System) + cdc_input.RFV3.apply(Reason_Nervous_System) + \
    cdc_input.RFV4.apply(Reason_Nervous_System) + cdc_input.RFV5.apply(Reason_Nervous_System)
    predictors['Reason_Nervous_System'] = cdc_input['Reason_Nervous_System'].apply(lambda x: 1 if x >= 1 else 0)    
    
    cdc_input['Reason_Cardiovascular_Other'] = cdc_input.RFV1.apply(Reason_Cardiovascular_Other) + \
    cdc_input.RFV2.apply(Reason_Cardiovascular_Other) + cdc_input.RFV3.apply(Reason_Cardiovascular_Other)+ \
    cdc_input.RFV4.apply(Reason_Cardiovascular_Other) + cdc_input.RFV5.apply(Reason_Cardiovascular_Other)
    predictors['Reason_Cardiovascular_Other'] = cdc_input['Reason_Cardiovascular_Other'].apply(lambda x: 1 if x >= 1 else 0)    
    
    cdc_input['Reason_Ears_Eyes_Complaint'] = cdc_input.RFV1.apply(Reason_Ears_Eyes_Complaint) + \
    cdc_input.RFV2.apply(Reason_Ears_Eyes_Complaint) + cdc_input.RFV3.apply(Reason_Ears_Eyes_Complaint)+ \
    cdc_input.RFV4.apply(Reason_Ears_Eyes_Complaint) + cdc_input.RFV5.apply(Reason_Ears_Eyes_Complaint)
    predictors['Reason_Ears_Eyes_Complaint'] = cdc_input['Reason_Ears_Eyes_Complaint'].apply(lambda x: 1 if x >= 1 else 0) 

    cdc_input['Reason_Respiratory_Other'] = cdc_input.RFV1.apply(Reason_Respiratory_Other) + \
    cdc_input.RFV2.apply(Reason_Respiratory_Other) + cdc_input.RFV3.apply(Reason_Respiratory_Other)+ \
    cdc_input.RFV4.apply(Reason_Respiratory_Other) + cdc_input.RFV5.apply(Reason_Respiratory_Other)
    predictors['Reason_Respiratory_Other'] = cdc_input['Reason_Respiratory_Other'].apply(lambda x: 1 if x >= 1 else 0)
    
    cdc_input['Reason_Gastrointestinal_Other'] = cdc_input.RFV1.apply(Reason_Gastrointestinal_Other) + \
    cdc_input.RFV2.apply(Reason_Gastrointestinal_Other) + cdc_input.RFV3.apply(Reason_Gastrointestinal_Other)+ \
    cdc_input.RFV4.apply(Reason_Gastrointestinal_Other) + cdc_input.RFV5.apply(Reason_Gastrointestinal_Other)
    predictors['Reason_Gastrointestinal_Other'] = cdc_input['Reason_Gastrointestinal_Other'].apply(lambda x: 1 if x >= 1 else 0)

    cdc_input['Reason_Genitourinary_Other'] = cdc_input.RFV1.apply(Reason_Genitourinary_Other) + \
    cdc_input.RFV2.apply(Reason_Genitourinary_Other) + cdc_input.RFV3.apply(Reason_Genitourinary_Other)+\
    cdc_input.RFV4.apply(Reason_Genitourinary_Other) + cdc_input.RFV5.apply(Reason_Genitourinary_Other)
    predictors['Reason_Genitourinary_Other'] = cdc_input['Reason_Genitourinary_Other'].apply(lambda x: 1 if x >= 1 else 0)
    
    cdc_input['Reason_Skin_Hair_Nails_Complaint'] = cdc_input.RFV1.apply(Reason_Skin_Hair_Nails_Complaint) +\
    cdc_input.RFV2.apply(Reason_Skin_Hair_Nails_Complaint) + cdc_input.RFV3.apply(Reason_Skin_Hair_Nails_Complaint)+\
    cdc_input.RFV4.apply(Reason_Skin_Hair_Nails_Complaint) + cdc_input.RFV5.apply(Reason_Skin_Hair_Nails_Complaint)
    predictors['Reason_Skin_Hair_Nails_Complaint'] = cdc_input['Reason_Skin_Hair_Nails_Complaint'].apply(lambda x: 1 if x >= 1 else 0)    
    
    cdc_input['Reason_Musculoskeletal_Other'] = cdc_input.RFV1.apply(Reason_Musculoskeletal_Other) +\
    cdc_input.RFV2.apply(Reason_Musculoskeletal_Other) + cdc_input.RFV3.apply(Reason_Musculoskeletal_Other)+\
    cdc_input.RFV4.apply(Reason_Musculoskeletal_Other) + cdc_input.RFV5.apply(Reason_Musculoskeletal_Other)
    predictors['Reason_Musculoskeletal_Other'] = cdc_input['Reason_Musculoskeletal_Other'].apply(lambda x: 1 if x >= 1 else 0)    
    
    cdc_input['Reason_Injury_Poisoning'] = cdc_input.RFV1.apply(Reason_Injury_Poisoning) + \
    cdc_input.RFV2.apply(Reason_Injury_Poisoning) + cdc_input.RFV3.apply(Reason_Injury_Poisoning)+\
    cdc_input.RFV4.apply(Reason_Injury_Poisoning) + cdc_input.RFV5.apply(Reason_Injury_Poisoning)
    predictors['Reason_Injury_Poisoning'] = cdc_input['Reason_Injury_Poisoning'].apply(lambda x: 1 if x >= 1 else 0)    
    
    cdc_input['reason']=cdc_input.ix[:, 'Reason_Chest_Pain':'Reason_Injury_Poisoning'].sum(axis=1)
    predictors['Reason_Other'] = cdc_input.reason.apply(Reason_Other)
    cdc_input.drop('reason',  axis=1, inplace=True)
    if drop4_5: 
        cdc_input.drop('RFV4',  axis=1, inplace=True)
        cdc_input.drop('RFV5',  axis=1, inplace=True)
   
    return predictors

def Reason_Other(i):
    if i==0:
        return 1
    else:
        return 0 
    
def is_there_a_code(x):
    if x['RFV1'] != -9 and  x['RFV2'] != -9 and  x['RFV3'] != -9 and  x['RFV4'] != -9 and  x['RFV5'] != -9 :
        return 0
    elif x['reason'] == 1:
        return 0
    else:
        return 1 
