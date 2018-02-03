from currency import currency
from bittrex.bittrex import Bittrex


class peer:

    def __init__(self):
        self.MarketCurrency = currency()
        self.BaseCurrency = currency()
        self.MinTradeSize = 0
        self.MarketName = ""
        self.IsActive = False
        self.Created = ""

        self.High = 0.0
        self.Low = 0.0
        self.Volume = 0.0
        self.Last = 0.0
        self.BaseVolume = 0.0
        self.TimeStamp = ""
        self.Bid = 0.0
        self.Ask = 0.0
        self.OpenBuyOrders = 0
        self.OpenSellOrders = 0
        self.PrevDay = 0
        self.HistoricalData = dict()

        self.OrderBook = []

    def Print(self):
        print("MarketCurrency : ")
        self.MarketCurrency.Print()
        print("BaseCurrency : ")
        self.BaseCurrency.Print()
        print("MinTradeSize : ", self.MinTradeSize)
        print("MarketName : ", self.MarketName)
        print("IsActive : ", self.IsActive)
        print("Created : ", self.Created)

    def PrintValues(self):
        print("Bid : ", self.Bid, " Last : ", self.Last, " Ask : ", self.Ask)
        print("High : ", self.High)
        print("Low : ", self.Low)
        print("Volume : ", self.Volume)
        print("Return : ", round(self.DailyReturn() * 100, 2), " %")

        return False

    def Mid(self):
        return (self.Bid + self.Ask) / 2.0

    def RefreshRealTime(self, MarketName=None):
        BittRexCo = Bittrex(None, None)

        if MarketName == None:
            Data = BittRexCo.get_ticker(self.MarketName)
        else:
            Data = BittRexCo.get_ticker(MarketName)

        if Data['success']:
            self.Bid = Data['result']['Bid']
            self.Ask = Data['result']['Ask']
            self.Last = Data['result']['Last']

            return True

    def DailyReturn(self):
        return (self.Last / self.PrevDay) - 1

    def GetHistoricalPrices(self):
        # BV - ???
        # C - CloseAsk
        # H - HighAsk
        # L - LowAsk
        # O - OpenAsk
        # V - Volume

        BittRexCo = Bittrex(None, None)
        Data = BittRexCo.get_historical_data(self.MarketName, "fiveMin")

        if Data['success']:
            self.HistoricalData = Data['result']
            return True
        return False

    def GetInformations(self, MarketName):
        BittRexCo = Bittrex(None, None)
        Data = BittRexCo.get_markets()

        if Data['success']:
            Res = Data['result']
            for item in Res:
                if item['MarketName'] == MarketName:
                    self.MarketName = item['MarketName']
                    self.MarketCurrency.GetInformation(item['MarketCurrency'])
                    self.BaseCurrency.GetInformation(item['BaseCurrency'])
                    self.MinTradeSize = item['MinTradeSize']
                    self.IsActive = item['IsActive']
                    self.Created = item['Created']

                    Data2 = BittRexCo.get_marketsummary(item['MarketName'])

                    if Data2['success']:
                        for item2 in Data2['result']:
                            self.High = item2['High']
                            self.Low = item2['Low']
                            self.Last = item2['Last']
                            self.Volume = item2['Volume']
                            self.BaseVolume = item2['BaseVolume']
                            self.TimeStamp = item2['TimeStamp']
                            self.Bid = item2['Bid']
                            self.Ask = item2['Ask']
                            self.OpenSellOrders = item2['OpenSellOrders']
                            self.OpenBuyOrders = item2['OpenBuyOrders']
                            self.PrevDay = item2['PrevDay']
                        return True
            return False
