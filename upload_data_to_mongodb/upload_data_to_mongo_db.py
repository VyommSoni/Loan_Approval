import pymongo
import numpy as np
import pandas as pd
from src.constant import MONGO_DB_URL,DATABASE_NAME,DATABASE_DIR
from src.logging import logging
from src.exeception import CustomException
import sys
import os

class upload_data_to_mongodb:
    def __init__(self,csv_file):
        self.csv_file=csv_file

    #now first create connection

    def connection(self):
        '''
        This function will create the mongodbconnection
        '''
        try:
            Client=pymongo.MongoClient(MONGO_DB_URL)
            self.Database_name=Client[DATABASE_NAME]
            print(self.Database_name,'Database conection successfully')
        except Exception as e:
            raise CustomException (e,sys)
    
    #upload the data
    def upload_file(self):
        '''
        This function will upload the data to mongodb
        '''
        try:
          Collection_name=self.csv_file.split('.')[0]#using filename for collection name
          collection=self.Database_name[Collection_name]
          print(collection)
          #now make it into dataframe to read
          filepath=os.path.join(DATABASE_DIR,self.csv_file)

          #now read
          df=pd.read_csv(filepath)

          #now write it in database
          data=df.to_dict(orient='records')#because mongo db stores data in dictionary format

          if data:
             collection.insert_many(data)
             print('len of data',len(data))
          else:
             print('Not Found any data')
        except Exception as e:
         raise CustomException (e,sys)
if __name__ == "__main__":

    uploader = upload_data_to_mongodb("loan_data.csv")

    uploader.connection()
    uploader.upload_file()  



