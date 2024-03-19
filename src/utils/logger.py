import json
from enum import Enum


class LogLevel(Enum):
    INFO = 'INFO'
    WARNING = 'WARNING'
    ERROR = 'ERROR'
    FATAL = 'FATAL'


class Logger:
    serviceName: str

    def __init__(self, serviceName: str) -> None:
        self.serviceName = serviceName

    def _log(self, event_name: str, level: LogLevel, properties: dict) -> None:
        output = {
            'service': self.serviceName,
            'event': event_name,
            'properties': str(properties),
            'level': level.value,
        }

        data = json.dumps(output)
        print(data)

    def info(self, event_name: str, properties: dict = {}) -> None:
        self._log(event_name, LogLevel.INFO, properties)

    def warning(self, event_name: str, properties: dict = {}) -> None:
        self._log(event_name, LogLevel.WARNING, properties)

    def error(self, event_name: str, properties: dict = {}) -> None:
        self._log(event_name, LogLevel.ERROR, properties)

    def fatal(self, event_name: str, properties: dict = {}) -> None:
        self._log(event_name, LogLevel.FATAL, properties)
