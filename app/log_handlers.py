"""This module contains a log handler for adding a request ID to incoming requests."""
import logging
import json
import sys


class RequestsLogHandler(logging.StreamHandler):
    """This class represents a handler which adds a request ID to the logs it emits."""
    def __init__(self, request_id):
        self.request_id = request_id
        super().__init__()

        self.stream = sys.stdout

        formatter = logging.Formatter('%(asctime)s - %(levelname)s: %(message)s')
        self.setFormatter(formatter)

    def format(self, record):
        vanilla = super().format(record)

        data = json.dumps({"request_id": self.request_id})

        return '{0} {1}'.format(vanilla, data)


class DefaultStreamHandler(logging.StreamHandler):
    """This class is the default log handler for when the service starts up."""

    def __init__(self):
        super().__init__()

        self.stream = sys.stdout

        formatter = logging.Formatter('%(asctime)s - %(levelname)s: %(message)s')
        self.setFormatter(formatter)
