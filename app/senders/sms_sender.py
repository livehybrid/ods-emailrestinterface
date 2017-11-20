import logging
from app.senders.smtp_sender import SMTPSender
from app.constants import MESSAGE_FIELD_EMAIL, MESSAGE_FIELD_MOBILE, \
    MOBILE_NUMBER_COUNTRY_CODE
import config

LOGGER = logging.getLogger()


class NHSMailSMSSender(SMTPSender):

    def __init__(self):
        super().__init__()

    def send_message(self, message):

        if not self.is_valid_message(message):
            return None

        message[MESSAGE_FIELD_EMAIL] = self.mobile_number + \
            config.SMS_RECIPIENT_EMAIL_SUFFIX

        super().send_via_smtp(message)

    def is_valid_message(self, message):
        if not self.__is_valid_mobile_number(message[MESSAGE_FIELD_MOBILE]):
            return None

        return super().is_valid_email_message(message)

    def __is_valid_mobile_number(self, mobile_number):

        if mobile_number[0:3] == MOBILE_NUMBER_COUNTRY_CODE:
            self.mobile_number = mobile_number

        if mobile_number[0] == '0':
            without_country_code = mobile_number[1::]
            mobile_number = MOBILE_NUMBER_COUNTRY_CODE + without_country_code
            self.mobile_number = mobile_number

        if len(self.mobile_number) != 13:
            return False

        return True
