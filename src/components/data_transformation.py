import sys  # For handling system-specific parameters and exceptions
from dataclasses import dataclass  # Used to create configuration class

import numpy as np   # Numerical operations
import pandas as pd  # Data handling with DataFrames

from sklearn.compose import ColumnTransformer  # Apply different transformations to columns
from sklearn.impute import SimpleImputer  # Fill missing values
from sklearn.pipeline import Pipeline  # Create preprocessing pipelines
from sklearn.preprocessing import OneHotEncoder, StandardScaler  # Encoding + Scaling

from src.exception import CustomException  # Custom exception handling
from src.logger import logging  # Logging messages
import os  # File path operations

from src.utils import save_object  # Save Python objects (like preprocessor)

@dataclass
class DataTransformationConfig:  
    preprocessor_obj_file_path = os.path.join('artifacts', "proprocessor.pkl")  # Path to save preprocessor

class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()  # Initialize config

    def get_data_transformer_object(self):
        '''
        This function is responsible for data transformation
        '''
        try:
            numerical_columns = ["writing_score", "reading_score"]  # Numerical features
            
            categorical_columns = [  # Categorical features
                "gender",
                "race_ethnicity",
                "parental_level_of_education",
                "lunch",
                "test_preparation_course",
            ]

            num_pipeline = Pipeline(  # Numerical pipeline
                steps=[
                    ("imputer", SimpleImputer(strategy="median")),  # Fill missing with median
                    ("scaler", StandardScaler())  # Standardize numerical data
                ]
            )

            cat_pipeline = Pipeline(  # Categorical pipeline
                steps=[
                    ("imputer", SimpleImputer(strategy="most_frequent")),  # Fill missing with mode
                    ("one_hot_encoder", OneHotEncoder()),  # Convert categories into numerical
                    ("scaler", StandardScaler(with_mean=False))  # Scale encoded data
                ]
            )

            logging.info(f"Categorical columns: {categorical_columns}")  # Log categorical columns
            logging.info(f"Numerical columns: {numerical_columns}")  # Log numerical columns

            preprocessor = ColumnTransformer(  # Combine both pipelines
                [
                    ("num_pipeline", num_pipeline, numerical_columns),
                    ("cat_pipelines", cat_pipeline, categorical_columns)
                ]
            )

            return preprocessor  # Return preprocessing object
        
        except Exception as e:
            raise CustomException(e, sys)  # Raise custom exception
        
    def initiate_data_transformation(self, train_path, test_path):

        try:
            train_df = pd.read_csv(train_path)  # Load training data
            test_df = pd.read_csv(test_path)  # Load testing data

            logging.info("Read train and test data completed")

            logging.info("Obtaining preprocessing object")

            preprocessing_obj = self.get_data_transformer_object()  # Get transformer object

            target_column_name = "math_score"  # Target column

            numerical_columns = ["writing_score", "reading_score"]  # Numerical columns

            input_feature_train_df = train_df.drop(columns=[target_column_name], axis=1)  # Training input features
            target_feature_train_df = train_df[target_column_name]  # Training target

            input_feature_test_df = test_df.drop(columns=[target_column_name], axis=1)  # Testing input features
            target_feature_test_df = test_df[target_column_name]  # Testing target

            logging.info(
                f"Applying preprocessing object on training dataframe and testing dataframe."
            )

            input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df)  # Fit + transform train data
            input_feature_test_arr = preprocessing_obj.transform(input_feature_test_df)  # Transform test data

            train_arr = np.c_[input_feature_train_arr, np.array(target_feature_train_df)]  # Combine train features + target
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]  # Combine test features + target

            logging.info("Saved preprocessing object.")

            save_object(
                file_path=self.data_transformation_config.preprocessor_obj_file_path,  # Save location
                obj=preprocessing_obj  # Object to save
            )

            return (
                train_arr,  # Processed training array
                test_arr,  # Processed testing array
                self.data_transformation_config.preprocessor_obj_file_path,  # Saved preprocessor path
            )

        except Exception as e:
            raise CustomException(e, sys)  # Raise custom exception