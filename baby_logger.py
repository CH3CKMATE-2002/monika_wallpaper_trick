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
    def __init__(
            self,
            name = '',
            verbosity = LogLevel.ERROR,
            template="[{level} @ {name} - {timestamp}]: {message}",
            no_color=False
    ) -> None:
        self.name = name
        self.verbosity_level = verbosity
        self.template = template
        self.no_color = no_color

    def log(self, level: LogLevel, message: str):
        if level.value <= self.verbosity_level.value:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            level_color = '' if self.no_color else {
                LogLevel.DEBUG:   Fore.GREEN,
                LogLevel.WARNING: Fore.YELLOW,
                LogLevel.INFO:    Fore.BLUE,
                LogLevel.ERROR:   Fore.RED
            }.get(level, Fore.WHITE)

            name_color = '' if self.no_color else Fore.CYAN

            timestamp_color = '' if self.no_color else Fore.MAGENTA

            reset = '' if self.no_color else Style.RESET_ALL

            log_message = self.template.format(
                name=f'{name_color}{self.name}{reset}',
                level=f'{level_color}{level.name:<7}{reset}',
                timestamp=f'{timestamp_color}{timestamp}{reset}',
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


global_logger = Logger(
    verbosity=LogLevel.DEBUG,
    template='[{level} - {timestamp}]: {message}',
)
