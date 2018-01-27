
from bittrex.bittrex import Bittrex
from peer import peer
import dateutil.parser
import time

class portfolio:
    def __init__(self,apikey,apisecret):
        self.apikey = apikey
        self.apisecret = apisecret
        self.Account = []

        self.ValueInUSD = 0.0

        self.Cash = 0.0

        self.safeheavencurrency = "USDT"
        self.cashUpperBound = 0.98

    def Refresh(self):

        BittRexCo = Bittrex(self.apikey,self.apisecret)
        Data = BittRexCo.get_balances()

        if Data['success']:

            self.Account=[]

            for item in Data['result']:

                if item['Currency'] == self.safeheavencurrency:
                    self.Cash = item['Available']

                self.Account.append(item)
            return True
        return False

    def ComputeValue(self, ToRefresh=False):

        self.ValueInUSD = 0.0

        for item in self.Account:
            if item['Currency'] == "USDT":
                self.ValueInUSD += item['Balance']
            else :
                p = peer()
                p.RefreshRealTime("USDT" + "-" + item['Currency'])

                self.ValueInUSD += item['Balance']*p.Last

        return self.ValueInUSD

    def PlaceBuyOrder(self, market, quantity, rate):
        BittRexCo = Bittrex(self.apikey,self.apisecret)
        Data = BittRexCo.buy_limit(market, quantity,rate)

        if not Data['success']:
            print(Data['message'])

        return Data['success']

    def PlaceSellOrder(self,market, quantity, rate):
        BittRexCo = Bittrex(self.apikey,self.apisecret)
        Data = BittRexCo.sell_limit(market, quantity,rate)

        if not Data['success']:
            print(Data['message'])

        return Data['success']

    def CancelOutDatedOrder(self, seconds):
        BittRexCo = Bittrex(self.apikey,self.apisecret)
        Data = BittRexCo.get_open_orders()
        
        if Data['success']:
            for item in Data['result']:
                dt = dateutil.parser.parse(item['Opened'])
                timestamp = int(time.mktime(dt.timetuple()))
                if time.time() - timestamp > seconds:
                    print("Cancelling Order : " + item['OrderUuid'])
                    BittRexCo.cancel(item['OrderUuid'])
        else:
            print(Data['message'])
                

