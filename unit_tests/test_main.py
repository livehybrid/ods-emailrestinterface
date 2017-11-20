""" Unit tests for the main entry point for the authorize service. """
import unittest
import mock
import main
import config


class TestMain(unittest.TestCase):

    @mock.patch('main.setup_worker')
    @mock.patch('tornado.httpserver.HTTPServer.listen')
    @mock.patch('main.get_app')
    @mock.patch('logging.Logger.info')
    def test__do_setup__will_call_logger_info__when_called(self, mock_logger_info,
                                                           mock_get_application,
                                                           mock_app_listen,
                                                           mock_setup_worker):

        main.do_setup()
        mock_logger_info.assert_called_with('listening on port: %d', config.PORT)

    @mock.patch('main.setup_worker')
    @mock.patch('tornado.httpserver.HTTPServer.listen')
    @mock.patch('main.get_app')
    @mock.patch('logging.Logger.info')
    def test__do_setup__will_call_get_application__when_called(self,
                                                               mock_logger_info,
                                                               mock_get_application,
                                                               mock_app_listen,
                                                               mock_setup_worker):

        main.do_setup()
        mock_get_application.assert_called_with()

    @mock.patch('main.setup_worker')
    @mock.patch('tornado.httpserver.HTTPServer.listen')
    @mock.patch('logging.Logger.info')
    def test__do_setup__will_call_listen__when_called(self,
                                                      mock_logger_info,
                                                      mock_app_listen,
                                                      mock_setuo_worker):

        main.do_setup()
        mock_app_listen.assert_called_with(config.PORT)
