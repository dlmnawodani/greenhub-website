# Import required packages and modules
# from __future__ import annotations
import logging as logging
# import sys as sys
# import os as os
# from decouple import config
# import asyncio as asyncio
# from typing import TYPE_CHECKING
from functools import wraps

class Logger:
    def __init__(self, name, write_to_file=False, log_file=None):
        """
        Initialize the Logger.

        Args:
            name (str): The name of the logger.
            write_to_file (bool, optional): Whether to write logs to a file. Defaults to False.
            log_file (str, optional): The path to the log file. Defaults to None.
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        self.formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # Add a file handler if write_to_file is True
        if write_to_file:
            # If log_file is not provided, use a default filename
            if log_file is None:
                log_file = 'app.log'
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(self.formatter)
            self.logger.addHandler(file_handler)
        else:
            # Optionally add a default console handler if write_to_file is False
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(self.formatter)
            self.logger.addHandler(console_handler)

    def _stringify(self, obj):
        """
        Format the object for logging.

        Args:
            obj: The object to be formatted.

        Returns:
            str: The formatted object string.
        """
        # format_object
        try:
            if isinstance(obj, (list, tuple, dict)):
                return repr(obj)
            return str(obj)
        except Exception as e:
            return f"<Unrepresentable: {e}>"
    
    """
    # def _log(self, level, message, obj=None, exc_info=False):
    #     if obj is not None:
    #         message = f"{message}: {obj}"
    #     self.logger.log(level, message, exc_info=exc_info)
    """
    
    def _log(self, level, message, obj=None, **kwargs):
        """
        Log a message with optional object and additional keyword arguments.

        Args:
            level: The logging level.
            message (str): The message to be logged.
            obj: The optional object to be logged.
            **kwargs: Additional keyword arguments for logging.
        """
        if obj is not None:
            # message = f"{message}: {obj}"
            message = f"{message}: {self._stringify(obj)}"
        self.logger.log(level, message, **kwargs)

    def debug(self, message, obj=None):
        """Log a debug message."""
        # self.logger.debug(message)
        self._log(logging.DEBUG, message, obj, exc_info=False)

    def info(self, message, obj=None):
        """Log an info message."""
        # self.logger.info(message)
        self._log(logging.INFO, message, obj, exc_info=False)

    def warn(self, message, obj=None):
        """Log a warning message."""
        # self.logger.warning(message)
        self._log(logging.WARNING, message, obj, exc_info=False)

    def error(self, message, obj=None):
        """Log an error message."""
        # self.logger.error(message)
        self._log(logging.ERROR, message, obj, exc_info=False)

    def exception(self, message=None, obj=None):
        """
        Log an exception message with traceback.

        If message is not provided, a default message is used.
        """
        if message is None:
            message = "An error occurred"
        # self.logger.exception(message)
        self._log(logging.ERROR, message, obj, exc_info=True)

    def set_level(self, level):
        """Set the logging level."""
        self.logger.setLevel(level)

    def add_handler(self, handler):
        """Add a custom handler to the logger."""
        handler.setFormatter(self.formatter)
        self.logger.addHandler(handler)

# Decorator function to log function/method calls
def logger_decorator(logger_name='logger', **logger_args):
    def decorator(func):
        logger_instance = Logger(logger_name, **logger_args)
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                if hasattr(args[0], '__class__') and hasattr(getattr(args[0], '__class__'), '__name__'):
                    # If the first argument is an instance of a class
                    class_name = args[0].__class__.__name__
                    logger_instance.debug(f"Calling method {func.__name__} of class {class_name} with args: {args[1:]}, kwargs: {kwargs}")
                else:
                    # If the first argument is not an instance of a class
                    logger_instance.debug(f"Calling function {func.__name__} with args: {args}, kwargs: {kwargs}")
                result = func(*args, **kwargs)
                if hasattr(args[0], '__class__') and hasattr(getattr(args[0], '__class__'), '__name__'):
                    # If the first argument is an instance of a class
                    class_name = args[0].__class__.__name__
                    logger_instance.debug(f"Method {func.__name__} of class {class_name} executed successfully")
                else:
                    logger_instance.debug(f"Function {func.__name__} executed successfully")
                return result
            except Exception as e:
                if hasattr(args[0], '__class__') and hasattr(getattr(args[0], '__class__'), '__name__'):
                    # If the first argument is an instance of a class
                    class_name = args[0].__class__.__name__
                    logger_instance.exception(f"Method {func.__name__} of class {class_name} encountered an error", e)
                else:
                    logger_instance.exception(f"Function {func.__name__} encountered an error", e)
                raise
        return wrapper
    return decorator

# Example usage:
if __name__ == "__main__":
    logger = Logger(__name__, write_to_file=False)
    # logger = Logger(__name__, write_to_file=True, log_file='app.log')

    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warn("This is a warning message")
    logger.error("This is an error message")

    try:
        1 / 0
    except Exception as e:
        logger.exception("An error occurred", e)

    # ====

    @logger_decorator(__name__)
    def example_function(x, y):
        return x / y

    class MyClass:
        def __init__(self):
            pass

        @logger_decorator(__name__)
        def example_method(self, x, y):
            return x / y

    # Test the decorated function
    try:
        example_function(5, 0)
    except Exception as e:
        pass

    # Test the decorated method
    my_instance = MyClass()
    try:
        my_instance.example_method(5, 0)
    except Exception as e:
        pass


__all__ = [
    "Logger",
    "logger_decorator"
]

        