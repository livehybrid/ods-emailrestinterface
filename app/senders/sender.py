from abc import ABCMeta, abstractmethod

class Sender(metaclass=ABCMeta):

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def send_message(self, message):
        pass

    @abstractmethod
    def is_valid_message(self, message):
        pass
