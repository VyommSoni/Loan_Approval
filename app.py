from src.Pipelines.Training import  TrainingPipeline
from src.Pipelines.Prediction import PredictionPipeline
from flask import Flask,render_template,request,send_file,request
from src.exeception import CustomException
import sys
from src.logging import logging

app=Flask(__name__,template_folder="Template")

@app.route("/")
def home():
   return render_template('index.html')

@app.route("/train",methods=['GET'])
def train():
   try:
      train_pipeline=TrainingPipeline()
      train_pipeline_detail=train_pipeline.run_pipeline()
      logging.info('Training completed..')
      return send_file(train_pipeline_detail,download_name='model.pkl',as_attachment=True)
   except Exception as e:
      raise CustomException(e,sys) from e 
    
@app.route("/predict",methods=['Get','POST'])
def predict():
   try:
      if request.method=='POST' :
         predict=PredictionPipeline(request)
         predict_file_detail=predict.run_pipeline()
         logging.info('prediction completed ,downloading prediction file..')
         return send_file(predict_file_detail.prediction_file_path,download_name=predict_file_detail.prediction_file_output,as_attachment=True)
      
      else:
         return render_template("prediction.html")
   except Exception as e:
      raise CustomException(e,sys) from e

