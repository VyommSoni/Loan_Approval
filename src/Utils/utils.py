import os
import sys
import yaml
import pandas as pd
import numpy as np
from typing import List
from src.exeception import CustomException
from src.logging import logging
from src.constant import *
import pickle
from sklearn.base import BaseEstimator, TransformerMixin

from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd

class OutlierCapper(BaseEstimator, TransformerMixin):

    def fit(self, X, y=None):
        return self

    def transform(self, X):

        X = X.copy()

        discrete_features = [col for col in X.columns if X[col].nunique() <= 25]
        continuous_features = [col for col in X.columns if col not in discrete_features]

        for col in continuous_features:

            Q1 = X[col].quantile(0.25)
            Q3 = X[col].quantile(0.75)

            IQR = Q3 - Q1

            upper_limit = Q3 + 1.5 * IQR
            lower_limit = Q1 - 1.5 * IQR

            X[col] = X[col].clip(lower_limit, upper_limit)

        return X
    
class utils:
    
    @staticmethod
    def save_object(path:str,obj:object):
        try:
            with open(path,'wb') as file:
                pickle.dump(obj,file)
        except Exception as e:
            raise CustomException(e,sys)
        
    @staticmethod
    def load_object(path:str):
        try:
            with open(path,'rb') as file:
                obj=pickle.load(file)
            return obj
        except Exception as e:
            raise CustomException(e,sys)
        
    def readyaml_file(self,filename:str):

        try:
            with open(filename,'r') as file:
                yaml_=yaml.safe_load(file)
            return yaml
        except Exception as e:
            raise CustomException(e,sys)
        
            

        
            
