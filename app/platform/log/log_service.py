from app.platform.instantiation.disposable import Disposable

from enum import Enum


class LogLevel(Enum):
    Off = 0,
    Info = 1,
    Debug = 2,
    Warning = 3,
    Error = 4,
    Critical = 5


class LogService(Disposable):
    def __init__(self, log_level: LogLevel):
        self.log_level = log_level

    def info(self, message):
        if self.log_level >= LogLevel.Info:
            print('[INFO]' + message)

    def debug(self, message):
        if self.log_level >= LogLevel.Debug:
            print('[DEBUG]' + message)

    def warn(self, message):
        if self.log_level >= LogLevel.Warning:
            print('[WARN]' + message)

    def error(self, message):
        if self.log_level >= LogLevel.Error:
            print('[ERROR]' + message)

    def critical(self, message):
        if self.log_level >= LogLevel.Critical:
            print('[CRITICAL]' + message)
