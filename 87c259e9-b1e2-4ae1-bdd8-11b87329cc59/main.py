from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI, EMA
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        self.ticker = "AAPL"

    @property
    def assets(self):
        return [self.ticker]

    @property
    def interval(self):
        return "1day"

    def run(self, data):
        # Initialize allocation with no holdings
        allocation_dict = {self.ticker: 0}
        
        # Calculate RSI and EMA values
        rsi_values = RSI(self.ticker, data["ohlcv"], 14)  # Using 14-days for RSI calculation
        ema_values = EMA(self.ticker, data["ohlcv"], 50)  # Using 50-days for EMA calculation
        
        if rsi_values and ema_values:
            # Get the latest values of RSI and EMA
            current_rsi = rsi_values[-1]
            current_ema = ema_values[-1]
            current_price = data["ohlcv"][-1][self.ticker]["close"]
            
            # Check for buying signal
            if current_rsi < 30 and current_price > current_ema:
                allocation_dict[self.ticker] = 1  # Allocate 100% to AAPL
                log(f"Buying signal: RSI={current_rsi}, Price={current_price}, EMA={current_ema}")
            else:
                log(f"No buying signal: RSI={current_rsi}, Price={current_price}, EMA={current_ema}")

        return TargetAllocation(allocation_dict)