# Python Crypto Order Book Matching Engine ⚡📈

![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Build](https://img.shields.io/badge/Build-Passing-brightgreen.svg)

A high-performance in-memory Limit Order Book (LOB) matching engine built in Python. Implements strict Price-Time priority FIFO matching for cryptocurrency spot pairs (BTC/USDT, ETH/INR) and FinTech trading venues.

---

## 🚀 Key Features

- **Price-Time Priority (FIFO)**: High-speed order queue sorting highest bids and lowest asks with deterministic microsecond tie-breaking.
- **Partial Fills & Resting Orders**: Handles partial matches, multi-order execution fills, and resting liquidity updates.
- **Level 2 Market Depth**: Instant best bid, best ask, and bid-ask spread inspection.
- **Audit-Ready Trade Executions**: Generates immutable trade execution reports with maker and taker order IDs.

---

## 📦 Installation & Setup

```bash
git clone https://github.com/shyampandey1104/python-crypto-orderbook-matching-engine.git
cd python-crypto-orderbook-matching-engine
pip install -r requirements.txt
```

---

## 🛠️ Usage Example

```python
from orderbook.engine import MatchingEngine

engine = MatchingEngine(symbol="BTC-USDT")

# Maker Sell Order
engine.place_order("SELL", price=65000.0, quantity=2.0)

# Aggressive Taker Buy Order
fill = engine.place_order("BUY", price=65200.0, quantity=1.5)
print(f"Status: {fill['status']} | Executed at: {fill['trades'][0]['executed_price']}")
```

---

## 🧪 Testing

```bash
pytest tests/
```

---

## 📄 License
MIT License. Created with ❤️ by [Shyam Pandey](https://github.com/shyampandey1104).
