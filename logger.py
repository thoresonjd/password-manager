"""
File: logger.py
Description: Logs messages to a file
Author: Justin Thoreson
Date: January 2024
"""

class Logger(object):
    """Logs messages to a file."""

    __slots__ = '__file', '__logs'

    def __init__(self, filename: str) -> None:
        """Opens/creates a log file and reads its contents."""

        self.__file = open(filename, 'a+')
        self.__logs = self.__read()

    def log(self, message: str) -> None:
        """Logs a message."""
        
        self.__logs.append(message)
        self.__write(message)

    def log_if_not_exists(self, message: str) -> bool:
        """
        Logs a message only if it does not already exist in the logs.
        :param message:
        :return: True if the message was logged, False otherwise
        """
        
        if (message_not_exists := message not in self.__logs):
            self.log(message)
        return message_not_exists
    
    def clear(self) -> None:
        """Clears all logs."""

        self.__logs.clear()
        self.__erase()
    
    def get_logs(self) -> list:
        """Retrieves a copy of the current logs."""
        
        return self.__logs[:]
    
    def __read(self) -> list:
        """Reads all lines from the log file."""

        self.__file.seek(0)
        return self.__file.read().splitlines()
    
    def __write(self, message: str) -> None:
        """Writes a message to the log file."""

        self.__file.write(f'{message}\n')
    
    def __erase(self) -> None:
        """Erases all contents of the log file."""

        self.__file.truncate(0)

    def __del__(self) -> None:
        """Closes the log file."""

        self.__file.close()