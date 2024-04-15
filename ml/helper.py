import sys
import os
from os.path import dirname
sys.path.append(os.path.abspath(os.path.join(dirname(__file__), os.pardir)))

import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

from utils import *

class MLHelper:
    def  __init__(self):
        self.dataset_df:pd.DataFrame = None
        self.model_LR = None
        self.model_RF = None

        #- Read Dataframe
        self.dataset_df = self.ReadDatasetToDF()

        #- Train Models
        self.model_LR = self.TrainRFModel()
        self.model_RF = self.TrainRFModel()

    def ReadDatasetToDF(self):
        #- Load data from Excel file with different sheets
        self.dataset_df = pd.read_excel(
            io = DATASET_EXCEL_PATH, 
            sheet_name = [LR_SHEET_NAME, RF_SHEET_NAME]
        )
        return self.dataset_df

    def TrainLRModel(self):
        #- Check column names of the Linear Regression sheet
        lr_df:pd.DataFrame = self.dataset_df[LR_SHEET_NAME]
        lr_df.columns = lr_df.columns.str.strip()
        print("LR Data Columns:", lr_df.columns)

        #- Train Linear Regression Model
        X_linear = lr_df[['Temperature', 'Humidity']]
        self.model_LR = LinearRegression()
        self.model_LR.fit(X_linear, lr_df['Phase'])

        return self.model_LR

    def TrainRFModel(self):
        #- Check column names of Random Forest sheet
        rf_df:pd.DataFrame = self.dataset_df[RF_SHEET_NAME]
        rf_df.columns = rf_df.columns.str.strip()
        print("RF Data Columns:", rf_df.columns)

        #- Train Random Forest Classifier
        X_forest = rf_df[['Temperature', 'Humidity']]
        y_forest = rf_df['Maturity']
        self.model_RF = RandomForestClassifier()
        self.model_RF.fit(X_forest, y_forest)

        return self.model_RF

    def PredictPhase(self, temperature:float, humidity:float):

        input_df = pd.DataFrame({'Temperature': [temperature], 'Humidity': [humidity]})
        predicted_phase = self.model_LR.predict(input_df)

        predicted_phase = predicted_phase.round().astype(int) #- # Round the predicted phase values to the nearest integer

        return predicted_phase[0]

    def PredictMaturity(self, temperature:float, humidity:float):

        input_df = pd.DataFrame({'Temperature': [temperature], 'Humidity': [humidity]})
        predicted_maturity = self.model_RF.predict(input_df)

        return predicted_maturity[0]


if __name__ == '__main__':
    mlHelper:MLHelper = MLHelper()
    
    predicted_phase = mlHelper.PredictPhase(30, 40)
    predicted_maturity = mlHelper.PredictMaturity(30, 40)
