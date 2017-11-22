""" This module contains config variables required for running the service. """
import os

# SERVICE CONFIG
PORT = int(os.environ.get('MESSAGE_WORKER_PORT', 10010))
TEMPLATE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), 'app', 'templates'))
OTP_TEMPLATE_NAME = None
CONFIRMATION_TEMPLATE_NAME = None
EMAIL_GATWEWAY_URI = os.environ.get('MESSAGE_WORKER_EMAIL_GATEWAY_URI', 'http://stub-email-gateway.co.uk')
SMS_RECIPIENT_EMAIL_SUFFIX = os.environ.get('SMS_RECIPIENT_EMAIL_SUFFIX', '@sms.nhs.net')
WORKER_EMAIL_ADDRESS = os.environ.get('MESSAGE_WORKER_EMAIL_ADDRESS', 'ods.test@email.net')
WORKER_EMAIL_PASSWORD = os.environ.get('MESSAGE_WORKER_EMAIL_PASSWORD', 'stub-password')
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', True)
EMAIL_LOGIN = os.environ.get('EMAIL_LOGIN', True)
