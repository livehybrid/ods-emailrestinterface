from app.readers.queue_reader import QueueReader
from app.message_handler import MessageHandler
from app.constants import MESSAGE_FIELD_SUBJECT, MESSAGE_FIELD_EMAIL, MESSAGE_FIELD_MOBILE, MESSAGE_FIELD_ONETIME_PASS, MESSAGE_FIELD_GUID, MESSAGE_TEMPLATE


class SingleReader(QueueReader):

    def __init__(self, sender, getParams, templateFile):
        self.handler = MessageHandler(sender)
        message = self.get_message(getParams, templateFile)

        self.handler.handle(message)

    def get_message(self, getParams, templateFile):
        message = {
            MESSAGE_FIELD_ONETIME_PASS: getParams['code'],
            MESSAGE_FIELD_SUBJECT: 'ODS One Time Password',
            MESSAGE_FIELD_EMAIL: getParams['destination'],
            MESSAGE_FIELD_GUID: getParams['guid'],
            MESSAGE_TEMPLATE: templateFile
        }
        return message

    def watch_queue(self):
        #Not used for single message, this is only used when reading from a queue
        return False
