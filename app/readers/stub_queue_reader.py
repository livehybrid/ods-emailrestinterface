from app.message_handler import MessageHandler
from app.readers.queue_reader import QueueReader
from app.constants import MESSAGE_FIELD_FIRST_NAME, MESSAGE_FIELD_SURNAME, MESSAGE_FIELD_TITLE, \
    MESSAGE_FIELD_SUBJECT, MESSAGE_FIELD_EMAIL, MESSAGE_FIELD_MOBILE, MESSAGE_FIELD_CONTENT,\
    MESSAGE_FIELD_ONETIME_PASS


class StubReader(QueueReader):

    def __init__(self, sender):
        self.handler = MessageHandler(sender)
        self.watch_queue()

    def watch_queue(self):

        for i in range(0, 3):
            message = self.get_message()

            self.handler.handle(message)

    def get_message(self):

        message = {
            MESSAGE_FIELD_FIRST_NAME: 'Jane',
            MESSAGE_FIELD_SURNAME: 'Doe',
            MESSAGE_FIELD_TITLE: 'Mrs',
            MESSAGE_FIELD_SUBJECT: 'test',
            MESSAGE_FIELD_EMAIL: 'adam.brown14@nhs.net',
            MESSAGE_FIELD_MOBILE: '',
            MESSAGE_FIELD_CONTENT: 'dummy_content',
            MESSAGE_FIELD_ONETIME_PASS: 'timmy_the_password'
        }

        return message
