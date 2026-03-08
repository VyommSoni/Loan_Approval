import numpy as np
import pandas as pd
import os
import sys
from src.exeception import CustomException
from src.logging import logging
import pymongo
from src.constant import *
from typing import List

#Here we write code for getting loan_data from mongodb

class Loan_data:
    def __init__(self,database_name:str):
        self.database_name=database_name

    #get collection names
    def get_collection_names(self)->List:
        '''
        This function will get the all collection names of mongo database
        '''
        try:
            mongo_client=pymongo.MongoClient(MONGO_DB_URL)
            database=mongo_client[self.database_name]
            collection_names=database.list_collection_names()
            return collection_names
        except Exception as e:
          raise CustomException(e,sys)

   #get the data from collection
    def get_data_from_collection(self,collection)->pd.DataFrame:
        '''
        This function will return the data from collection in form of dataframe
        '''
        try:
            client=pymongo.MongoClient(MONGO_DB_URL)
            database_=client[self.database_name]
            collection=database_[collection]
            data=collection.find()

            df=pd.DataFrame(data)
            
            #in mongodb extra ID columns is automatic added to we have to remove it first
            if "_id" in df.columns.to_list():
                df.drop(columns='_id',axis=1)
            return df
        except Exception as e:
            raise CustomException(e,sys)
    
    def export_collection(self):
        '''
        This function will export the data aas dataframe
        '''
        try:
            collection=self.get_collection_names()
            for collection_name in collection:
                data=self.get_data_from_collection(collection=collection_name)
                yield collection_name,data
        except Exception as e:
            raise CustomException (e,sys)


        

