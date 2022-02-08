import logging

logging.captureWarnings(True)
from io import StringIO


class LogFilter():
    """Filter a log based on its level."""
    def __init__(self, level):
        self._level = level

    def filter(self, logRecord):
        """Perform filter on incoming log collection."""
        return logRecord.levelno <= self._level


class LogHook():
    """Ties in to the pyGAPS logging functionality and temporarily captures all output."""

    log_stream = None
    logger = None
    handler = None

    def __init__(self):
        self.log_stream = StringIO()
        self.logger = logging.getLogger('pygaps')
        self.infohandler = logging.StreamHandler(stream=self.log_stream)
        self.infohandler.setLevel(logging.INFO)
        self.infohandler.addFilter(LogFilter(logging.INFO))
        info_fmt = logging.Formatter("<font color=\"black\">%(message)s</font>")
        self.infohandler.setFormatter(info_fmt)
        self.warninghandler = logging.StreamHandler(stream=self.log_stream)
        self.warninghandler.setLevel(logging.WARNING)
        self.warninghandler.addFilter(LogFilter(logging.WARNING))
        warning_fmt = logging.Formatter("<font color=\"magenta\">Warning: %(message)s</font>")
        self.warninghandler.setFormatter(warning_fmt)
        self.errorhandler = logging.StreamHandler(stream=self.log_stream)
        self.errorhandler.setLevel(logging.ERROR)
        self.errorhandler.addFilter(LogFilter(logging.ERROR))
        error_fmt = logging.Formatter("<font color=\"red\">Error: %(message)s</font>")
        self.errorhandler.setFormatter(error_fmt)

    def __enter__(self):
        self.logger.addHandler(self.infohandler)
        self.logger.addHandler(self.warninghandler)
        self.logger.addHandler(self.errorhandler)
        return self

    def __exit__(self, type, value, traceback):
        self.logger.removeHandler(self.infohandler)
        self.logger.removeHandler(self.warninghandler)
        self.logger.removeHandler(self.errorhandler)
        return True

    def get_logs(self):
        """Get all logs during the capture as a string."""
        logs = self.log_stream.getvalue().replace("\n", "<br>")
        self.log_stream.truncate(0)
        self.log_stream.seek(0)
        if logs:
            return logs
        else:
            return ''


log_hook = LogHook()
