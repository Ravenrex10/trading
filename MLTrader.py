from strategyInterface import Strategy, config
from timedelta import Timedelta
from alpaca_trade_api import REST
from math import floor
from lumibot.strategies.strategy import Strategy
from finbert_utils import estimate_sentiment

class MLTrader(Strategy):
    def initialize(self, symbol="SPY", cash_at_risk=0.5, sentiment_threshold=0.9):
        self.symbol = symbol
        self.sleeptime = "24H"  # Can adjust dynamically
        self.last_trade = None
        self.cash_at_risk = cash_at_risk
        self.sentiment_threshold = sentiment_threshold
        self.api = REST(base_url=config["base_url"], key_id=config["api_key"], secret_key=config["api_secret"])
        self.performance_log = []

    def position_sizing(self):
        cash = self.get_cash()
        last_price = self.get_last_price(self.symbol)
        volatility = self.get_volatility(self.symbol)
        adjusted_cash_at_risk = self.cash_at_risk / (1 + volatility)
        quantity = round(cash * adjusted_cash_at_risk / last_price, 0)
        return cash, last_price, quantity

    def get_volatility(self, symbol, lookback=30):
        # Assume get_historical_prices() returns a Bars object
        bars = self.get_historical_prices(symbol, lookback)
        
        # Convert to DataFrame if needed, or access close prices directly
        if hasattr(bars, 'df'):
            prices = bars.df['close']  # If the Bars object has a DataFrame-like attribute
        else:
            prices = pd.DataFrame(bars)['close']  # Convert to DataFrame if necessary
        
        # Calculate returns and then volatility
        returns = prices.pct_change().dropna()
        return returns.std()
    
    def get_dates(self): 
        today = self.get_datetime()
        three_days_prior = today - Timedelta(days=3)
        return today.strftime('%Y-%m-%d'), three_days_prior.strftime('%Y-%m-%d')


    def get_sentiment(self):
        try:
            today, three_days_prior = self.get_dates()
            news = self.api.get_news(symbol=self.symbol, start=three_days_prior, end=today)
            news = [ev.__dict__["_raw"]["headline"] for ev in news]
            probability, sentiment = estimate_sentiment(news)
            return probability, sentiment
        except Exception as e:
            print(f"Error fetching sentiment: {e}")
            return 0, "neutral"
    

    def on_trading_iteration(self):
        cash, last_price, quantity = self.position_sizing()
        probability, sentiment = self.get_sentiment()

        if cash > last_price:
            if sentiment == "positive" and probability > self.sentiment_threshold:
                if self.last_trade == "sell":
                    self.sell_all()
                order = self.create_order(
                    self.symbol,
                    quantity,
                    "buy",
                    type="bracket",
                    take_profit_price=last_price * 1.20,
                    stop_loss_price=last_price * 0.95
                )
                self.submit_order(order)
                self.last_trade = "buy"

            elif sentiment == "negative" and probability > self.sentiment_threshold:
                if self.last_trade == "buy":
                    self.sell_all()
                order = self.create_order(
                    self.symbol,
                    quantity,
                    "sell",
                    type="bracket",
                    take_profit_price=last_price * 0.8,
                    stop_loss_price=last_price * 1.05
                )
                self.submit_order(order)
                self.last_trade = "sell"
