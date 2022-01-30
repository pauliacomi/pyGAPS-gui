import logging

logging.captureWarnings(True)
from io import StringIO


class LogHook():

    log_stream = None
    logger = None
    handler = None

    def __init__(self):
        self.log_stream = StringIO()
        self.logger = logging.getLogger('pygaps')
        self.handler = logging.StreamHandler(stream=self.log_stream)
        self.handler.setLevel(logging.INFO)

    def __enter__(self):
        self.logger.addHandler(self.handler)
        return self

    def __exit__(self, type, value, traceback):
        self.logger.removeHandler(self.handler)
        return True

    def getLogs(self):
        logs = self.log_stream.getvalue().replace("\n", "<br>")
        self.log_stream.truncate(0)
        self.log_stream.seek(0)
        if logs:
            return f'<font color="magenta">Warning: {logs}</font>'
        else:
            return ''


log_hook = LogHook()
