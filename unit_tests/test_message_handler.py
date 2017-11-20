import unittest
from socket import gaierror
from mock import MagicMock, patch
from app.message_handler import MessageHandler
from smtplib import SMTPSenderRefused, SMTPAuthenticationError, SMTPServerDisconnected, SMTPRecipientsRefused
from app.senders.email_sender import NHSMailEmailSender


class TestMessageHandler(unittest.TestCase):

    def test__message_handler__MessageHandler____init____exposesInjectedSender(self):
        mock_sender = MagicMock(spec=NHSMailEmailSender).return_value

        handler = MessageHandler(mock_sender)

        self.assertEqual(mock_sender, handler.sender)

    @patch('app.message_handler.MessageHandler.send')
    def test__message_handler__MessageHandle__handle__populatesAndSendsTemplate__whenCalledWithValidMessage(self, mock_send):

        mock_sender = MagicMock(spec=NHSMailEmailSender).return_value
        handler = MessageHandler(mock_sender)
        message = {
            'first_name': 'Jane',
            'surname': 'Doe',
            'title': 'Mrs',
            'subject': 'test',
            'recipient_email_address': 'email@nhs.net',
            'mobile_number': '',
            'content': 'dummy_content',
            'onetime_pass': 'timmy_the_password'
        }
        templated_message = message
        templated_message['content'] = 'Dear Mrs Jane Doe\n    ' \
                                       'Welcome to NDOP your one time passcode is:\n           ' \
                                       'timmy_the_password\n\n    ' \
                                       'Many Thanks,\n        ' \
                                       'Your mates at NDOP'

        handler.handle(message)

        mock_send.assert_called_with(templated_message)

    @patch('app.message_handler.LOGGER.warning')
    @patch('app.message_handler.MessageHandler.send')
    @patch('app.comms_builder.populate_template')
    def test__message_handler__MessageHandler__handle__logsError__whenSMTPRecipientsRefusedIsRaised(self, mock_templater, mock_send, mock_logger):

        mock_sender = MagicMock(spec=NHSMailEmailSender).return_value
        handler = MessageHandler(mock_sender)
        mock_send.side_effect = SMTPRecipientsRefused(['some_recipients'])

        handler.handle({})

        assert mock_logger.called

    def test__message_handler__MessageHandler__send__sendsMessage__whenCalled(self):

        mock_sender = MagicMock(spec=NHSMailEmailSender).return_value
        handler = MessageHandler(mock_sender)
        dummy_message = {}

        handler.send(dummy_message)

        handler.sender.send_message.assert_called_with(dummy_message)

    @patch('app.message_handler.LOGGER.warning')
    def test__message_handler__MessageHandler__send__logsError__whenSMTPSenderRefusedIsRaised(self, mock_logger):

        mock_sender = MagicMock(spec=NHSMailEmailSender).return_value
        handler = MessageHandler(mock_sender)
        dummy_message = {}
        handler.sender.send_message.side_effect = SMTPSenderRefused(1, 'some_message', 'some_sender')

        handler.send(dummy_message)

        assert mock_logger.called

    @patch('app.message_handler.LOGGER.warning')
    def test__message_handler__MessageHandler__send__logsError__whenSMTPAuthenticationErrorIsRaised(self, mock_logger):

        mock_sender = MagicMock(spec=NHSMailEmailSender).return_value
        handler = MessageHandler(mock_sender)
        dummy_message = {}
        handler.sender.send_message.side_effect = SMTPAuthenticationError(1, 'some_message')

        handler.send(dummy_message)

        assert mock_logger.called

    @patch('app.message_handler.LOGGER.warning')
    def test__message_handler__MessageHandler__send__logsError__whenSMTPServerDisconnectedIsRaised(self, mock_logger):

        mock_sender = MagicMock(spec=NHSMailEmailSender).return_value
        handler = MessageHandler(mock_sender)
        dummy_message = {}
        handler.sender.send_message.side_effect = SMTPServerDisconnected

        handler.send(dummy_message)

        assert mock_logger.called

    @patch('app.message_handler.LOGGER.warning')
    def test__message_handler__MessageHandler__send__logsError__whenGetAddressInfoErrorIsRaised(self, mock_logger):

        mock_sender = MagicMock(spec=NHSMailEmailSender).return_value
        handler = MessageHandler(mock_sender)
        dummy_message = {}
        handler.sender.send_message.side_effect = gaierror

        handler.send(dummy_message)

        assert mock_logger.called