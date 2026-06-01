# Import sys module for system-specific parameters and exception details
import sys

# Import logging module for logging errors and events
import logging


# Function to generate detailed error message
def error_message_detail(error, error_detail: sys):

    # Extract exception traceback information
    _, _, exc_tb = error_detail.exc_info()

    # Get file name where exception occurred
    file_name = exc_tb.tb_frame.f_code.co_filename

    # Return formatted detailed error message
    return "Error occurred in python script name [{0}] line number [{1}] error message [{2}]".format(
        
        # Insert file name
        file_name,

        # Insert line number where error occurred
        exc_tb.tb_lineno,

        # Insert actual error message
        str(error)
    )


# Create custom exception class
class CustomException(Exception):

    # Constructor for custom exception
    def __init__(self, error_message, error_detail: sys):

        # Call parent Exception constructor
        super().__init__(error_message)

        # Store formatted detailed error message
        self.error_message = error_message_detail(error_message, error_detail)

    # String representation of exception
    def __str__(self):

        # Return detailed error message when exception is printed
        return self.error_message