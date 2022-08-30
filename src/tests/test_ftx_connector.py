from gorilla_bot.util.connectors.ftx_connector import FTXConnector
from tests.gorilla_test_case import GorillaTestCase


class FTXConnectorTestCase(GorillaTestCase):

    def setUp(self):
        self.ftx_connector = FTXConnector()

    def tearDown(self):
        pass

    def test_get_price(self):  # test method names begin with 'test'

        price = self.ftx_connector.get_price()
        self.assertIsNotNone(price)
        self.assertIsInstance(price, float)
        self.assertTrue(price >= 0)
