# Importing os module for file and directory operations
import os

# Importing sys module to handle system-specific parameters and exceptions
import sys

# Importing custom exception class from src.exception
from src.exception import CustomException

# Importing custom logging setup
from src.logger import logging

# Importing pandas for data handling
import pandas as pd

# Importing function to split dataset into train and test
from sklearn.model_selection import train_test_split

# Importing dataclass decorator for cleaner config class
from dataclasses import dataclass

# Importing DataTransformation class
from src.components.data_transformation import DataTransformation

# Importing DataTransformation configuration
from src.components.data_transformation import DataTransformationConfig

# Importing ModelTrainer configuration
from src.components.model_trainer import ModelTrainerConfig

# Importing ModelTrainer class
from src.components.model_trainer import ModelTrainer


# Creating configuration class using dataclass
@dataclass
class DataIngestionConfig:
    
    # Path where train data will be saved
    train_data_path: str = os.path.join('artifacts', "train.csv")
    
    # Path where test data will be saved
    test_data_path: str = os.path.join('artifacts', "test.csv")
    
    # Path where raw data will be saved
    raw_data_path: str = os.path.join('artifacts', "data.csv")


# Creating DataIngestion class
class DataIngestion:
    
    # Constructor method
    def __init__(self):
        
        # Creating object of config class
        self.ingestion_config = DataIngestionConfig()

    
    # Main method for data ingestion
    def initiate_data_ingestion(self):
        
        # Logging entry into data ingestion method
        logging.info("Entered the data ingestion method or component")

        try:
            
            # Reading CSV file into pandas dataframe
            df = pd.read_csv('notebook\\data\\stud.csv')
            
            # Logging successful file read
            logging.info('Read the dataset as dataframe')

            
            # Creating artifacts folder if it doesn't already exist
            os.makedirs(
                os.path.dirname(self.ingestion_config.train_data_path),
                exist_ok=True
            )

            
            # Saving complete raw dataset into artifacts/data.csv
            df.to_csv(
                self.ingestion_config.raw_data_path,
                index=False,   # Prevent row index from being saved
                header=True    # Save column names
            )

            
            # Logging start of train-test split
            logging.info("Train test split initiated")

            
            # Splitting data into train and test sets
            train_set, test_set = train_test_split(
                df,                # Input dataframe
                test_size=0.2,     # 20% data for testing
                random_state=42    # Fixed random seed for reproducibility
            )

            
            # Saving training dataset
            train_set.to_csv(
                self.ingestion_config.train_data_path,
                index=False,
                header=True
            )

            
            # Saving testing dataset
            test_set.to_csv(
                self.ingestion_config.test_data_path,
                index=False,
                header=True
            )

            
            # Logging successful completion
            logging.info("Ingestion of the data is completed")

            
            # Returning train and test file paths
            return (
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )

        
        # If any error occurs
        except Exception as e:
            
            # Raise custom exception with system details
            raise CustomException(e, sys)


# Main program starts here
if __name__ == "__main__":
    
    # Creating object of DataIngestion class
    obj = DataIngestion()
    train_data,test_data=obj.initiate_data_ingestion()

    
    data_transformation=DataTransformation()
    train_arr,test_arr,_=data_transformation.initiate_data_transformation(train_data,test_data)

    modeltrainer=ModelTrainer()
    print(modeltrainer.initiate_model_trainer(train_arr,test_arr))
    
    