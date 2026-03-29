import os
import sys
import numpy as np
import pandas as pd
from src.components.Data_ingestion import Data_Ingestion
from src.components.Data_validation import DataValidation
from src.components.Data_Transformation import DataTransformation
from src.components.Model_Building import Model_Trainer
from src.constant import *
from src.exeception import CustomException
from src.logging import logging
from pathlib import Path


class TrainingPipeline:

    def start_data_ingestion(self):
        '''This function will start the data ingestion process....'''
        try:
            data_dir=Data_Ingestion()
            valid_data_dir=data_dir.initiate_dataingestion()
            return valid_data_dir
        except Exception as e:
            raise CustomException(e,sys)
        
    def start_validation(self,valid_data_dir):
        '''This function will validate the data'''
        try:
            validation_dir=DataValidation(valid_data_dir)
            data_validation_dir=validation_dir.initiate_datavalidation()
            return data_validation_dir
        except Exception as e:
            raise CustomException(e,sys)
    
    def data_transformation(self,valid_data):
        '''This function will transform the data'''
        try:
            data_validation_dir=DataTransformation(valid_data)
            X_train,X_test,Y_train,Y_test,Preprocessor_path=data_validation_dir.DataTrasformation()
            return  X_train,X_test,Y_train,Y_test,Preprocessor_path
        except Exception as e:
            raise CustomException(e,sys)
    
    def model_buildiing(self,
                        X_train:np.array,X_test:np.array,Y_train:np.array,Y_test:np.array,Preprocessor_path:Path):
        '''This function will train the model'''
        try:
            model=Model_Trainer()
            model_score=model.initiate_model_trainer(X_train,X_test,Y_train,Y_test,Preprocessor_path)
            return model,model_score
        except Exception as e:
            raise CustomException (e,sys)
        
    def run_pipeline(self):
        '''this function will run all the components of files'''
        try:
            logging.info('Running the Training Pipeline...')
            valid_data_dir=self.start_data_ingestion()#data ingestion
            logging.info('Got the data..')

            data_validation_dir=self.start_validation(valid_data_dir)
            logging.info('Complete the Data validation process...')

            X_train,X_test,Y_train,Y_test,Preprocessor_path=self.data_transformation(data_validation_dir)
            logging.info('Completed the data transformation process...')

            model,model_score=self.model_buildiing(X_train,X_test,Y_train,Y_test,Preprocessor_path)


            print('best model score is ',model_score)
            return model

        except Exception as e:
            raise CustomException (e,sys)
        






        
