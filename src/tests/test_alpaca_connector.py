from gorilla_bot.util.connectors.alpaca_connector import AlpacaConnector
from tests.gorilla_test_case import GorillaTestCase


class AlpacaConnectorTestCase(GorillaTestCase):

    def setUp(self):
        self.conn = AlpacaConnector()

    def tearDown(self):
        pass

    def test_open_position(self):
        self.assertTrue(True)
        order_info = self.conn.open_position("BTCUSD", 100)
        price = float(order_info['filled_avg_price'])
        self.assertIsNotNone(price)
        self.assertIsInstance(price, float)
        self.assertTrue(price >= 0)
