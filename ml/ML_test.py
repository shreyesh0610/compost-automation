# import pandas as pd
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.linear_model import LinearRegression
# from sklearn.preprocessing import LabelEncoder

# # # import sys COMMENT
# # # import os
# # # from os.path import dirname
# # # sys.path.append(os.path.abspath(os.path.join(dirname(__file__), os.pardir)))

# # # import pandas as pd
# # # from sklearn.linear_model import LinearRegression
# # # from sklearn.ensemble import RandomForestClassifier
# # # from sklearn.preprocessing import LabelEncoder

# # # from utils import *

# # # Define your constants here if needed
# # # LR_SHEET_NAME = 'LinearRegressionSheetName'
# # # RF_SHEET_NAME = 'RandomForestSheetName'
# # # DATASET_EXCEL_PATH = 'path/to/your/dataset.xlsx'

# class MLHelper:
#     def  __init__(self, dataset_excel_path):
#         self.dataset_df: pd.DataFrame = None
#         self.model_LR = None
#         self.model_RF_phase = None
#         self.model_RF_maturity = None

#         #- Read Dataframe
#         self.dataset_excel_path = dataset_excel_path
#         self.dataset_df = self.ReadDatasetToDF()

#         #- Train Models
#         self.model_LR = self.TrainLRModel()
#         self.model_RF_phase = self.TrainRFModelForPhase()
#         self.model_RF_maturity = self.TrainRFModelForMaturity()

#     def ReadDatasetToDF(self):
#         #- Load data from Excel file with different sheets
#         self.dataset_df = pd.read_excel(
#             io=self.dataset_excel_path,
#             sheet_name=None  # Read all sheets into a dictionary
#         )
#         return self.dataset_df

#     def TrainLRModel(self):
#         #- Check column names of the Linear Regression sheet
#         lr_df: pd.DataFrame = self.dataset_df['Linear Regression-']  # Replace 'LinearRegressionSheetName' with the actual name of your linear regression sheet

#         lr_df['Temperature'] = lr_df['Temperature'].astype(float)
#         lr_df['Humidity'] = lr_df['Humidity'].astype(float)
#         lr_df['Ec'] = lr_df['Ec'].astype(float)
#         lr_df['Ph'] = lr_df['Ph'].astype(float)

#         lr_df.dropna(inplace=True)
#         print("LR Data Columns:", lr_df.columns)

#         #- Train Linear Regression Model
#         X_linear = lr_df[['Temperature', 'Humidity', 'Ec', 'Ph']]
#         Y_linear = lr_df['Phase']

#         model_LR = LinearRegression()
#         model_LR.fit(X_linear, Y_linear)

#         return model_LR

#     def TrainRFModelForPhase(self):
#         #- Check column names of Random Forest sheet for phase
#         rf_df: pd.DataFrame = self.dataset_df['Linear Regression-']  # Replace 'RandomForestSheetName' with the actual name of your random forest sheet
#         rf_df.columns = rf_df.columns.str.strip()
#         print("RF Data Columns for Phase:", rf_df.columns)

#         #- Train Random Forest Classifier for phase
#         X_forest = rf_df[['Temperature', 'Humidity', 'Ec', 'Ph']]
#         y_forest = rf_df['Phase']
#         model_RF_phase = RandomForestClassifier()
#         model_RF_phase.fit(X_forest, y_forest)

#         return model_RF_phase

#     def TrainRFModelForMaturity(self):
#         #- Check column names of Random Forest sheet for maturity
#         rf_df: pd.DataFrame = self.dataset_df['Random Forest']  # Replace 'RandomForestSheetName' with the actual name of your random forest sheet
#         rf_df.columns = rf_df.columns.str.strip()
#         print("RF Data Columns for Maturity:", rf_df.columns)

#         #- Train Random Forest Classifier for maturity
#         X_forest = rf_df[['Temperature', 'Humidity', 'Ec', 'Ph']]
#         y_forest = rf_df['Maturity']
#         model_RF_maturity = RandomForestClassifier()
#         model_RF_maturity.fit(X_forest, y_forest)

#         return model_RF_maturity
    
#     def PredictPhase(self, temperature: float, humidity: float, ec: float, ph: float):
#         input_df = pd.DataFrame({'Temperature': [temperature], 'Humidity': [humidity], 'Ec': [ec], 'Ph': [ph]})
        
#         predicted_phase = self.model_RF_phase.predict(input_df)
#         predicted_phase = predicted_phase.round().astype(int)[0]  # Fix subscriptable error

#         # - logic to not let phase go backward
#         # old_phase = int(self.dataset_df['Linear Regression-']['Phase'].iloc[-1])  # Assuming 'Phase' column exists in the last sheet
#         # predicted_phase = max(predicted_phase, old_phase)
#         # ----------

#         return predicted_phase

#     def PredictMaturity(self, temperature: float, humidity: float, ec: float, ph: float):
#         input_df = pd.DataFrame({'Temperature': [temperature], 'Humidity': [humidity], 'Ec': [ec], 'Ph': [ph]})
#         predicted_maturity = self.model_RF_maturity.predict(input_df)
        
#         return predicted_maturity[0]

# def test_model_with_user_input(mlHelper):
#     # Take input values for humidity, temperature, ec, and pH
#     new_input = [31.9, 85, 212, 5.4]  # Example input values

#     # Convert the input values into a format that can be used by the model
#     new_input_features = [new_input]  # Convert to a list of lists

#     # Make predictions using the trained model
#     predicted_phase = mlHelper.PredictPhase(*new_input)
#     predicted_maturity = mlHelper.PredictMaturity(*new_input)

#     print("Predicted Phase:", predicted_phase)
#     print("Predicted Maturity:", predicted_maturity)


# if __name__ == '__main__':
#     # Provide the path to the Excel file containing the dataset
#     dataset_excel_path = r"/home/admin/Desktop/test-compostifAI/compost-automation/ml/dataset.xlsx"

#     # Create an instance of MLHelper
#     mlHelper = MLHelper(dataset_excel_path)

#     # Test the ML models with user input
#     test_model_with_user_input(mlHelper)
