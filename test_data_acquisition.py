from ibapi.client import EClient, MarketDataTypeEnum
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.ticktype import TickTypeEnum
import ibapi
import threading
import time


class IBapi(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)

    def tickPrice(self, reqId, tickType, price, attrib):
        print('The ' +
              str(next(name for name, value in vars(TickTypeEnum).items() if value == tickType)) + ' price is: ', price)


def run_loop():
    app.run()


def create_contract(symbol, secType, exchange, currency='USD'):
    contract = Contract()
    contract.symbol = symbol
    contract.secType = secType
    contract.exchange = exchange
    if currency:
        contract.currency = currency
    return contract

app = IBapi()
app.connect('127.0.0.1', 7496, 123)

# Start the socket in a thread
api_thread = threading.Thread(target=run_loop, daemon=True)
api_thread.start()

time.sleep(1)  # Sleep interval to allow time for connection to server

# Create contract objects
apple_contract = create_contract('AAPL', 'STK', 'SMART')  # Apple stock price
eurusd_contract = create_contract('EUR', 'CASH', 'IDEALPRO')  # EU-USA price
# BTC_futures_contract = create_contract('BRR', 'FUT', 'CMECRYPTO', currency=None)  # bitcoin price, NOT CORRECTED
# BTC_futures_contract.lastTradeDateOrContractMonth = '202003'
# using delayed market data
app.reqMarketDataType(MarketDataTypeEnum.DELAYED)

# Request Market Data
app.reqMktData(1, apple_contract, '', False, False, [])

time.sleep(5)  # Sleep interval to allow time for incoming price data
app.disconnect()
