# IDANN Triage   
   
[IDANN Triage](https://zliendo.github.io/idann_home.html) utilizes interpretable deep neural networks with attention to predict critical patient outcomes and resources, aiding emergency departments with patient prioritization.

This repository contains refactored code (first round) from the original repository used during MIDS w210 capstone course:   
[MIDS-Capstone-EHR-ED-Care](https://github.com/r-hopper/MIDS-Capstone-EHR-ED-Care) (UCB capstone instructors have access to this repository). The code was re-factored for easy reading and replication, keeping model's architecture and performance levels (we are creating other project to evolve the initial model).   

The table below lists the notebooks that can be executed in the specified order to replicate results.   

## Pre-Processing and Exploratory Data Analysis (EDA)

|N. | Type | Task and its Notebook|  files|  
|---|---|---|---| 
| 1a | Pre-Processing | Transforms CDC fixed format files to CSV format. </br> Notebook:   [transform_fixed_to_csv.ipynb](notebooks/data_pre_processing/transform_fixed_to_csv.ipynb) | **Input:** data/raw/ED[year], </br> data/external/format[year].txt  </br> **Output:**  data/interim/ED[year].csv | 
| 1b | Pre-Processing | Consolidates files from different years into one and applies exclusion criteria. </br> Notebook: [consolidating_files.ipynb](notebooks/data_pre_processing/consolidating_files.ipynb)   |  **Input:** data/interim/ED[year].csv </br> **Output:** data/processed/ED_TOTAL_2009_2009.csv , </br> data/processed/ED_TOTAL_2009_2015.csv | 
| 2 | EDA | Exploratory Data Analysis of CDC data from 2009 to 2015. </br> Notebook: [CDC_eda_ESI_CO.ipynb](notebooks/eda/CDC_eda_ESI_CO.ipynb)|**Input:**  data/processed/ ED_TOTAL_2009_2015.csv | |

## Training Models   
|N. | Type | Task and its Notebook|  files|  
|---|---|---|---| 
| 3| **LR_BAS**:  Baseline Model | Logistic Regression replication Model that predicts critical outcomes. </br> Notebook: [CDC_LR_2009_baseline.ipynb](notebooks/modeling/CDC_LR_2009_baseline.ipynb) |  **Input:** data/processed/ ED_TOTAL_2009_2009.csv   | 
| 4a| **LR_RMH**: Improving LR Model|  Logistic Regression with additional features like: Reason for Visit (RFV) codes as vectors to capture its hierarchical semantic. </br> Notebook: [CDC_LR_2009_more_features.ipyn](notebooks/modeling/CDC_LR_2009_more_features.ipynb)    | **Input:**  data/processed/ ED_TOTAL_2009_2009.csv   |
| 4b|  **RF**: Random Forest|  We also implemented a Random forest (RF) model which provides a list of feature importance, relevant for model interpretation. However its performance was lower than the LR model. </br> Notebook: [CDC_RF_2009.ipynb](notebooks/modeling/CDC_RF_2009.ipynb)   |  **Input:** data/processed/ ED_TOTAL_2009_2009.csv   |
| 4c| **FNN**:Forward Neural Newtwork  |  FNN with the same features than RF and LR_RMH. </br> Notebook: [CDC_NN_2009_modeling.ipynb](notebooks/modeling/CDC_NN_2009_modeling.ipynb)    |  **Input:** data/processed/ ED_TOTAL_2009_2009.csv   |
| 4d| **FNN_TE**: FNN and Embeddings|  Forward Neural Newtwork (FNN) with embedding for the Reason for Visit (RFV) codes. </br>  Notebook:[CDC_NN_Embedding_2009_modeling.ipynb](notebooks/modeling/CDC_NN_Embedding_2009_modeling.ipynb)    | **Input:**  data/processed/  ED_TOTAL_2009_2009.csv   |
|5| **FNN_TE_ATT**: FNN Attention  for Critical Outcomes| FNN_TE with Attention Layer, predicts critical outcomes, with the attention layer. </br> Notebooks: [CDC_ATT_NN_2009_Text_Emb.ipynb](notebooks/modeling/CDC_ATT_NN_2009_Text_Emb.ipynb)    | **Input:** data/processed/ ED_TOTAL_2009_2009.csv   | 
|6| **FNN_TEA_RS**: FNN Attention for Resource estimation|  FNN_TE with Attention Layer, with multiclass outcome for resource utilization, Notebook: [CDC_ATT_RSS_NN_2009_Text_Emb.ipynb](notebooks/modeling/CDC_ATT_RSS_NN_2009_Text_Emb.ipynb)     |  **Input:** data/processed/ ED_TOTAL_2009_2009.csv   | 

## Determining ESI thresholds  
|N. | Type | Task and its Notebook|  files|  
|---|---|---|---| 
|7|Prediction | prediction with 2009 data to determine ESI thresholds.</br> Notebook: [Batch_2009_Prediction_for_Thresholds_Optimization.ipynb](notebooks/prediction/Batch_2009_Prediction_for_Thresholds_Optimization.ipynb)    | **Input:** data/processed/ ED_TOTAL_2009_2009.csv </br> **Output:** data/result/Predictions_2009_DataForThresholds.json | 
|8 |Thresholds | Determining thresholds for ESI values.</br> Notebook: [ESI_threshold_optimization.ipynb](notebooks/prediction/ESI_threshold_optimization.ipynb  )    |**Input:**  data/result/Predictions_2009_DataForThresholds.json  </br> **Output:** data/result/thresholds.json  |

## Test Evaluation with 2010 data 
|N. | Type | Task and its Notebook|  files|  
|---|---|---|---| 
|8|Prediction | prediction with 2010 for evaluation.</br> Notebook: [Batch_Prediction_2010.ipynb](notebooks/test_evaluation/Batch_Prediction_2010.ipynb)    | **Input:** data/processed/ ED_TOTAL_2010_2010.csv </br> **Output:** data/result/Predictions_2010_DataForThresholds.json | 
|9 |Results Viz | Several Visualizations comparing new ESI with original ESI and its performance improvement .</br> Notebook: [ESI_vs_pred_ESI_Viz.ipynb](notebooks/test_evaluation/ESI_vs_pred_ESI_Viz.ipynb)  , test_evaluation/ESI_sankeys_viz.ipynb    | **Input:**  data/result/ thresholds.json, </br>data/result/Predictions_2010_DataForThresholds.json</br>  **Output:** viz images and report |

## Prediction and pulling attention relative weights

|N. | Type | Task and its Notebook|  files|  
|---|---|---|---| 
|10|Prediction | Example of predicting for one record and pulling attention relative weights from the model that had just done the prediction </br> Notebook: [CO_ATT_prediction_interpretability_sample.ipynb](notebooks/prediction/CO_ATT_prediction_interpretability_sample.ipynb)    | **Input:** data/processed/ ED_TOTAL_2010_2010.csv </br> **Output:**  |
|11|Prediction | Example of how to predict for one record (it includes call to py method that is used in the cloud api-service) </br> Notebook: [ATTNN_predict_for_one_record.ipynb](notebooks/prediction/ATTNN_predict_for_one_record.ipynb)    | **Input:** data/processed/ ED_TOTAL_2010_2010.csv </br> **Output:**  |


## ESI Prediction API   
|N. | Type | Task and its Notebook|  files|  
|---|---|---|---| 
|12|API Service |  call to REST API example.</br> Notebook: [API_Service_Call_example.ipynb](notebooks/api_service/API_Service_Call_example.ipynb)   | **Input:**  </br> **Output:**   | 


Project structure based on:
https://drivendata.github.io/cookiecutter-data-science/

 
