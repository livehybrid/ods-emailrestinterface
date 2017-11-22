""" This module is the root of the application and contains the main startup class."""
import os
import logging
import tornado.ioloop
import tornado.web
import tornado.httpserver
#from app.readers.stub_queue_reader import StubReader
from app.constants import CONFIG_WORKER_MODE_EMAIL, CONFIG_EMAIL_OTP_TEMPLATE_NAME,\
    CONFIG_WORKER_MODE_SMS, CONFIG_SMS_OTP_TEMPLATE_NAME, MOBILE_NUMBER_COUNTRY_CODE
from app.senders.email_sender import NHSMailEmailSender
from app.senders.sms_sender import NHSMailSMSSender
from app.readers.single_reader import SingleReader

import config
from app.log_handlers import DefaultStreamHandler

__STATIC_RESOURCE_PATH = os.path.join(os.path.dirname(__file__), "app/static")


def get_app():
    """ This function returns an instance of the application with app routing."""
    settings = {
        "static_path": __STATIC_RESOURCE_PATH
    }
    application = tornado.web.Application([
	(r"/ping", reqPing),
	(r"/send", reqSend)
    ], **settings)

    return application

class reqPing(tornado.web.RequestHandler):
    def get(self):
        logging.info("Got Ping request! Sending Pong!")
        response = "pong"
        self.write(response)

class reqSend(tornado.web.RequestHandler):
    def get(self):
        getParams = {
          "code": self.get_argument("code"),
          "guid": self.get_argument("guid"),
          "destination": self.get_argument("destination")
        }
        response = "OKAY"
        #//If Begins with 0 and is 11 chars long then SMS
        #//If Begins with +44 and is 13 chars long with no @ then SMS
        #//If is email address then EMAIL
        
        if ((getParams['destination'][0:3] == MOBILE_NUMBER_COUNTRY_CODE) and len(getParams['destination'])==13):
            #Type is SMS with +44 at the beginning
            sendType = CONFIG_WORKER_MODE_SMS
            sender = NHSMailSMSSender()
            messageTemplate = CONFIG_SMS_OTP_TEMPLATE_NAME
        elif (getParams['destination'][0] == "0") and len(getParams['destination']) == 11:
            #Type is SMS with 0 at front
            sendType = CONFIG_WORKER_MODE_SMS
            sender = NHSMailSMSSender()
            messageTemplate = CONFIG_SMS_OTP_TEMPLATE_NAME
        else:
            sender = NHSMailEmailSender()
            sendType = CONFIG_WORKER_MODE_EMAIL
            messageTemplate = CONFIG_EMAIL_OTP_TEMPLATE_NAME

        #SingleReader reads a single email/sms from the get parameters of the request
        SingleReader(sender, getParams, messageTemplate)

        self.write(response)


def do_setup():
    """Setup for the application."""
    logger = logging.getLogger()
#    logger.setLevel(logging.INFO)
    logger.setLevel(logging.DEBUG)
    handler = DefaultStreamHandler()
    logger.addHandler(handler)
    logger.info('configured logger')

    application = get_app()
    logger.info('created application')

    http_server = tornado.httpserver.HTTPServer(application)

    http_server.listen(config.PORT)
    logger.info('listening on port: %d', config.PORT)


if __name__ == "__main__":
    do_setup()
    tornado.ioloop.IOLoop.current().start()
    logging.getLogger().info('started tornado')
