import sys
import threading
from enum import Enum
from colorama import Fore, Style, init
from datetime import datetime
from typing import Union, TextIO

# Initialize colorama
init()

class LogLevel(Enum):
    """
@author: CH3CKMATE-2002
@contributor: Atlas
    Enum representing different log levels.
    """
    TRACE = 8
    DEBUG = 7
    SUCCESS = 6
    WARNING = 5
    NOTICE = 4
    INFO = 3
    ERROR = 2
    CRITICAL = 1
    SILENT = 0

    @staticmethod
    def get(value: Union[int, str]) -> 'LogLevel':
        """
        Retrieves the LogLevel from an integer or string value.
        """
        if isinstance(value, int):
            try:
                return LogLevel(value)
            except:
                raise ValueError(f'Invalid logging level {value} (should be between -2 and 6)')
        
        value = value.lower()
        if 'trace'.startswith(value):
            return LogLevel.TRACE
        elif 'debug'.startswith(value):
            return LogLevel.DEBUG
        elif 'success'.startswith(value):
            return LogLevel.SUCCESS
        elif 'warning'.startswith(value):
            return LogLevel.WARNING
        elif 'notice'.startswith(value):
            return LogLevel.NOTICE
        elif 'info'.startswith(value):
            return LogLevel.INFO
        elif 'error'.startswith(value):
            return LogLevel.ERROR
        elif 'critical'.startswith(value):
            return LogLevel.CRITICAL
        else:
            return LogLevel.SILENT

class OmegaLogger():
    """
@author: CH3CKMATE-2002
@contributor: Atlas
    A simple and flexible logging class that supports colorized output, verbosity levels,
    and logging to different output streams.
    """
    def __init__(
            self,
            name: str = '',
            template: str = "[{level} @ {name} - {timestamp}]: {message}",
            verbosity: LogLevel = LogLevel.ERROR,
            stream: TextIO = sys.stdout,
            force_no_color: bool = False,
            timestamp_format: str = "%Y-%m-%d %H:%M:%S"
    ) -> None:
        """
        Initializes the Logger instance.
        """
        self.name = name
        self.template = template
        self._verbosity_level = verbosity
        self._stream = stream
        self._force_no_color = force_no_color
        self._timestamp_format = timestamp_format
        self._lock = threading.Lock()

    @property
    def no_color(self) -> bool:
        """
        Determines whether colorized output is disabled.
        """
        return self._force_no_color or not self._stream.isatty()

    @no_color.setter
    def no_color(self, value: bool) -> None:
        """
        Allows the user to explicitly disable colorized output.
        """
        self._force_no_color = value

    @property
    def stream(self) -> TextIO:
        """
        Retrieves the current output stream.
        """
        return self._stream

    @stream.setter
    def stream(self, value: TextIO) -> None:
        """
        Sets a new output stream.
        """
        self._stream = value

    @property
    def timestamp_format(self) -> str:
        """
        Retrieves the current timestamp format.
        """
        return self._timestamp_format

    @timestamp_format.setter
    def timestamp_format(self, value: str) -> None:
        """
        Allows the user to set a custom timestamp format.
        """
        self._timestamp_format = value
    
    @property
    def verbosity(self) -> LogLevel:
        return self._verbosity_level
    
    @verbosity.setter
    def verbosity(self, value: Union[int, str, LogLevel]):
        """
        Sets the verbosity level for logging.
        """
        if isinstance(value, (int, str)):
            value = LogLevel.get(value)
        self._verbosity_level = value

    def log(self, level: LogLevel, message: str) -> None:
        """
        Logs a message at the specified log level.
        """
        if level.value <= self._verbosity_level.value:
            timestamp = datetime.now().strftime(self._timestamp_format)

            level_color = '' if self.no_color else {
                LogLevel.TRACE:   Fore.CYAN,
                LogLevel.DEBUG:   Fore.GREEN,
                LogLevel.SUCCESS: Fore.LIGHTGREEN_EX,
                LogLevel.WARNING: Fore.YELLOW,
                LogLevel.NOTICE:  Fore.LIGHTBLUE_EX,
                LogLevel.INFO:    Fore.BLUE,
                LogLevel.ERROR:   Fore.RED,
                LogLevel.CRITICAL: Fore.LIGHTRED_EX
            }.get(level, Fore.WHITE)

            name_color = '' if self.no_color else Fore.CYAN
            timestamp_color = '' if self.no_color else Fore.MAGENTA
            reset = '' if self.no_color else Style.RESET_ALL

            log_message = self.template.format(
                name=f'{name_color}{self.name}{reset}',
                level=f'{level_color}{level.name:<8}{reset}',
                timestamp=f'{timestamp_color}{timestamp}{reset}',
                message=message,
            )

            with self._lock:
                self._stream.write(log_message + '\n')
                self._stream.flush()
    
    def trace(self, message: str):
        self.log(LogLevel.TRACE, message)
    
    def debug(self, message: str):
        self.log(LogLevel.DEBUG, message)
    
    def success(self, message: str):
        self.log(LogLevel.SUCCESS, message)

    def warning(self, message: str):
        self.log(LogLevel.WARNING, message)
    
    def notice(self, message: str):
        self.log(LogLevel.NOTICE, message)

    def info(self, message: str):
        self.log(LogLevel.INFO, message)

    def error(self, message: str):
        self.log(LogLevel.ERROR, message)
    
    def critical(self, message: str):
        self.log(LogLevel.CRITICAL, message)


# Global Logger Instance
global_logger = OmegaLogger(
    verbosity=LogLevel.DEBUG,
    template='[{level} - {timestamp}]: {message}',
)


if __name__ == '__main__':
    logger = OmegaLogger(name='Testing', verbosity=LogLevel.TRACE)
    logger.trace('Tracing callbacks')
    logger.debug('Calculating decals')
    logger.success('Task failed successfully')
    logger.warning('Uh-oh... Something is about to happen')
    logger.notice('I love you')
    logger.info('Did you know that bananas?')
    logger.error('Ouch!')
    logger.critical('FATAL ERROR! SEGMENTATION FAULT!')