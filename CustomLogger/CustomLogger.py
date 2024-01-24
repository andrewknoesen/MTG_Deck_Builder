import logging

class CustomLogLevel:
    CUSTOM_LEVEL = 25

# Register the new log level with a custom name
logging.addLevelName(CustomLogLevel.CUSTOM_LEVEL, 'CUSTOM')

# Create a custom logger class
class CustomLogger(logging.Logger):
    def custom(self, msg, *args, **kwargs):
        if self.isEnabledFor(CustomLogLevel.CUSTOM_LEVEL):
            self._log(CustomLogLevel.CUSTOM_LEVEL, msg, args, **kwargs)

# Set the custom logger class
logging.setLoggerClass(CustomLogger)

# Configure the logging module with a custom log level
logging.basicConfig(level=CustomLogLevel.CUSTOM_LEVEL, format='%(asctime)s [%(levelname)s] [%(filename)s:%(lineno)d] - %(message)s')

# Obtain a logger instance
logger = logging.getLogger(__name__)

def log_message(msg: str, log_level=CustomLogLevel.CUSTOM_LEVEL):
    if log_level == CustomLogLevel.CUSTOM_LEVEL:
        logger.custom(msg, stacklevel=2)
    else:
        logger.log(log_level, msg, stacklevel=2)
        
def log_error(msg):
    log_message(msg, logging.ERROR)

def log_warn(msg):
    log_message(msg, logging.WARN)
    
def log_info(msg):
    log_message(msg, logging.INFO)