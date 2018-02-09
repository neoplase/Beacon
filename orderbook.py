from bittrex.bittrex import *

BUY ='buy'
SELL ='sell'

class Order:
    def __init__(self):
        self.Side = ''
        self.Quantity = ''
        self.Rate = 0.0



class OrderBook:

    def __init__(self, market):
        self.Orders = []
        self.Market = market
        self.Date = time.time()

    def Refresh(self):
        BittRexCo = Bittrex(None, None)

        if self.Market != "" :

            try:
                Data = BittRexCo.get_orderbook(self.Market,BOTH_ORDERBOOK,10)
                self.Date = time.time()

                if Data['success']:

                    for item in Data['result']['buy'] :
                        tmp = Order()
                        tmp.Quantity = item['Quantity']
                        tmp.Rate = item['Rate']
                        tmp.Side = BUY

                        self.Orders.append(tmp)

                    for item in Data['result']['sell']:
                        tmp = Order()
                        tmp.Quantity = item['Quantity']
                        tmp.Rate = item['Rate']
                        tmp.Side = SELL

                        self.Orders.append(tmp)

                    self.Refresh_Values()

                    return True
                else:
                    return False
            except:
                return False

    def Refresh_Values(self):

        self.MidPrice = -1
        self.AskPrice = 1000000
        self.BidPrice = -1
        self.AskVolume = -1
        self.BidVolume = -1

        for item in self.Orders:
            if item.Side == BUY :
                if item.Rate >= self.BidPrice :
                    self.BidPrice = item.Rate
                    self.BidVolume = self.BidVolume + item.Quantity

            elif item.Side == SELL:
                if item.Rate <= self.AskPrice :
                    self.AskPrice = item.Rate
                    self.AskVolume = self.AskVolume + item.Quantity

        self.MidPrice = (self.AskPrice + self.BidPrice)/2

#OB = OrderBook("BTC-LTC")

#OB.Refresh()
