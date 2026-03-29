import os
import sys
from typing import List
from src.logging import logging
from src.exeception import CustomException
from src.Utils.utils import utils
from dataclasses import dataclass
from flask import request
from src.constant import *
import pandas as pd

@dataclass
class PredictionFileDetail:
    prediction_file_dir:str='Prediction'
    prediction_file_output:str='Prediction.csv'
    prediction_file_path:str=os.path.join(prediction_file_dir,prediction_file_output)

class PredictionPipeline:
    def __init__(self,request):
        self.utils=utils()
        self.prediction_detail=PredictionFileDetail()
        self.request=request

    def save_input_files(self)->str:
        try:
            pred_file_input_dir = "prediction_artifacts"
            os.makedirs(pred_file_input_dir, exist_ok=True)
             
            input_csv_file = self.request.filesv_files['file']
            pred_file_path = os.path.join(pred_file_input_dir,input_csv_file.filename)
            
            
            input_csv_file.save(pred_file_path)
            print(f"pred file path", pred_file_path)
            return pred_file_path
        
        except Exception as e:
            raise CustomException(e,sys)
        
    def predict(self, features):
        try:
                
            model_path = self.utils.download_object(
                    bucket_name=AWS_S3_BUCKET_NAME,
                    bucket_filename="model.pkl",
                    dest_file="model.pkl"
                )
            model = self.utils.load_object(path=model_path)
            print(f"model",model)

            preds = model.predict(features)

            return preds
        except Exception as e:
            raise CustomException(e,sys)
    def get_predict_dataframe(self,input_dataframe_path:str)->pd.DataFrame:
        try:
            prediction_column_name : str = Target_column
            input_dataframe: pd.DataFrame = pd.read_csv(input_dataframe_path)
            if Target_column in input_dataframe.columns:
               input_dataframe=input_dataframe.drop(columns=[Target_column])
               predictions = self.predict(input_dataframe)
            input_dataframe[prediction_column_name] = [pred for pred in predictions]
            target_column_mapping = {0:'Reject', 1:'Approve'}

            input_dataframe[prediction_column_name] = input_dataframe[prediction_column_name].map(target_column_mapping)
            
            os.makedirs(self.prediction_detail.prediction_file_dir, exist_ok= True)
            input_dataframe.to_csv(self.prediction_detail.prediction_file_path, index= False)
            logging.info("predictions completed. ")
            return input_dataframe

        except Exception as e:
            raise CustomException(e, sys) from e
    def run_pipeline(self):
        try:
            input_csv_path = self.save_input_files()
            self.get_predict_dataframe(input_csv_path)

            return self.prediction_file_detail


        except Exception as e:
            raise CustomException
        


