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

        #- Read Dataframe
        self.dataset_df = self.ReadDatasetToDF()
        # /workspaces/compost-automation/ml/dataset.xlsx

        #- Train Models
        self.model_RF_phase = self.TrainRFModelForPhase()
        self.model_RF_maturity = self.TrainRFModelForMaturity()

    def ReadDatasetToDF(self):
        #- Load data from Excel file with different sheets
        self.dataset_df = pd.read_excel(
            io = DATASET_EXCEL_PATH,
            sheet_name = [LR_SHEET_NAME, RF_SHEET_NAME]
        )
        return self.dataset_df

    def TrainRFModelForPhase(self):
        #- Check column names of Random Forest sheet
        rf_df:pd.DataFrame = self.dataset_df[LR_SHEET_NAME]
        rf_df = rf_df.dropna()
        rf_df.columns = rf_df.columns.str.strip()
        print("RF Data Columns:", rf_df.columns)

        #- Train Random Forest Classifier
        X_forest = rf_df[['Temperature', 'Humidity', 'Ec', 'Ph']]
        y_forest = rf_df['Phase']
        self.model_RF_phase = RandomForestClassifier()
        self.model_RF_phase.fit(X_forest, y_forest)

        return self.model_RF_phase

    def TrainRFModelForMaturity(self):
        #- Check column names of Random Forest sheet
        rf_df:pd.DataFrame = self.dataset_df[RF_SHEET_NAME]
        rf_df = rf_df.dropna()
        rf_df.columns = rf_df.columns.str.strip()
        print("RF Data Columns:", rf_df.columns)

        #- Train Random Forest Classifier
        X_forest = rf_df[['Temperature', 'Humidity', 'Ec', 'Ph']]
        y_forest = rf_df['Maturity']
        self.model_RF_maturity = RandomForestClassifier()
        self.model_RF_maturity.fit(X_forest, y_forest)

        return self.model_RF_maturity

    def PredictPhase(self, temperature: float, humidity: float, ec: float, ph: float):

        input_df = pd.DataFrame({'Temperature': [temperature], 'Humidity': [humidity], 'Ec': [ec], 'Ph': [ph]})

        predicted_phase = self.model_RF_phase.predict(input_df)
        predicted_phase = predicted_phase.round().astype(int)

        # return 4 #! HARDCODED
        return predicted_phase[0]

    def PredictMaturity(self, temperature:float, humidity:float, ec: float, ph: float):

        input_df = pd.DataFrame({'Temperature': [temperature], 'Humidity': [humidity], 'Ec': [ec], 'Ph': [ph]})
        predicted_maturity = self.model_RF_maturity.predict(input_df)

        # return "Mature" #! HARDCODED
        return predicted_maturity[0]


if __name__ == '__main__':
    mlHelper:MLHelper = MLHelper()

    predicted_phase = mlHelper.PredictPhase(29.50, 95, 220,4.90)
    predicted_maturity = mlHelper.PredictMaturity(29.50, 95, 220,4.90)
    print(predicted_phase, predicted_maturity)

