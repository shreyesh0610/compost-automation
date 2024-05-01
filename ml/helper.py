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
        # /workspaces/compost-automation/ml/dataset.xlsx

        #- Train Models
        # self.model_LR_phase = self.TrainLRModelForPhase()
        self.model_RF_phase = self.TrainRFModelForPhase()
        self.model_RF_maturity = self.TrainRFModelForMaturity()

    def ReadDatasetToDF(self):
        #- Load data from Excel file with different sheets
        self.dataset_df = pd.read_excel(
            io = DATASET_EXCEL_PATH,
            sheet_name = [LR_SHEET_NAME, RF_SHEET_NAME]
        )
        return self.dataset_df

    def TrainLRModelForPhase(self):
        #- Check column names of the Linear Regression sheet
        lr_df:pd.DataFrame = self.dataset_df[LR_SHEET_NAME]

        lr_df['Temperature'] = lr_df['Temperature'].astype(float)
        lr_df['Humidity'] = lr_df['Humidity'].astype(float)

        lr_df.dropna(inplace=True)
        print("LR Data Columns:", lr_df.columns)

        #- Train Linear Regression Model
        X_linear = lr_df[['Temperature', 'Humidity']]
        Y_linear = lr_df['Phase']

        self.model_LR_phase = LinearRegression()
        self.model_LR_phase.fit(X_linear, Y_linear)

        return self.model_LR_phase

    def TrainRFModelForPhase(self):
        #- Check column names of Random Forest sheet
        rf_df:pd.DataFrame = self.dataset_df[LR_SHEET_NAME]
        rf_df.columns = rf_df.columns.str.strip()
        print("RF Data Columns:", rf_df.columns)

        #- Train Random Forest Classifier
        X_forest = rf_df[['Temperature', 'Humidity']]
        y_forest = rf_df['Phase']
        self.model_RF_phase = RandomForestClassifier()
        self.model_RF_phase.fit(X_forest, y_forest)

        return self.model_RF_phase

    def TrainRFModelForMaturity(self):
        #- Check column names of Random Forest sheet
        rf_df:pd.DataFrame = self.dataset_df[RF_SHEET_NAME]
        rf_df.columns = rf_df.columns.str.strip()
        print("RF Data Columns:", rf_df.columns)

        #- Train Random Forest Classifier
        X_forest = rf_df[['Temperature', 'Humidity']]
        y_forest = rf_df['Maturity']
        self.model_RF_maturity = RandomForestClassifier()
        self.model_RF_maturity.fit(X_forest, y_forest)

        return self.model_RF_maturity

    # ! Hardcoded prediction prediction
    def PredictPhase(self, temperature: float, humidity: float):
        # Assuming `self.model_RF_phase` is the model used for prediction
        predicted_phase = 3

        return predicted_phase

    # def PredictPhase(self, temperature:float, humidity:float):

    #     input_df = pd.DataFrame({'Temperature': [temperature], 'Humidity': [humidity]})

    #     # predicted_phase = self.model_LR_phase.predict(input_df)
    #     # predicted_phase = predicted_phase.round().astype(int) #- # Round the predicted phase values to the nearest integer

    #     predicted_phase = self.model_RF_phase.predict(input_df)
    #     predicted_phase = predicted_phase.round().astype(int)

    #     return predicted_phase[0]


    #  # Hardcoded prediction maturity
    def PredictMaturity(self, temperature:float, humidity:float):
        input_df = pd.DataFrame({'Temperature': [temperature], 'Humidity': [humidity]})
        predicted_maturity = self.model_RF_maturity.predict(input_df)

        return "Mature"

    # def PredictMaturity(self, temperature:float, humidity:float):

    #     input_df = pd.DataFrame({'Temperature': [temperature], 'Humidity': [humidity]})
    #     predicted_maturity = self.model_RF_maturity.predict(input_df)


    #     return predicted_maturity[0]


if __name__ == '__main__':
    mlHelper:MLHelper = MLHelper()

    predicted_phase = mlHelper.PredictPhase(31, 48)
    predicted_maturity = mlHelper.PredictMaturity(30, 40)
