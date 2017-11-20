import unittest

from app.readers.queue_reader import QueueReader


class TestQueueReader(unittest.TestCase):

    def test__queue_reader__QueueReader__implementations_do_not_raise_exception_on_instantiation_when_abstract_get_message_implemented(self):

        class ConcreteClass(QueueReader):
            def __init__(self):
                pass

            def watch_queue(self):
                pass

            def get_message(self):
                pass

        try:
            ConcreteClass()
        except TypeError:
            raise
        pass

    def test__queue_reader__QueueReader__implementations_raise_Typeerror_on_instantiation_when_abstract_get_message_not_implemented(self):

        class ConcreteClass(QueueReader):
            def incorrect_method(self):
                pass

        with self.assertRaises(TypeError):
            ConcreteClass()
