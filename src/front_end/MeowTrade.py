import logging

import pandas as pd
from ibapi.client import EClient
from ibapi.contract import Contract
from ibapi.wrapper import EWrapper
from ibapi.common import TickerId

class MeowTrade(EWrapper, EClient):
    def __init__(self, data_list=None):
        EClient.__init__(self, self)
        self.data_list = data_list

        self.bulletins = []  # List to store bulletins

    def setup_connection(self):
        self.connect("127.0.0.1", 7496, clientId=1)
        self.run()

    def error(self, reqId:TickerId, errorCode:int, errorString:str, advancedOrderRejectJson = ""):
        if errorCode in [2104, 2106, 2158]:  # these are actually not errors, they are just notifications
            logging.info(f"System Notification - ReqId: {reqId}, ErrorCode: {errorCode}, Message: {errorString}")
        else:
            logging.error(f"Error - ReqId: {reqId}, ErrorCode: {errorCode}, ErrorString: {errorString}")

    def accountSummary(self, reqId:int, account:str, tag:str, value:str, currency:str):
        logging.info(f"ReqId: {reqId}, Account: {account}, Tag: {tag}, Value: {value}, Currency: {currency}")

    def accountSummaryEnd(self, reqId:int):
        logging.info(f"AccountSummaryEnd. ReqId: {reqId}")
        self.disconnect()

    def nextValidId(self, orderId: int):
        logging.info("Tradetron: nextValidId: Now connected")

        # self.reqMarketDataType(1)  # Live data
        self.reqMarketDataType(3)  # Delayed data
        contract = Contract()
        contract.symbol = "SPY"
        contract.secType = "STK"
        contract.currency = "USD"
        contract.exchange = "SMART"
        self.reqMktData(1, contract, "", False, False, [])  # Requesting market data for SPY



    def updateNewsBulletin(self, msgId:int, msgType:int, newsMessage:str, originExch:str):
        """
        Update the news bulletin
        :param msgId:
        :param msgType:
        :param newsMessage:
        :param originExch:
        :return:
        """
        logging.info(f"MeowTrade: News Bulletin: ID={msgId}, Type={msgType}, Message={newsMessage}, Exchange={originExch}")
        # Store the bulletin in the list
        self.bulletins.append((msgId, msgType, newsMessage, originExch))

    def tickPrice(self, reqId:TickerId, tickType:int, price:float, attrib):
        # if tickType == 4:  # last price
        logging.info(f"MeowTrade: Tick Price - ReqId: {reqId}, TickType: {tickType}, Price: {price}")

        new_row = {'Time': pd.Timestamp.now(), 'Value': price}
        self.data_list.append(new_row)




