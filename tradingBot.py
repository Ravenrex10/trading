from lumibot.brokers import Alpaca
from lumibot.backtesting import YahooDataBacktesting
from datetime import datetime
from MLTrader import MLTrader
from MeanReversionStrategy import MeanReversionStrategy
from strategyInterface import config

ALPACA_CREDS = {
    "API_KEY": config["api_key"], 
    "API_SECRET": config["api_secret"], 
    "PAPER": True
}


start_date = datetime(2020, 1, 1)
end_date = datetime(2024, 11, 1)

broker = Alpaca(ALPACA_CREDS)

strategy = MLTrader(name='mlstrat', broker=broker, parameters={"symbol": "SPY", "cash_at_risk": 0.5, "sentiment_threshold": 0.9})
strategy.backtest(YahooDataBacktesting, start_date, end_date, parameters={"symbol": "SPY", "cash_at_risk": 0.5, "sentiment_threshold": 0.9})
