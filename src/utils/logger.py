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

    def _log(self, ctx: any, event_name: str, level: LogLevel, attributes: any) -> None:
        output = {
            'ctx': ctx,
            'event': event_name,
            'level': level.value,
            'service': self.serviceName,
            'properties': str(attributes),
        }

        data = json.dumps(output)
        print(data)

    def info(self, ctx: any, event_name: str, attributes: dict) -> None:
        self._log(ctx, event_name, LogLevel.INFO, attributes)

    def warning(self, ctx: any, event_name: str, attributes: dict) -> None:
        self._log(ctx, event_name, LogLevel.WARNING, attributes)

    def error(self, ctx: any, event_name: str, attributes: dict) -> None:
        self._log(ctx, event_name, LogLevel.ERROR, attributes)

    def fatal(self, ctx: any, event_name: str, attributes: dict) -> None:
        self._log(ctx, event_name, LogLevel.FATAL, attributes)
