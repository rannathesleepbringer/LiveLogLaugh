import logging.config
import json
import logging.handlers
import atexit
import datetime as dt
import logging
import pathlib
import platform

logger = logging.getLogger(__name__)
LOG_RECORD_BUILTIN_ATTRS = {
    "args",
    "asctime",
    "created",
    "exc_info",
    "exc_text",
    "filename",
    "funcName",
    "levelname",
    "levelno",
    "lineno",
    "module",
    "msecs",
    "message",
    "msg",
    "name",
    "pathname",
    "process",
    "processName",
    "relativeCreated",
    "stack_info",
    "thread",
    "threadName",
    "taskName",
}
def versiontuple(v):
    return tuple(map(int, (v.split("."))))

class MyJSONFormatter(logging.Formatter):
    def __init__(
        self,
        *,
        fmt_keys: dict[str, str] | None = None,
    ):
        super().__init__()
        self.fmt_keys = fmt_keys if fmt_keys is not None else {}

    def format(self, record: logging.LogRecord) -> str:
        message = self._prepare_log_dict(record)
        return json.dumps(message, default=str)

    def _prepare_log_dict(self, record: logging.LogRecord):
        always_fields = {
            "message": record.getMessage(),
            "timestamp": dt.datetime.fromtimestamp(
                record.created, tz=dt.timezone.utc
            ).isoformat(),
        }
        if record.exc_info is not None:
            always_fields["exc_info"] = self.formatException(record.exc_info)

        if record.stack_info is not None:
            always_fields["stack_info"] = self.formatStack(record.stack_info)

        message = {
            key: msg_val
            if (msg_val := always_fields.pop(val, None)) is not None
            else getattr(record, val)
            for key, val in self.fmt_keys.items()
        }
        message.update(always_fields)

        for key, val in record.__dict__.items():
            if key not in LOG_RECORD_BUILTIN_ATTRS:
                message[key] = val

        return message


class NonErrorFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool | logging.LogRecord:
        return record.levelno <= logging.INFO

# logging.config.dictConfig(config=logging_config)
class love:
    def __init__(self, func) -> None:
        self.func = func
    def __call__(self, *args, **kwargs):
        if versiontuple(platform.python_version()) >=  versiontuple("3.12.0"):

            config_file = pathlib.Path("queued-stderr-file.json")
            with open(config_file) as f_in:
                config = json.load(f_in)

            logging.config.dictConfig(config)

            queue_handler = logging.getHandlerByName("queue_handler")

            if queue_handler is not None:
                queue_handler.listener.start()
                atexit.register(queue_handler.listener.stop)
        else:
            config_file = pathlib.Path("stderr-file.json")
            with open(config_file) as f_in:
                config = json.load(f_in)

            logging.config.dictConfig(config)

                
        logging.basicConfig(level="INFO")
        # logger.debug("debug message", extra={"x": "hello"})
        # logger.info("info message")
        # logger.warning("warning message")
        # logger.error("error message")
        # logger.critical("critical message")

        try:
            logger.info(f"Function {self.func.__name__} completed Successfully", extra={"Function": f" {self.func.__name__}","Arguments":f"{args}", "Results":f"{self.func(*args,**kwargs)}"})
        except Exception as e:
            logger.exception(f"Exception occured", extra={"Exception:":e,"Function": f" {self.func.__name__}","Arguments":f"{args}"})
