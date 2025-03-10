import logging
import os
from SRC.Authentication import manageprofile

class Application:
    def __init__(self):
        self.path = os.getcwd()
        self.log_file_path = os.path.join(self.path,'Restaurant_Management_System-py', 'SRC', 'Logs', 'Application_log.txt')
        self.auth_manager = manageprofile.AuthenticationManager()
        self.setup_logging()
    
    def setup_logging(self):
        logging.basicConfig(
            filename=self.log_file_path,
            level=logging.ERROR,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
    
    def display(self):
        self.auth_manager.display_menu()


