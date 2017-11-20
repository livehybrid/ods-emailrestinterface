from abc import ABCMeta, abstractmethod


class QueueReader(metaclass=ABCMeta):

    @abstractmethod
    def __init__(self, sender):
        pass

    @abstractmethod
    def watch_queue(self):
        pass

    @abstractmethod
    def get_message(self):
        pass
