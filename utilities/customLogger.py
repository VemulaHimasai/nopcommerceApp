import logging
import os


class LogGen:

    @staticmethod
    def loggen():

        # Get project root directory
        project_path = os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))
        )

        # Logs folder
        log_folder = os.path.join(project_path, "Logs")

        # Create Logs folder if it doesn't exist
        os.makedirs(log_folder, exist_ok=True)

        # Log file path
        log_file = os.path.join(log_folder, "automation.log")

        logging.basicConfig(
            filename=log_file,
            format='%(asctime)s: %(levelname)s: %(message)s',
            datefmt='%m/%d/%Y %I:%M:%S %p',
            level=logging.INFO,
            force=True
        )

        logger = logging.getLogger()

        return logger
