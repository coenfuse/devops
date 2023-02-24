# description of this module in 50 words
# ..


# standard imports
import logging

# internal imports
# ..

# module imports
# ..

# thirdparty imports
# ..



def trace(msg):
    logging.log(msg, level = 0)

def debug(msg):
    logging.log(msg, level = logging.DEBUG)

def info(msg):
    logging.log(msg, level = logging.INFO)

def warn(msg):
    logging.log(msg, level = logging.WARN)

def error(msg):
    logging.log(msg, level = logging.ERROR)

def critical(msg):
    logging.log(msg, level = logging.CRITICAL)