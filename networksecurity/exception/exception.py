import sys
from networksecurity.logging import logger

class NetworkSecurityException(Exception):
    def __init__(self, message, error_details:sys):
        super().__init__(message)
        self.message = message
        _, _, exc_tb = error_details
        
        self.lineno = exc_tb.tb_lineno
        self.filename = exc_tb.tb_frame.f_code.co_filename

    def __str__(self):
        return "Error: {0} at line {1} in {2}".format(self.message, self.lineno, self.filename)
    
    
if __name__ == '__main__':
    try:
        logger.logging.info("this is a test message")
        a = 1/0
        print("this is a test message")
    except Exception as e:
        raise NetworkSecurityException("Error occured", sys.exc_info())