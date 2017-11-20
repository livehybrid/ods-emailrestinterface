import unittest
from mock import MagicMock

from app.readers.queue_reader import QueueReader
from app.readers.stub_queue_reader import StubReader
from app.senders.email_sender import NHSMailEmailSender


class TestStubReader(unittest.TestCase):

    def test__stub_queue_reader__StubReader__IsASubclassOfQueueReader(self):
        assert issubclass(StubReader, QueueReader)

    def test_stub_reader__StubReader__DoesNotRaiseExceptionWhenInstantiatedWithEmail(self):

        sender = MagicMock(spec=NHSMailEmailSender)
        try:
            StubReader(sender)
        except:
            raise
        pass
