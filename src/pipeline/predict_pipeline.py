# Import sys module for system-specific parameters
import sys

# Import os module for file path handling
import os

# Import pandas for DataFrame operations
import pandas as pd

# Import custom exception class
from src.exception import CustomException

# Import utility function to load saved objects
from src.utils import load_object


# Class for handling prediction pipeline
class PredictPipeline:

    # Constructor
    def __init__(self):
        pass

    # Function to make predictions
    def predict(self, features):
        try:

            # Define path for trained model file
            model_path = os.path.join("artifacts", "model.pkl")

            # Define path for preprocessor file
            preprocessor_path = os.path.join("artifacts", "preprocessor.pkl")

            # Print message before loading files
            print("Before Loading")

            # Load trained model
            model = load_object(file_path=model_path)

            # Load preprocessor object
            preprocessor = load_object(file_path=preprocessor_path)

            # Print message after loading files
            print("After Loading")

            # Transform input features using preprocessor
            data_scaled = preprocessor.transform(features)

            # Predict using trained model
            preds = model.predict(data_scaled)

            # Return predictions
            return preds

        except Exception as e:

            # Raise custom exception if error occurs
            raise CustomException(e, sys)


# Class for collecting custom input data
class CustomData:

    # Constructor to initialize input values
    def __init__(
        self,
        gender: str,
        race_ethnicity: str,
        parental_level_of_education: str,
        lunch: str,
        test_preparation_course: str,
        reading_score: int,
        writing_score: int
    ):

        # Store gender value
        self.gender = gender

        # Store race/ethnicity value
        self.race_ethnicity = race_ethnicity

        # Store parental education level
        self.parental_level_of_education = parental_level_of_education

        # Store lunch type
        self.lunch = lunch

        # Store test preparation course status
        self.test_preparation_course = test_preparation_course

        # Store reading score
        self.reading_score = reading_score

        # Store writing score
        self.writing_score = writing_score


    # Convert input data into DataFrame
    def get_data_as_data_frame(self):
        try:

            # Create dictionary of input values
            custom_data_input_dict = {

                "gender": [self.gender],

                "race_ethnicity": [self.race_ethnicity],

                "parental_level_of_education": [
                    self.parental_level_of_education
                ],

                "lunch": [self.lunch],

                "test_preparation_course": [
                    self.test_preparation_course
                ],

                "reading_score": [self.reading_score],

                "writing_score": [self.writing_score],
            }

            # Convert dictionary into pandas DataFrame
            return pd.DataFrame(custom_data_input_dict)

        except Exception as e:

            # Raise custom exception if error occurs
            raise CustomException(e, sys)