import os
import numpy as np
import pandas as pd
import sys
from src.exeception import CustomException
from src.logging import logging
from src.constant import *
from src.Utils.utils import utils
from sklearn.linear_model import  LogisticRegression
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score
from dataclasses import dataclass
from sklearn.compose import ColumnTransformer
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV

@dataclass
class ModelCofig:
    model_dir=os.path.join(Artifacts_folder,'Model_Trainer')
    Trained_model_path=os.path.join(model_dir,'Trained_model.pkl')
    model_config=os.path.join("Config",'model.yaml')

class VisibiltyModel:
    def __init__(self,preprocessor:ColumnTransformer,trained_model_object):
        self.preprocessor=preprocessor
        self.trained_model_object=trained_model_object

    def predict(self,X:pd.DataFrame)->pd.DataFrame:
        '''This function will predict on preprocessed data'''
        try:
            logging.info('Predicting Dataframe..')
            transformed_data=self.preprocessor.transform(X)
            logging.info('Transformed the feature..')

            return self.trained_model_object.predict(transformed_data)
        except Exception as e:
            raise CustomException(e,sys)
class Model_Trainer:
    def __init__(self):
        self.model_config=ModelCofig()
        self.model={
            "GaussianNB":GaussianNB(),
            "LogisticRegression":LogisticRegression(),
            "XGBclassifier":XGBClassifier(objective="binary:logistic"),
            "RandomForestClassifier":RandomForestClassifier()}
        self.utils=utils()
    
    def evaluate_model(self,X_train,X_test,Y_train,Y_test,models):
        '''This function will evaluate the model perfomance and generate report...'''
        try:
            report = {}
            for model_name, model in models.items():
             model.fit(X_train, Y_train)

             Y_pred_train = model.predict(X_train)
             Y_pred_test = model.predict(X_test)

             train_score = accuracy_score(Y_train, Y_pred_train)
             test_score = accuracy_score(Y_test, Y_pred_test)

             report[model_name] = test_score

            return report

        except Exception as e:
          raise CustomException(e, sys)
        
    def get_best_model(self,X_train:np.array,
                       X_test:np.array,
                       Y_train:np.array,
                       Y_test:np.array):
        
        '''This function will select best model from report'''

        try:
            model_report:dict=self.evaluate_model(
                X_train=X_train,
                X_test=X_test,
                Y_train=Y_train,
                Y_test=Y_test,
                models=self.model
            )

            #get best model score
            best_model_score=max(sorted(model_report.values()))

            #get best model name
            best_model_name=list(model_report.keys())[list(model_report.values()).index(best_model_score)]

            #best model object
            best_model_object=self.model[best_model_name]

            return best_model_name,best_model_score,best_model_object
        except Exception as e:
            raise CustomException(e,sys)
        
    def finetune_best_model(self,best_model_name,best_model_object,X_train,Y_train):
            '''This funtion will tune the model '''
            try:
                model_paramgrid=self.utils.readyaml_file(self.model_config.model_config)["model_selection"]["model"][best_model_name]["search_param_grid"]

                gridsearch_cv=GridSearchCV(best_model_object,param_grid=model_paramgrid,cv=3,n_jobs=-1)

                gridsearch_cv.fit(X_train,Y_train)

                best_params=gridsearch_cv.best_params_#best params
                print(f"best_parameter for model {best_model_object}",best_params)

                fine_tuned_model= best_model_object.set_params(**best_params)
                return fine_tuned_model
            except Exception as e:
                raise CustomException(e,sys)
    
    def initiate_model_trainer(self,X_train,Y_train,X_test,Y_test,preprocessor_path):
        '''This will start the model training process'''

        logging.info('Starting model traning process..')

        try:
            #load thr preprocessor file like preprocessor.pkl
            preprocessor=self.utils.load_object(path=preprocessor_path)

            logging.info('Got the preprocssor file'
                         )
            model_report:dict=self.evaluate_model(
                X_train=X_train,
                Y_train=Y_train,
                X_test=X_test,
                Y_test=Y_test,
                models=self.model
            )
            
            #best model score
            best_model_score=best_model_score=max(sorted(model_report.values()))

            #best model name
            best_model_name=list(model_report.keys())[list(model_report.values()).index(best_model_score)]

            #best model object
            best_model_object=self.model[best_model_name]

            #now fine tune model

            finetuned_model=self.finetune_best_model(best_model_name=best_model_name,best_model_object=best_model_object,X_train=X_train,Y_train=Y_train)

            finetuned_model.fit(X_train,Y_train)

            y_pred=finetuned_model.predict(X_test)

            best_model_score= accuracy_score(Y_test,y_pred)
            
            print("best model name and score is ",best_model_name,best_model_score)

            custom_model=VisibiltyModel(preprocessor=preprocessor,trained_model_object=finetuned_model)

            logging.info('Saving file at path',self.model_config.Trained_model_path)

            os.makedirs(os.path.dirname(self.model_config.Trained_model_path),exist_ok=True)

            self.utils.save_object(path=self.model_config.Trained_model_path,
                                obj=custom_model)
            
            
            return best_model_score
        except Exception as e:
            raise CustomException (e,sys)





            

            
        



    
       

       


        
        

