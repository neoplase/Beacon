from bittrex.bittrex import Bittrex
from peer import peer

class market:
    def __init__(self):
        self.Peers = []

    def GetActiveMarkets(self, filterBaseCcy = None, filterVolume = None):
        BittRexCo = Bittrex(None, None)
        Data = BittRexCo.get_markets()

        if Data['success'] :
            for item in Data['result']:
                if filterBaseCcy == None :
                    
                    p = peer()
                    p.GetInformations(item['MarketName'])

                    if filterVolume == None :
                        self.Peers.append(p)    
                    else:
                        if p.Last*p.Volume >= filterVolume :
                            self.Peers.append(p)

                elif item['BaseCurrency'] == filterBaseCcy:
                    
                    p = peer()
                    p.GetInformations(item['MarketName'])

                    if filterVolume == None :
                        self.Peers.append(p)
                    else:
                        if p.Last*p.Volume >= filterVolume:
                            self.Peers.append(p)

