import unittest
import config
from mock import patch
from app.senders.sender import Sender
from app.senders.email_sender import NHSMailEmailSender
from smtplib import SMTPSenderRefused, SMTPAuthenticationError, SMTPRecipientsRefused, SMTPServerDisconnected
from socket import gaierror


class TestEmailSender(unittest.TestCase):

    def setUp(self):
        self.gethostbyname_patcher = patch('socket.gethostbyname').start()
        self.getfqdn_patcher = patch('socket.getfqdn').start()
        self.connect_patcher = patch('smtplib.SMTP.connect').start()
        self.starttls_patcher = patch('smtplib.SMTP.starttls').start()
        self.login_patcher = patch('smtplib.SMTP.login').start()

        self.connect_patcher.return_value = 220, 'some_message'

        self.worker_email_address_original_value = config.WORKER_EMAIL_ADDRESS
        self.worker_email_password_original_value = config.WORKER_EMAIL_PASSWORD
        self.email_gateway_uqi_original_value = config.EMAIL_GATWEWAY_URI
        config.WORKER_EMAIL_ADDRESS = 'test_worker@email.com'
        config.WORKER_EMAIL_PASSWORD = 'test-password'
        config.EMAIL_GATEWAY_URI = 'send.email:1234'

        self.test_message = {
            'first_name': 'Jane',
            'surname': 'Doe',
            'title': 'Mrs',
            'subject': 'test subject',
            'recipient_email_address': 'email@nhs.net',
            'mobile_number': '',
            'content': 'some test content'
        }

    def tearDown(self):
        self.gethostbyname_patcher.stop()
        self.getfqdn_patcher.stop()
        self.connect_patcher.stop()
        self.starttls_patcher.stop()
        self.login_patcher.stop()

        config.WORKER_EMAIL_ADDRESS = self.worker_email_address_original_value
        config.WORKER_EMAIL_PASSWORD = self.worker_email_password_original_value
        config.EMAIL_GATEWAY_URI = self.email_gateway_uqi_original_value

    def test__email_sender__EmailSender__IsSubclassOfAbstractSender(self):
        assert issubclass(NHSMailEmailSender, Sender)

    def test___EmailSender____init____DoesNotRaiseException__WhenCalled(self):

        try:
            NHSMailEmailSender()
        except:
            raise
        pass

    def test__email_sender__EmailSender____init____RaisesSMTPAuthenticationError__WhenWorkerEmailAddressIsIncorrect(self):

        config.WORKER_EMAIL_ADDRESS = '12345'

        self.login_patcher.side_effect = SMTPAuthenticationError(1, 'some_message')

        with self.assertRaises(SMTPAuthenticationError):
            NHSMailEmailSender()

    def test__email_sender__EmailSender____init____RaisesSMTPAuthenticationError__WhenWorkerEmailPasswordIsIncorrect(self):

        exception = SMTPAuthenticationError(1, 'some_message')
        self.login_patcher.side_effect = exception

        with self.assertRaises(SMTPAuthenticationError):
            NHSMailEmailSender()

    @patch('smtplib.SMTP.sendmail')
    @patch('smtplib.SMTP.__init__')
    def test__email_sender__EmailSender____init____RaisesGetAddressInfoError__WhenNHSMailGatewayAddressIsIncorrect(self, mock_smtp_client, mock_sendmail):

        mock_smtp_client.side_effect = gaierror

        with self.assertRaises(gaierror):
            NHSMailEmailSender()

    @patch('smtplib.SMTP.sendmail')
    @patch('app.senders.smtp_sender.MIMEText')
    def test__email_sender__EmailSender__send_message__CallsSendMailWithRecipientEmailAndContentWhenBothAreValid(self, mock_mimetext, mock_send_mail):

        mock_mimetext_instance = mock_mimetext.return_value
        recipient_email = self.test_message['recipient_email_address']

        sender = NHSMailEmailSender()
        sender.send_message(self.test_message)

        mock_send_mail.assert_called_with('test_worker@email.com', [recipient_email], mock_mimetext_instance.as_string())

    def test__email_sender__EmailSender__send_message__ReturnsNone__WhenRecipientIsNone(self):

        sender = NHSMailEmailSender()

        invalid_message = self.test_message
        invalid_message['recipient_email_address'] = None
        result = sender.send_message(invalid_message)

        self.assertIsNone(result)

    def test__email_sender__EmailSender__send_message__ReturnsNone__WhenRecipientIsEmpty(self):

        sender = NHSMailEmailSender()
        invalid_message = self.test_message
        invalid_message['recipient_email_address'] = ''
        result = sender.send_message(invalid_message)

        self.assertIsNone(result)

    def test__email_sender__EmailSender__send_message__ReturnsNone__WhenNoEmailContentIsNone(self):

        sender = NHSMailEmailSender()
        invalid_message = self.test_message
        invalid_message['content'] = None
        result = sender.send_message(invalid_message)

        self.assertIsNone(result)

    def test__email_sender__EmailSender__send_message__ReturnsNone__WhenEmailContentIsEmpty(self):

        sender = NHSMailEmailSender()
        invalid_message = self.test_message
        invalid_message['content'] = ''
        result = sender.send_message(invalid_message)

        self.assertIsNone(result)

    def test__email_sender__EmailSender__send_message__ReturnsNone__WhenEmailSubjectIsNone(self):
        sender = NHSMailEmailSender()
        invalid_message = self.test_message
        invalid_message['subject'] = None
        result = sender.send_message(invalid_message)

        self.assertIsNone(result)

    def test__email_sender__EmailSender__send_message__ReturnsNone__WhenEmailSubjectIsEmpty(self):
        sender = NHSMailEmailSender()
        invalid_message = self.test_message
        invalid_message['subject'] = ''
        result = sender.send_message(invalid_message)

        self.assertIsNone(result)

    @patch('smtplib.SMTP.sendmail')
    def test__email_sender__EmailSender__send_message__RaisesSMTPSenderRefused__WhenTLSConnectionNotEstablished(self, mock_send_mail):

        exception = SMTPSenderRefused(1, 'some_message', 'some_sender')
        mock_send_mail.side_effect = exception

        sender = NHSMailEmailSender()

        self.assertRaises(SMTPSenderRefused, sender.send_message, self.test_message)

    @patch('smtplib.SMTP.sendmail')
    def test__email_sender__EmailSender__send_message__RaisesSMTPRecipientsRefused__WhenUserAddressIsIncorrect(self, mock_send_mail):

        exception = SMTPRecipientsRefused(['some_recipients'])
        mock_send_mail.side_effect = exception

        sender = NHSMailEmailSender()

        self.assertRaises(SMTPRecipientsRefused, sender.send_message, self.test_message)

    @patch('smtplib.SMTP.sendmail')
    def test__email_sender__EmailSender__send_message__RaisesSMTPServerDisconnected(self, mock_send_mail):

        exception = SMTPServerDisconnected
        mock_send_mail.side_effect = exception

        sender = NHSMailEmailSender()

        self.assertRaises(SMTPServerDisconnected, sender.send_message, self.test_message)
