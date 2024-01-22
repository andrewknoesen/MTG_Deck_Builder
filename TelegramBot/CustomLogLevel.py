import logging

class CustomLogLevel(logging.Level):
    CUSTOM_LEVEL = 25

# Register the new log level with a custom name
logging.addLevelName(CustomLogLevel.CUSTOM_LEVEL, 'CUSTOM')
