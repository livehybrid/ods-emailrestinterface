import logging
from app.senders.smtp_sender import SMTPSender


LOGGER = logging.getLogger()


class NHSMailEmailSender(SMTPSender):

    def __init__(self):
        super().__init__()

    def send_message(self, message):
        if self.is_valid_message(message):
            super().send_via_smtp(message)

    def is_valid_message(self, message):
        return super().is_valid_email_message(message)
