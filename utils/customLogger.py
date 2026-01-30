import logging
import os


class LogGen:
    @staticmethod
    def loggen():
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        log_dir = os.path.join(project_root, "logs")
        os.makedirs(log_dir, exist_ok=True)  # Create logs/ if it doesn't exist
        log_file = os.path.join(log_dir, "automation.log")

        logger = logging.getLogger("AutomationLogger")
        logger.setLevel(logging.INFO)

        if not logger.handlers:
            file_handler = logging.FileHandler(log_file)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                                          datefmt='%m/%d/%y %I:%M:%S %p')
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

        return logger