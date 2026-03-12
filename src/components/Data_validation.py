import numpy as np
import pandas as pd
import os
import sys
from src.exeception import CustomException
from src.logging import logging
from src.constant import *
from dataclasses import dataclass
import json
import shutil
from typing import List

@dataclass
class DataValidationConfig:
    Data_dir=os.path.join(Artifacts_folder,"DataValidation")
    valid_data_dir=os.path.join(Data_dir,"Valid_data")
    invalid_data=os.path.join(Data_dir,'Invalid_data')
    schema_config=os.path.join("Config","schema.json")

class DataValidation:
    def __init__(self,raw_data_dir):
        self.raw_data_dir=raw_data_dir
        self.datavalidation_config=DataValidationConfig()

    #first check schema values:
    def Validate_schema(self):
        '''
        This function will read the schema config and return the values of schema
        '''
        try:
            with open(self.datavalidation_config.schema_config,'r') as file:
                dic=json.load(file)
            no_of_columns=dic["NumberofColumns"]
            datestampfile=dic["LengthOfDateStampInFile"]
            lengthoftimestamp=dic["LengthOfTimeStampInFile"]

            return no_of_columns,datestampfile,lengthoftimestamp
        except Exception as e:
            raise CustomException (e,sys)
    #now validate filename

    def validate_filename(self,filepath:str)->bool:
        '''
        This fucntion will return boolean value if filename is correct or not
        '''
        try:
            filename=os.path.basename(filepath)
            originalfilename='loan_data.csv'
            if filename==originalfilename:
                validation_status=True
            else:
                validation_status=False
            return validation_status
        except Exception as e:
            raise CustomException (e,sys)

    #now validate no of columns
    def validate_no_of_columns(self,filepath:str,schema_cols:int)->bool:
        '''This function will valiadte no of columns and return the boolean value
        '''
        try:
            dataframe=pd.read_csv(filepath)
            validate_columns_status=len(dataframe.columns)==schema_cols
            return validate_columns_status
        except Exception as e:
            raise CustomException(e,sys)
        
    #missing value in whole columns
    def missing_values_in_whole_columns(self,filepath:str)->bool:
        '''
        This fucntion will return boolean value '''
        
        try:
            dataframe=pd.read_csv(filepath)
            
            column_with_missing_value=dataframe.isnull().all().any()#return boolean 
            if column_with_missing_value==True:
                column_with_missing_value_status=False
            else:
                column_with_missing_value_status=True
            return column_with_missing_value_status
        except Exception as e:
            raise CustomException(e,sys)
        
    def get_raw_filespath(self)->List:
        '''
        This function will read the all files and return list of all files'''
        try:
            filenames=os.listdir(self.raw_data_dir)
            file=[os.path.join(self.raw_data_dir,filename)for filename in filenames]

            return file
        except Exception as e:
            raise CustomException (e,sys)
        
    def move_file_to_valid_dir(self,curr_path:str,dest_path:str):
        '''This function will move file to valid data dir '''
        try:
           os.makedirs(dest_path,exist_ok=True)
           if os.path.basename(curr_path) not in  os.listdir(dest_path):
               shutil.move(curr_path,dest_path)
        except Exception as e:
            raise CustomException (e,sys)
        
    def validate_raw_files(self):
        '''This fuunction will now validate file using our written function'''
        try:
            filename=self.get_raw_filespath()#will get all filespath in list
            no_of_columns,datestampfile,lengthoftimestamp=self.Validate_schema()
            validated_files=0
            for filespath in filename:

                validate_filename_status=self.validate_filename(filepath=filespath)
                no_of_column_status=self.validate_no_of_columns(filepath=filespath,schema_cols=no_of_columns)
                missing_value_columns_status=self.missing_values_in_whole_columns(filepath=filespath)

                #now check for condition
                if validate_filename_status and no_of_column_status and missing_value_columns_status:
                    self.move_file_to_valid_dir(curr_path=filespath,dest_path=self.datavalidation_config.valid_data_dir)
                    validated_files+=1
                else:
                    self.move_file_to_valid_dir(curr_path=filespath,dest_path=self.datavalidation_config.invalid_data)
                validate_status=validated_files>0
            return validate_status
        except Exception as e:
            raise CustomException (e,sys)
        
    #initiate data validation
    def initiate_datavalidation(self):
        '''This function will intiate data data validation process by calling validate raw files'''

        try:
            logging.info("Starting DataValidation processs...")
            validate_status=self.validate_raw_files()

            if validate_status:
                valid_data_dir=self.datavalidation_config.valid_data_dir
                return valid_data_dir
            else:
                print('No data to further processss')
                logging.info('Got the invalida data')
        except Exception as e:
            raise CustomException(e,sys)


        
               
               




            


