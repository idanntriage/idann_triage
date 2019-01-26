import csv
import pandas as pd
import numpy as np

def  exclusionCriteriaFromCDC(cdc_file) :
    #Performing same exclusion than the ones performed in the referenced paper:

    #"The 2009 sample included 26,556 adult (18 years and older) patient records from 356 of 389 EDs 
    #(91.5% unweighted response rate), resulting in an unbiased weighted national sample of 102 million ED patient visits (20).
    # Patients dead on arrival (11 patient visits [< 0.1%]), transferred to a psychiatric hospital (594 [2.2%]), or with an
    # unknown outcome (753 patient visits [2.9%]) were excluded. The final study cohort of 25,198 patient visits provided data
    # for a weighted nationally representative sample of 97 million patient visits."
    
    print ('number of original records: %6d' % len(cdc_file) )
    
    # Excluding patients less than 18 years old and records where the date of birth was missing
    # [BDATEFL] Patient birth date - IMPUTED FIELDS 
    # [AGE] PATIENT AGE (IN YEARS; DERIVED FROM DATE OF BIRTH) 
    cdc_file_t1 = cdc_file[(cdc_file['AGE'] >= 18) & ( cdc_file['BDATEFL'] != 1)]
    print ('removing records where age <18 or DOB was missing: %6d' % len(cdc_file_t1))

    #excluding patients dead on arrival
    # [DOA] Dead On Arrival
    cdc_file_t2 = cdc_file_t1[(cdc_file_t1['DOA'] ==0) ]
    print ('removing records of patients dead on arrival: %6d' % len(cdc_file_t2))

    #excludes patients that were transferred to a pshychratic hospital
    # [TRANPSYC] Transfer to psychiatric hospital 
    # [ADMIT] Admitted to:
    cdc_file_t3 = cdc_file_t2[(cdc_file_t2['TRANPSYC'] ==0) &( cdc_file_t2['ADMIT']!=4)]
    print ('removing records of patients transferred to a psychiatric unit: %6d' % len(cdc_file_t3))

    # excludes records where the outcome is unknown 
    # [ADMIT] Admitted to:
    cdc_file_t4 = cdc_file_t3[(cdc_file_t3['ADMIT'] > -8) ]
    print ('removing records where the outcome is not unknown: %6d' % len(cdc_file_t4))
    
    # excludes records where ESI was imputed?  we don't have to since the model is predicting Critical Outcomes,
    # we are not using the ESI from the CDC file for the model
    #if 'IMMEDRFL' in cdc_file_t4.columns:
    #    cdc_file_t4 = cdc_file_t4[(cdc_file_t4['IMMEDRFL'] == 0) ]
    #    print ('removing records where the ESI was imputed: %6d' % len(cdc_file_t4))
    
    #removing records where the ESI is unknown (not mention in the paper but graphs don't include unknown ESI)  
    # [IMMEDR] RECODED IMMEDIACY WITH WHICH PATIENT SHOULD BE SEEN 
    cdc_input = cdc_file_t4[(cdc_file_t4['IMMEDR'] !=7) & (cdc_file_t4['IMMEDR'] > 0) ]
    print ('removing records where the SEI is not unknown: %6d' % len(cdc_input))
    return cdc_input

def consolidateAndApplyExclusion(years, fileConfig):
    outputDirectory =  fileConfig['dataDirectory'] + fileConfig['processedDirectory']  
    inputDirectory = fileConfig['dataDirectory'] + fileConfig['interimDirectory']  
    output_filename = outputDirectory +"ED_TOTAL_" +   years[0] + "_" + years[len(years)-1] + ".csv"
    number_records = 0
    appended_data = []
    for file_year in years:
        fileName = inputDirectory +'ED' + file_year + '.csv'
        cdc_file = pd.read_csv(fileName)
        cdc_input = exclusionCriteriaFromCDC(cdc_file)
        appended_data.append(cdc_input)
        print '-' *50
        number_records += len (cdc_input)   
    cdc_files_appended = pd.concat(appended_data, ignore_index=True)
    cdc_files_appended = cdc_files_appended.fillna(-9)
    cdc_files_appended.to_csv(output_filename, index=False)
    

def filter_out_records_na(cdc_file):
    cdc_filtered = cdc_file[(cdc_file.TEMPF != -9 )| (cdc_file.PULSE != -9)|(cdc_file.RESPR != -9) | \
                           (cdc_file.BPSYS != -9) |(cdc_file.BPDIAS != -9) | (cdc_file.POPCT != -9) | \
                           (cdc_file.AGE != -9) | (cdc_file.SEX != -9)]
    return cdc_filtered 
    
    
    