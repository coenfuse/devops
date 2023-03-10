# description of this module in 50 words
# ..


# standard imports
import logging as __logger__

# internal imports
# ..

# module imports
# ..

# thirdparty imports
# ..



# docs
# ------------------------------------------------------------------------------
def trace(message: str) -> None:
    __logger__.log(5, message)


# docs
# ------------------------------------------------------------------------------
def debug(message: str) -> None:
    __logger__.debug(message)


# docs
# ------------------------------------------------------------------------------
def info(message: str) -> None:
    __logger__.info(message)


# docs
# ------------------------------------------------------------------------------
def warn(message: str) -> None:
    __logger__.warning(message)


# docs
# ------------------------------------------------------------------------------
def error(message: str) -> None:
    __logger__.error(message, exc_info = True, stack_info = True)


# docs
# ------------------------------------------------------------------------------
def critical(message: str) -> None:
    __logger__.critical(message, exc_info = True, stack_info = True)