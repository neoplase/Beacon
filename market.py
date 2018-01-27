from bittrex.bittrex import Bittrex
from peer import peer

class market:
    def __init__(self):
        self.Peers = []

    def GetActiveMarkets(self, filterBaseCcy = None, Top = 0):
        BittRexCo = Bittrex(None, None)
        Data = BittRexCo.get_markets()

        if Data['success'] :
            for item in Data['result']:
                if filterBaseCcy == None :
                    
                    p = peer()
                    p.GetInformations(item['MarketName'])

                    self.Peers.append(p)


                elif item['BaseCurrency'] == filterBaseCcy:
                    
                    p = peer()
                    p.GetInformations(item['MarketName'])

                    self.Peers.append(p)

            if Top > 0 :
                self.Peers = self.Peers[:Top]

