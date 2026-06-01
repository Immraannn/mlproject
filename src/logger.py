# Import logging module for creating logs
import logging

# Import os module for directory and file path operations
import os

# Import datetime module to get current date and time
from datetime import datetime


# Create log file name using current timestamp
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"


# Create path for log file inside logs folder
logs_path = os.path.join(os.getcwd(), "logs", LOG_FILE)


# Create directory if it does not exist
os.makedirs(logs_path, exist_ok=True)


# Create full log file path
LOG_FILE_PATH = os.path.join(logs_path, LOG_FILE)


# Configure logging settings
logging.basicConfig(

    # Set log file location
    filename=LOG_FILE_PATH,

    # Set format of log messages
    format="[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s",

    # Set logging level
    level=logging.INFO,
)