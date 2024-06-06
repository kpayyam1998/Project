import os
import logging
from datetime import datetime

class Logger:
    def __init__(self):
        log_file = f"{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.log"
        
        # Create log directory with exist_ok=True to avoid the if condition
        os.makedirs('logs', exist_ok=True)

        # Get the log directory
        log_file_path = os.path.join(os.getcwd(), "logs", log_file)

        # Create log file and file format
        logging.basicConfig(filename=log_file_path,
                            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                            level=logging.INFO)

    @staticmethod
    def create_log(message):
        logging.info(message)
