import numpy as np
import pandas as pd 
import os
import sys
import pymongo
from src.constant import *
from src.Data_Acces.data_access import Loan_data
from src.exeception import CustomException
from src.logging import logging
from dataclasses import dataclass


@dataclass
class DataIngestion_Config:
    Data_ingestion_dir=os.path.join(Artifacts_folder,"data_ingestion")

class Data_Ingestion:
    def __init__(self):
       self.data_dir=DataIngestion_Config()

    def export_data_into_data_dir(self):
        '''
        This function will get data from mongo db and store in our artifacts folder'''
        try:
            #make sure your artifcats folder have made
            Filepath=self.data_dir.Data_ingestion_dir
            os.makedirs(Filepath,exist_ok=True)

            #data
            loan_data=Loan_data(database_name=DATABASE_NAME)

            #iterate over the data
            logging.info(f"Saving exported data into feature store file path: {Filepath}")
            for collection_names,data in loan_data.export_collection():
                store_file_path=os.path.join(Filepath,collection_names+'.csv')
                print('dataset store in',store_file_path)
                data.to_csv(store_file_path,index=False)#write in csv format
        except Exception as e :
            raise CustomException(e,sys)
    
    #start data ingestion
    def initiate_dataingestion(self):
        try:
            logging.info('Started data-ingestion process'
                         )
            self.export_data_into_data_dir()

            logging.info("Got thr data from mongodb")
            
            logging.info("Exiting the data ingestion process")
            
            return self.data_dir.Data_ingestion_dir
        except Exception as e:
            raise CustomException (e,sys)
        


if __name__ == "__main__":
    print("Data ingestion started")

    obj = Data_Ingestion()
    obj.initiate_dataingestion()

    print("Data ingestion completed")

            