from lumibot.brokers import Alpaca
from lumibot.backtesting import YahooDataBacktesting
from lumibot.strategies.strategy import Strategy
from lumibot.traders import Trader
from datetime import datetime
from alpaca_trade_api import REST
from timedelta import Timedelta

API_KEY = ''
API_SECRET = ''
BASE_URL = 'https://paper-api.alpaca.markets'

ALPACA_CREDS = {"API_KEY": API_KEY,
                "API_SECRET": API_SECRET,
                "PAPER": True}
start_date = datetime(2024, 1, 1)
end_date = datetime(2024, 2, 1)

class MLTrader(Strategy):
    def initialize(self, symbol: str = "SPY", cash_at_risk:float = 0.5):
        self.symbol = symbol
        self.sleeptime = "24H"
        self.last_trade = None
        self.cash_at_risk = cash_at_risk
        pass

    def position_sizing(self):
        cash = self.get_cash()
        last_price = self.get_last_price(self.symbol)
        quantity = round(cash * self.cash_at_risk /last_price)
        return cash, last_price, quantity

    def on_trading_iteration(self):
        cash, last_price, quantity = self.position_sizing()
        if cash > last_price:
            if self.last_trade == None:
                order = self.create_order(self.symbol,
                                          quantity,
                                          "buy",
                                          type="bracket",
                                          take_profit_price=last_price*1.20,
                                          stop_loss_price=last_price*0.95)
                self.submit_order(order)
                self.last_trade = "buy"


broker = Alpaca(ALPACA_CREDS)
strategy = MLTrader(name='mlstrat',
                    broker=broker,
                    parameters={"symbol": "SPY",
                                'cash_at_risk' : 0.5})

strategy.backtest(YahooDataBacktesting,
                  start_date,
                  end_date,
                  parameters={"symbol": "SPY",
                              'cash_at_risk' : 0.5})


