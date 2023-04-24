# description of this module in 50 words
# ..


# standard imports
import logging
import sys

# internal imports
# ..

# module imports
# ..

# thirdparty imports
# ..



# docs
# ------------------------------------------------------------------------------
def create_logger(
        name: str, 
        tag: str, 
        level: int, 
        propagate: bool = False) -> logging.Logger:
    
    logger = logging.getLogger(name)
    logger.propagate = propagate

    match level:
        case 0: logger.setLevel(5)      # TRACE
        case 1: logger.setLevel(logging.DEBUG)
        case 2: logger.setLevel(logging.INFO)
        case 3: logger.setLevel(logging.WARN)
        case 4: logger.setLevel(logging.ERROR)
        case 5: logger.setLevel(logging.CRITICAL)

    logfmt = logging.Formatter(
        fmt = f"%(asctime)s.%(msecs)03d [%(levelname).1s] : {tag} %(message)s", 
        datefmt = "%Y-%m-%d %H:%M:%S")
    
    # HACK : only used since isinstance(root_handler, logging.StreamHandler)
    # is not working correctly.
    # type(root_handler) prints <class 'logging.StreamHandler'> whereas
    # type(type(logging.StreamHandler)) prints <class 'type'>
    # This must be a meta-class issue
    def isStreamHandler(suspect):
        return suspect.__class__.__name__ == "StreamHandler"
    
    def isFileHandler(suspect):
        return suspect.__class__.__name__ == "FileHandler"
    
    for root_handler in logging.root.handlers:
        custom_handler = None

        if isStreamHandler(root_handler):
            custom_handler = logging.StreamHandler(sys.stdout)

        elif isFileHandler(root_handler):
            custom_handler = logging.FileHandler(
                filename = root_handler.baseFilename, 
                delay = True)

        if custom_handler is not None:
            custom_handler.setFormatter(logfmt)   
            logger.addHandler(custom_handler)

    return logger






# docs
# ------------------------------------------------------------------------------
def trace(message: str, logger: str = "") -> None:
    logging.getLogger(logger).log(5, message)


# docs
# ------------------------------------------------------------------------------
def debug(message: str, logger: str = "") -> None:
    logging.getLogger(logger).debug(message)


# docs
# ------------------------------------------------------------------------------
def info(message: str, logger: str = "") -> None:
    logging.getLogger(logger).info(message)


# docs
# ------------------------------------------------------------------------------
def warn(message: str, logger: str = "") -> None:
    logging.getLogger(logger).warning(message)


# docs
# ------------------------------------------------------------------------------
def error(message: str, logger: str = "") -> None:
    logging.getLogger(logger).error(message)


# docs
# ------------------------------------------------------------------------------
def critical(message: str, logger: str = "") -> None:
    logging.getLogger(logger).critical(message) # exc_info = True, stack_info = True)