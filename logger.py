"""
File: logger.py
Description: Logs messages to a file
Author: Justin Thoreson
Date: 3 January 2024
"""

class Logger(object):
    """Logs messages to a file."""

    __slots__ = 'file', 'logs'

    def __init__(self, filename: str) -> None:
        """Opens/creates a log file and reads its contents."""

        self.file = open(filename, 'a+')
        self.logs = self.__read()

    def log(self, message: str, end: str = '\n') -> None:
        """Logs a message."""
        
        message = ''.join([message, end])
        self.logs.append(message)
        self.__write(message)

    def log_if_not_exists(self, message: str, end: str = '\n') -> None:
        """Logs a message only if it does not already exist in the logs."""
        
        if message not in self.logs:
            self.log(message, end)
    
    def clear(self) -> None:
        """Clears all logs."""

        self.logs.clear()
        self.__erase()
    
    def __read(self) -> list:
        """Reads all lines from the log file."""

        self.file.seek(0)
        return self.file.read().splitlines()
    
    def __write(self, message) -> None:
        """Writes a message to the log file."""

        self.file.write(message)
    
    def __erase(self) -> None:
        """Erases all contents of the log file."""

        self.file.truncate(0)

    def __del__(self) -> None:
        """Closes the log file."""

        self.file.close()