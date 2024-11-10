from abc import ABC, abstractmethod
import json

with open("config.json") as json_data_file:
    config = json.load(json_data_file)

# Define the Strategy Interface (Java-like interface)
class Strategy(ABC):
    
    @abstractmethod
    def initialize(self, symbol="SPY", cash_at_risk=0.5, sentiment_threshold=0.9):
        """Initialize strategy parameters."""
        pass
    
    @abstractmethod
    def position_sizing(self):
        """Calculate position sizing based on available cash."""
        pass
    
    @abstractmethod
    def get_sentiment(self):
        """Get sentiment data to drive decisions."""
        pass
    
    @abstractmethod
    def on_trading_iteration(self):
        """Define behavior during each trading iteration."""
        pass

    @abstractmethod
    def get_volatility(self, symbol, lookback=30):
        """Calculate volatility for risk management."""
        pass

    def log_trade(self, trade_type, price, quantity):
        """Log trade details."""
        trade_info = {
            "type": trade_type,
            "price": price,
            "quantity": quantity,
            "timestamp": self.get_datetime()
        }
        self.performance_log.append(trade_info)
        print(f"Logged trade: {trade_info}")
