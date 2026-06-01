# Import Flask class and required functions
from flask import Flask, request, render_template

# Import NumPy library
import numpy as np

# Import Pandas library
import pandas as pd

# Import StandardScaler for feature scaling
from sklearn.preprocessing import StandardScaler

# Import custom classes for data input and prediction pipeline
from src.pipeline.predict_pipeline import CustomData, PredictPipeline


# Create Flask application instance
application = Flask(__name__)

# Assign application to app variable
app = application


# Define route for home page
@app.route('/')
def index():
    # Render index.html when user visits homepage
    return render_template('index.html')


# Define route for prediction page
# Accept both GET and POST requests
@app.route('/predictdata', methods=['GET', 'POST'])
def predict_datapoint():

    # If request method is GET
    if request.method == 'GET':

        # Show input form page
        return render_template('home.html')

    else:

        # Create object of CustomData class
        # Collect all form input values
        data = CustomData(

            # Get gender input
            gender=request.form.get('gender'),

            # Get ethnicity input
            race_ethnicity=request.form.get('ethnicity'),

            # Get parental education input
            parental_level_of_education=request.form.get(
                'parental_level_of_education'
            ),

            # Get lunch type input
            lunch=request.form.get('lunch'),

            # Get test preparation course input
            test_preparation_course=request.form.get(
                'test_preparation_course'
            ),

            # Get reading score and convert into float
            reading_score=float(request.form.get('reading_score')),

            # Get writing score and convert into float
            writing_score=float(request.form.get('writing_score'))
        )

        # Convert collected input data into DataFrame
        pred_df = data.get_data_as_data_frame()

        # Print input data in terminal
        print(pred_df)

        # Print status message
        print("Before Prediction")

        # Create prediction pipeline object
        predict_pipeline = PredictPipeline()

        # Print status message
        print("Mid Prediction")

        # Predict result using trained model
        results = predict_pipeline.predict(pred_df)

        # Print status message
        print("After Prediction")

        # Render home page with prediction result
        return render_template('home.html', results=results[0])


# Main function
if __name__ == "__main__":

    # Run Flask app on all available network interfaces
    app.run(host="0.0.0.0")