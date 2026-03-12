import os
import sys
import pandas as pd
import numpy 
from typing import List
from src.exeception import CustomException
from src.logging import logging
from dataclasses import dataclass
from sklearn.model_selection import train_test_split
from src.constant import *
from src.Utils.utils import utils,OutlierCapper
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler,PowerTransformer
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer


@dataclass
class DataTransformationConfig:
    Transformed_dir=os.path.join(Artifacts_folder,"Data_Transformation")
    Transformed_X_train=os.path.join(Transformed_dir,"Train.npy")
    Transformed_X_test=os.path.join(Transformed_dir,"Test.npy")
    Transfomed_File=os.path.join(Transformed_dir,"Preprocessing.pkl")

class DataTransformation:
    def __init__(self,valid_data_dir):
        self.utils=utils()
        self.DataTransfomed_dir=DataTransformationConfig()
        self.valid_data_dir=valid_data_dir

    @staticmethod
    def merged_batch_files(valid_data_dir:str)->pd.DataFrame:
        '''This function will iterate over the dir of data validation and 
        merge all files'''
        #in production system ,data comes from multiple sources,so before preprocessing
        #we must merge it ,so we can easliy do further steps

        try:
            file_name=os.listdir(valid_data_dir)
            csv_data=[]

            for files in file_name:
                csv_files=pd.read_csv(os.path.join(valid_data_dir,files))
                csv_data.append(csv_files)
            merged_data =pd.concat(csv_data)
            return merged_data
        except Exception as e:
            raise CustomException(e,sys)
        
    def DataTrasformation(self):

        '''This function will intiate data transformation process'''
        try:
            df=DataTransformation.merged_batch_files(valid_data_dir=self.valid_data_dir)

            #feature enginering
            df['Gender']=df['Gender'].replace({
           "Male":1,
           "Female":0
             })

            df['Education']=df['Education'].replace({
            "Graduate":1,
            "Not Graduate":0
              })

            df['Self_Employed']=df['Self_Employed'].replace({
            "No":0,
            "Yes":1
             })

            df['Property_Area']=df['Property_Area'].replace({
            "Urban":1,
            "Semiurban":2,
            "Rural":3
               })

            df['Loan_Status']=df['Loan_Status'].replace({
            "Y":1,
            "N":0
             })
            df['Dependents']=df['Dependents'].replace({
           "1":1,
           "2":2,
           "3+":3
            })

        #here we should not encode married columns beacuse it totally depends on dependent column beacuse if its not  married then 
        #its value will be 0 in dependent,otherwise numerical value

        #Extracting new columns or Features


            df['Total_Income']=df['ApplicantIncome']+df['CoapplicantIncome']
            df["LoanAmount"]=df['LoanAmount']*1000
            df['Loan_Amount_Term']=df['Loan_Amount_Term']/12

            #Drop the irrevelant columns

            df.drop(columns=['Loan_ID','Married','ApplicantIncome','CoapplicantIncome'],axis=1,inplace=True)
            
            #change the datatype
            df['Gender'] = pd.to_numeric(df['Gender'], errors='coerce')
            df['Dependents'] = pd.to_numeric(df['Dependents'], errors='coerce')
            df['Education'] = pd.to_numeric(df['Education'], errors='coerce')
            df['LoanAmount'] = pd.to_numeric(df['LoanAmount'], errors='coerce')
            df['Loan_Amount_Term'] = pd.to_numeric(df['Loan_Amount_Term'], errors='coerce')
            df['Property_Area'] = pd.to_numeric(df['Property_Area'], errors='coerce')
            df['Loan_Status'] = pd.to_numeric(df['Loan_Status'], errors='coerce')
            df['Total_Income'] = pd.to_numeric(df['Total_Income'], errors='coerce')

            #Rename the columns:
            df.rename(columns={
            "Dependents":"having_family",
            "LoanAmount":"Loan",
            "Loan_Amount_Term":"Repay_years",
             },inplace=True)
            
            #X and Y
            X=df.drop(columns=Target_column,axis=1)
            Y=df[Target_column]

            #train test split
            X_train,X_test,Y_train,Y_test=train_test_split(X,Y,random_state=42,test_size=0.2)

            #first derive column of different datatype
            num_features = [feature for feature in X_train.columns if X_train[feature].dtype != 'O']
            print('Num of Numerical Features :', len(num_features))

            discrete_features = [col for col in num_features if X_train[col].nunique() <= 25]
            print("Num of Discrete Features:", len(discrete_features))

            continuous_features = [col for col in num_features if col not in discrete_features]
            print("Num of Continuous Features:", len(continuous_features))


            #now impute missing values in differnet datatype

            discrete_pipeline = Pipeline(steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("standard_scaler",StandardScaler())
             ])

            continuous_pipeline = Pipeline(steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("oulier_capping",OutlierCapper()),
            ("power_transformer",PowerTransformer()),
            ("standard_scaler",StandardScaler())
             ])  
            
            
            Preprocessor=ColumnTransformer(
                transformers=[
                    ("discrete_pipeline",discrete_pipeline,discrete_features),
                    ("continious_pipeline",continuous_pipeline,continuous_features)
                ]
            )
            
            #now fit X_train into preprocessor
            X_train=Preprocessor.fit_transform(X_train)
            X_test=Preprocessor.transform(X_test)


            #save preprocessor file

            Preprocessor_path=self.DataTransfomed_dir.Transfomed_File
            os.makedirs(os.path.dirname(Preprocessor_path),exist_ok=True)

            self.utils.save_object(path=Preprocessor_path,obj=Preprocessor)

            return X_train,X_test,Y_train,Y_test,Preprocessor_path
        
        except Exception as e:
            raise CustomException(e,sys)






        







