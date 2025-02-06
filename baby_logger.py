"""
@author: CH3CKMATE-2002
@description: Simplest logger in the world, for fun purposes!
"""

from enum import Enum
from colorama import Fore, Style, init
from datetime import datetime

# Initialize colorama
init()


class LogLevel(Enum):
    DEBUG = 3
    WARNING = 2
    INFO = 1
    ERROR = 0
    SILENT = -1


class Logger():
    def __init__(self, verbosity=LogLevel.ERROR, template="[{level} - {timestamp}]: {message}") -> None:
        self.verbosity_level = verbosity
        self.template = template

    def log(self, level: LogLevel, message: str):
        if level.value <= self.verbosity_level.value:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            color = {
                LogLevel.DEBUG:   Fore.GREEN,
                LogLevel.WARNING: Fore.YELLOW,
                LogLevel.INFO:    Fore.BLUE,
                LogLevel.ERROR:   Fore.RED
            }.get(level, Fore.WHITE)

            log_message = self.template.format(
                timestamp=f'{Fore.MAGENTA}{timestamp}{Style.RESET_ALL}',
                level=f'{color}{level.name:<7}{Style.RESET_ALL}',
                message=message,
            )

            print(log_message)

    def debug(self, message: str):
        self.log(LogLevel.DEBUG, message)

    def warning(self, message: str):
        self.log(LogLevel.WARNING, message)

    def info(self, message: str):
        self.log(LogLevel.INFO, message)

    def error(self, message: str):
        self.log(LogLevel.ERROR, message)
