""" This module is the root of the application and contains the main startup class."""
import os
import logging
import tornado.ioloop
import tornado.web
import tornado.httpserver
from app.readers.stub_queue_reader import StubReader
from app.constants import CONFIG_WORKER_MODE_EMAIL, CONFIG_EMAIL_OTP_TEMPLATE_NAME, CONFIG_EMAIL_CONFIRMATION_TEMPLATE_NAME,\
    CONFIG_WORKER_MODE_SMS, CONFIG_SMS_OTP_TEMPLATE_NAME, CONFIG_SMS_CONFIRMATION_TEMPLATE_NAME
from app.senders.email_sender import NHSMailEmailSender
from app.senders.sms_sender import NHSMailSMSSender

import config
from app.log_handlers import DefaultStreamHandler

__STATIC_RESOURCE_PATH = os.path.join(os.path.dirname(__file__), "app/static")


def get_app():
    """ This function returns an instance of the application with app routing."""
    settings = {
        "static_path": __STATIC_RESOURCE_PATH
    }
    application = tornado.web.Application([], **settings)

    return application


def setup_worker():

    sender = None

    if config.WORKER_MODE == CONFIG_WORKER_MODE_EMAIL:
        sender = NHSMailEmailSender()
        config.OTP_TEMPLATE_NAME = CONFIG_EMAIL_OTP_TEMPLATE_NAME
        config.CONFIRMATION_TEMPLATE_NAME = \
            CONFIG_EMAIL_CONFIRMATION_TEMPLATE_NAME

    if config.WORKER_MODE == CONFIG_WORKER_MODE_SMS:
        sender = NHSMailSMSSender()
        config.OTP_TEMPLATE_NAME = CONFIG_SMS_OTP_TEMPLATE_NAME
        config.CONFIRMATION_TEMPLATE_NAME = \
            CONFIG_SMS_CONFIRMATION_TEMPLATE_NAME

    StubReader(sender)


def do_setup():
    """Setup for the application."""
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    handler = DefaultStreamHandler()
    logger.addHandler(handler)
    logger.info('configured logger')

    application = get_app()
    logger.info('created application')

    http_server = tornado.httpserver.HTTPServer(application)

    http_server.listen(config.PORT)
    logger.info('listening on port: %d', config.PORT)
    setup_worker()


if __name__ == "__main__":
    do_setup()
    tornado.ioloop.IOLoop.current().start()
    logging.getLogger().info('started tornado')
