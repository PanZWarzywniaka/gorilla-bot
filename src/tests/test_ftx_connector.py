
import unittest
import logging
from gorilla_bot.util.connectors.ftx_connector import FTXConnector


class FTXConnectorTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        logging.disable(logging.CRITICAL)

    @classmethod
    def tearDownClass(cls):
        logging.disable(logging.NOTSET)

    def setUp(self):
        self.ftx_connector = FTXConnector()

    def tearDown(self):
        pass

    def test_get_price(self):  # test method names begin with 'test'

        price = self.ftx_connector.get_price()
        self.assertIsNotNone(price)
        self.assertIsInstance(price, float)
        self.assertTrue(price >= 0)
