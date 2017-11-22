from socket import gaierror
from app.comms_builder import populate_template
from smtplib import SMTPSenderRefused, SMTPAuthenticationError, SMTPServerDisconnected, SMTPRecipientsRefused
import logging
from app.constants import MESSAGE_FIELD_CONTENT, MESSAGE_FIELD_GUID


LOGGER = logging.getLogger()


class MessageHandler:

    def __init__(self, sender):
        self.sender = sender

    def handle(self, message):
        #Do we know the template type yet?
        message[MESSAGE_FIELD_CONTENT] = populate_template(message)
        try:
            self.send(message)

        except SMTPRecipientsRefused:
            LOGGER.warning('invalid recipient email address')

    def send(self, message):
        try:
            self.sender.send_message(message)
            LOGGER.info("Message sent for guid=%s" % message[MESSAGE_FIELD_GUID])
        except (SMTPSenderRefused, SMTPAuthenticationError,
                gaierror, SMTPServerDisconnected):
            LOGGER.warning('could not connect to email gateway ' + str(Exception))
