import logging
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
        return self.log_stream.getvalue()
