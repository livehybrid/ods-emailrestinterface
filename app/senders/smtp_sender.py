import smtplib
from email.mime.text import MIMEText
import logging
from abc import abstractmethod

from app.senders.sender import Sender
from app.constants import MESSAGE_FIELD_EMAIL, MESSAGE_FIELD_CONTENT, MESSAGE_FIELD_SUBJECT,\
    MIMETEXT_FIELD_SUBJECT, MIMETEXT_FIELD_RECIPIENT_TO, MIMETEXT_FIELD_SENDER_FROM
import config

LOGGER = logging.getLogger()


class SMTPSender(Sender):

    def __init__(self):
        self.smtp_client = smtplib.SMTP(config.EMAIL_GATWEWAY_URI)
        self.smtp_client.starttls()
        self.worker_email = config.WORKER_EMAIL_ADDRESS
        self.smtp_client.login(self.worker_email,
                               config.WORKER_EMAIL_PASSWORD)

    @abstractmethod
    def send_message(self, message):
        pass

    def send_via_smtp(self, message):
        recipient = message[MESSAGE_FIELD_EMAIL]
        content = message[MESSAGE_FIELD_CONTENT]
        message_mimetext = MIMEText(content)
        smtp_client = self.smtp_client

        message_mimetext[MIMETEXT_FIELD_SUBJECT] = message[MESSAGE_FIELD_SUBJECT]
        message_mimetext[MIMETEXT_FIELD_SENDER_FROM] = self.worker_email
        message_mimetext[MIMETEXT_FIELD_RECIPIENT_TO] = recipient

        smtp_client.sendmail(self.worker_email,
                             [recipient],
                             message_mimetext.as_string())

        return True

    @staticmethod
    def is_valid_email_message(message):
        if not message[MESSAGE_FIELD_EMAIL]:
            LOGGER.error('no recipient provided in message')
            return False

        if not message[MESSAGE_FIELD_CONTENT]:
            LOGGER.error('no message content')
            return False

        if not message[MESSAGE_FIELD_SUBJECT]:
            LOGGER.error('no subject provided in message')
            return False

        return True
