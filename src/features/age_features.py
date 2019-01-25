
def  get_age_normalize(cdc_input, predictors):    
    predictors['AGE'] = cdc_input['AGE']
    def normalize_field(field):
        min_age = 18
        max_age = 120 #TO DO : get exact
        return (predictors[field]-min_age)/(max_age-min_age)
    predictors['AGE'] = normalize_field('AGE')
    return predictors

# Age categories
#--------------------
def Age_18_30(i):
    if i>=18 and i<31:
        return 1
    else:
        return 0
def Age_31_40(i):
    if i>=31 and i<40:
        return 1
    else:
        return 0
def Age_41_50(i):
    if i>=41 and i<50:
        return 1
    else:
        return 0
def Age_51_60(i):
    if i>=51 and i<60:
        return 1
    else:
        return 0
def Age_61_70(i):
    if i>=61 and i<70:
        return 1
    else:
        return 0
def Age_71_80(i):
    if i>=71 and i<80:
        return 1
    else:
        return 0
def Age_81_Above(i):
    if i>=81:
        return 1
    else:
        return 0

def get_age_categories(cdc_input, predictors):

    predictors['Age_18_30'] = cdc_input.AGE.apply(Age_18_30)
    predictors['Age_31_40'] = cdc_input.AGE.apply(Age_31_40)
    predictors['Age_41_50'] = cdc_input.AGE.apply(Age_41_50)
    predictors['Age_51_60'] = cdc_input.AGE.apply(Age_51_60)
    predictors['Age_61_70'] = cdc_input.AGE.apply(Age_61_70)
    predictors['Age_71_80'] = cdc_input.AGE.apply(Age_71_80)
    predictors['Age_81_Above'] = cdc_input.AGE.apply(Age_81_Above)

    return predictors

