from strategyInterface import Strategy

class MeanReversionStrategy(Strategy):
    def __init__(self, symbol="SPY", cash_at_risk=0.5):
        self.symbol = symbol
        self.cash_at_risk = cash_at_risk
        self.last_trade = None
        self.performance_log = []
    
    def initialize(self, symbol="SPY", cash_at_risk=0.5):
        self.symbol = symbol
        self.cash_at_risk = cash_at_risk

    def position_sizing(self):
        cash = self.get_cash()
        last_price = self.get_last_price(self.symbol)
        quantity = round(cash * self.cash_at_risk / last_price, 0)
        return cash, last_price, quantity

    def get_sentiment(self):
        return 0, "neutral"  # No sentiment in this strategy

    def on_trading_iteration(self):
        cash, last_price, quantity = self.position_sizing()
        # Example of mean reversion logic: buy when price is 1% below moving average, sell when 1% above
        moving_avg = self.get_moving_average(self.symbol, 20)  # 20-period moving average
        if last_price < moving_avg * 0.99:  # Buy signal
            if self.last_trade != "buy":
                self.create_order(self.symbol, quantity, "buy")
                self.last_trade = "buy"
                
        elif last_price > moving_avg * 1.01:  # Sell signal
            if self.last_trade != "sell":
                self.create_order(self.symbol, quantity, "sell")
                self.last_trade = "sell"

    def get_volatility(self, symbol, lookback=30):
        return 0  # No volatility consideration in this simple strategy
