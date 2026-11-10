import unittest
from orderbook.engine import MatchingEngine


class TestMatchingEngine(unittest.TestCase):
    def setUp(self):
        self.engine = MatchingEngine(symbol="BTC-USDT")

    def test_limit_order_matching(self):
        # Place maker Sell order: 1.5 BTC @ 65,000 USDT
        maker_ask = self.engine.place_order("SELL", 65000.0, 1.5, order_id="ASK-1")
        self.assertEqual(maker_ask["status"], "OPEN")
        self.assertEqual(len(self.engine.asks), 1)

        # Place aggressive taker Buy order: 1.0 BTC @ 65,100 USDT
        taker_buy = self.engine.place_order("BUY", 65100.0, 1.0, order_id="BID-1")
        self.assertEqual(taker_buy["status"], "FILLED")
        self.assertEqual(len(taker_buy["trades"]), 1)
        self.assertEqual(taker_buy["trades"][0]["executed_price"], 65000.0)
        self.assertEqual(taker_buy["trades"][0]["executed_quantity"], 1.0)

        # Remaining ask in book should be 0.5 BTC
        self.assertEqual(self.engine.asks[0].remaining_quantity, 0.5)

    def test_spread_calculation(self):
        self.engine.place_order("BUY", 64000.0, 0.5)
        self.engine.place_order("SELL", 64200.0, 0.8)
        depth = self.engine.get_order_book_depth()
        self.assertEqual(depth["best_bid"], 64000.0)
        self.assertEqual(depth["best_ask"], 64200.0)
        self.assertEqual(depth["spread"], 200.0)


if __name__ == "__main__":
    unittest.main()
