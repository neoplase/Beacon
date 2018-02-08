import statsmodels.formula.api as smf

from orderbook import OrderBook
from pandas import DataFrame

from portfolio import portfolio
from peer import peer

import time

class Model:

    def __init__(self):
        # type: () -> Model
        self.Model = None

        self.TimeWindow = 0
        self.jLag = 0


    def Calibrate(self,Orderbooks, timeWindow, jLag):
        if len(Orderbooks) >     timeWindow + jLag + 1 :
            self.TimeWindow = timeWindow
            self.jLag = jLag

            PriceChanges = []
            OI = []

            Data = {}
            for i in range(0, len(Orderbooks)-2):
                OI.append(self.OI(Orderbooks[i+1], Orderbooks[i]))

            for i in range(0 ,len(Orderbooks) - self.TimeWindow):
                tmp = 0

                for j in range(0, self.TimeWindow):
                    tmp = tmp + (Orderbooks[i+j].MidPrice - Orderbooks[i].MidPrice)/Orderbooks[i].MidPrice

                tmp = tmp / self.TimeWindow

                PriceChanges.append(tmp)


            for i in range(self.TimeWindow-1, len(Orderbooks) - self.TimeWindow):
                tmp = [PriceChanges[i]]
                for j in range(1,self.jLag+1):
                    tmp.append(OI[i -j])
                Data[i] = tmp

            pd = DataFrame.from_dict(Data).transpose()
            print(pd)
            keys = []

            keys.append('PriceChange')

            for i in range(0,self.jLag):
                keys.append('OI' + str(jLag-i))

            pd.columns = keys

            formula = ''

            for item in keys :

                if item == 'PriceChange':
                    formula = formula + item
                    formula = formula + ' ~ '
                    first = True
                else :
                    if first :
                        formula = formula  + item
                        first = False
                    else:
                        formula = formula + ' + ' + item

            lm = smf.ols(formula=formula, data=pd).fit()

            print(lm.params)
            print(lm.summary())

            self.Model = lm

            return True
        else :
            print("Not Enough Data to calibrate")
            return False

    def PriceChangePrediction(self, Orderbooks):

        OI = []

        if len(OrderBook) == self.jLag:
            for i in range(0, len(Orderbooks)-2):
                OI.append(self.OI(Orderbooks[i+1], Orderbooks[i]))

            return self.Model.predict(OI)
        else:
            return False

    def OI(self, Orderbookt, Orderbooktminusone):

        if Orderbookt.BidPrice < Orderbooktminusone.BidPrice :
            dVtB = 0
        elif Orderbookt.BidPrice == Orderbooktminusone.BidPrice :
            dVtB = Orderbookt.BidVolume - Orderbooktminusone.BidVolume
        else :
            dVtB = Orderbookt.BidVolume

        if Orderbookt.AskPrice < Orderbooktminusone.AskPrice :
            dVtA = Orderbookt.AskVolume
        elif Orderbookt.AskPrice == Orderbooktminusone.AskPrice :
            dVtA = Orderbookt.AskVolume - Orderbooktminusone.AskVolume
        else :
            dVtA = 0

        return dVtB - dVtA

def LaunchStrategy():

    print("Launching algorithm ...")

    port = portfolio("a19827699f5e4d8a8e7b32729df8c690", "62bda7d2f09f461ba5e45b6644bb35f5")
    print("Computing Portfolio ...")

    port.Refresh()
    port.ComputeValue()

    Peer = peer()

    while not Peer.GetInformations("USDT-BTC"):
        print('Retrying ...')

    _Orderbooks = []


    for i in range(0,300):
        time.sleep(1)
        print("Retrieving Orderbook : " + str(i))

        tmp = OrderBook(Peer.MarketName)

        if tmp.Refresh():
            _Orderbooks.append(tmp)

    Mod = Model()

    Mod.Calibrate(_Orderbooks, 12,6)

    _Orderbooks = []

    InitialValue = port.ValueInUSD

    for i in range(0,120):

        print("Value of Portfolio: ", round(port.ValueInUSD, 2), " $ ")
        print("Available Cash : ", round(port.Cash, 2), " $")
        print("PNL : ", round(port.ValueInUSD - InitialValue, 2), " $ ")

        time.sleep(1)

        print("Retrieving Orderbook : " + str(i))
        
        tmp = OrderBook("USDT-BTC")

        if tmp.Refresh():

            if len(_Orderbooks) >= 6:

                _Orderbooks.pop()

            _Orderbooks.append(tmp)

            if len(_Orderbooks) >= 6:

                Value = Mod.PriceChangePrediction(_Orderbooks[::-1])

                if type(Value) == bool:
                    print("ERROR: No refreshed data")

                elif Value > 0 :
                    port.Refresh()

                    #Pas de transaction en dessous de 1 $ ...
                    if port.Cash > 1.00 :
                        Peer.RefreshRealTime()

                        buyingPrice = Peer.Mid()
                        buyingNumber = (99.0/100.0) * port.Cash / buyingPrice

                        print("Buying ", Peer.MarketCurrency.Ccy, " -> ", round(buyingNumber, 2), " at ", round(buyingPrice,
                                                                                                                4)," Last = ", round(Peer.Last, 4), " ) ")
                        if not port.PlaceBuyOrder(Peer.MarketName, buyingNumber, buyingPrice):
                            print("Error on placing buy order ... Time : ", time.time())
                elif Value < 0 :
                    port.Refresh()

                    for item in port.Account:

                        if item['Currency'] == Peer.MarketCurrency.Ccy:
                            shares = item['Available']

                            if shares != 0:
                                print(Peer.MarketCurrency.Ccy, "shares in portfolio to sell", shares)

                            if shares > 0:
                                Peer.RefreshRealTime()
                                sellingPrice = Peer.Mid()

                                print("Selling ", Peer.MarketCurrency.Ccy, " -> ", round(shares, 2), " at ",
                                      round(sellingPrice, 4), " ( Last = ", round(Peer.Last, 4), " )")

                                if not port.PlaceSellOrder(Peer.MarketName, shares, sellingPrice):
                                   print("Error on placing sell order ... Time : ", time.time())

                            elif shares != 0:
                                print("Selling not done : ", Peer.MarketCurrency.Ccy, " Min Trade size not met -> ",
                                      round(Peer.MinTradeSize, 4))


LaunchStrategy()