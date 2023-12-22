import os
import hmac
import hashlib
import requests
import time
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access environment variables
api_key = os.getenv("API_KEY")
database_url = os.getenv("DATABASE_URL")
api_key = 'your_api_key'
api_secret = 'your_api_secret'


class BinanceTradingBot:
    def __init__(self, api_key, api_secret, symbol, interval='1h'):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = 'https://api.binance.com/api/v3'
        self.symbol = symbol
        self.interval = interval

    def _generate_signature(self, data):
        return hmac.new(self.api_secret.encode('utf-8'), data.encode('utf-8'), hashlib.sha256).hexdigest()

    def _request(self, method, endpoint, params=None, data=None):
        url = f"{self.base_url}/{endpoint}"
        headers = {'X-MBX-APIKEY': self.api_key}

        if method == 'GET':
            response = requests.get(url, headers=headers, params=params)
        elif method == 'POST':
            headers['Content-Type'] = 'application/x-www-form-urlencoded'
            headers['signature'] = self._generate_signature(params)
            response = requests.post(url, headers=headers, params=params, data=data)

        return response.json()

    def get_candlestick_data(self):
        endpoint = 'klines'
        params = {'symbol': self.symbol, 'interval': self.interval, 'limit': 5}
        return self._request('GET', endpoint, params=params)

    def place_market_order(self, side, quantity):
        endpoint = 'order'
        params = {
            'symbol': self.symbol,
            'side': side,
            'type': 'MARKET',
            'quantity': quantity,
            'timestamp': int(time.time() * 1000),
        }
        return self._request('POST', endpoint, params=params)

# Replace with your Binance API key and secret
symbol_to_trade = 'BTCUSDT'

# Initialize the trading bot
trading_bot = BinanceTradingBot(api_key, api_secret, symbol_to_trade)

# Get recent candlestick data
candlestick_data = trading_bot.get_candlestick_data()
print(candlestick_data)

# Example: Place a market order (BUY) for 0.001 BTC
order_result = trading_bot.place_market_order('BUY', quantity=0.001)
print(order_result)