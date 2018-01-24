from portfolio import portfolio
from market import market
from peer import peer

from time import time
import math

def main():
    
    
    print("Launching algorithm ...")

    port = portfolio("a19827699f5e4d8a8e7b32729df8c690", "62bda7d2f09f461ba5e45b6644bb35f5")
    print("Computing Portfolio ...")

    port.Refresh()
    port.ComputeValue()
    print("Retrieving Active Markets on ", port.safeheavencurrency)

    mkt = market()
    mkt.GetActiveMarkets(port.safeheavencurrency, 1000000)

    print("Initial Value of Portfolio: ", round(port.ValueInUSD, 2), " $ ")
    print("Available Cash : ", round(port.Cash, 2), " $")
    print("Cash Ratio Limit : ", round(port.cashUpperBound, 2))

    InitialCash = port.Cash
    InitialValue = port.ValueInUSD

    i = 0
    
    
    while True:
        
        try:
            port.Refresh()
            port.ComputeValue()

        except:
            print("Error on refresh")

        print("------------------------------------------------------------------------------------")

        AvailableCash = port.Cash - (InitialCash * (1 - port.cashUpperBound))

        print("Value of Portfolio: ", round(port.ValueInUSD, 2), " $ ")
        print("Available Cash : ", round(AvailableCash, 2), " $")
        print("PNL : ", round(port.ValueInUSD - InitialValue, 2), " $ ")

        # Checking Buy and Sell Orders

        ToBuy = []
        ToSell = []

        for TargetPeer in mkt.Peers:

            try:
                TargetPeer.GetHistoricalPrices()
                
            except:
                print("Error on Histo")

            last20 = TargetPeer.HistoricalData[-20*30:]
            last5 = TargetPeer.HistoricalData[-5*30:]
            last60 = TargetPeer.HistoricalData[-60:]
            TargetPeer.RefreshRealTime()

            #for item in last5:
            #    print(item)

            ma_5 = 0
            ma_20 = 0
            mean_60 = 0
            std = 0
    
            n = float(len(last60))
    
            for item in last60:
                mean_60 += item['C']
    
            mean_60 = mean_60 / n
    
            for item in last60:
                std += (item['C'] - mean_60) * (item['C'] - mean_60)
    
            std = std / n
            std = math.sqrt(std)
    
            n = 0
    
            for item in last5:
                ma_5 += n * item['C']
                n = n +1

            ma_5 += n*TargetPeer.Mid()

            n = 0
    
            for item in last20:
                ma_20 += n * item['C']
                n = n + 1

            ma_20 += n * TargetPeer.Mid()

            ma_5 = 2 * ma_5 / (float(len(last5)) * (float(len(last5)) + 1))
            
            ma_20 = 2 * ma_20 / (float(len(last20)) * (float(len(last20)) + 1))

            
            print("Ratio for : ", TargetPeer.MarketName, " = ", round(ma_5 / ma_20 * 100 - 100, 2), " % ")
            if ma_5 > 1.000 * ma_20:
                ToBuy.append(TargetPeer)
            elif ma_5 < 1.000 * ma_20:
                ToSell.append(TargetPeer)
        
        
        try:
            for PeerToB in ToBuy:

                PeerToB.RefreshRealTime()

                buynumber = ((port.Cash - (InitialCash * (1 - port.cashUpperBound))) / PeerToB.Mid()) / len(ToBuy)

                buyingPrice = float(PeerToB.Mid())

                if buynumber > PeerToB.MinTradeSize :

                    if buynumber * buyingPrice > 0.01:

                        print("Buying ", PeerToB.MarketCurrency.Ccy, " -> ", round(buynumber, 2), " at ", round(buyingPrice,
                                                                                                                4), " Last = ", round(PeerToB.Last,4), " ) ")

                        if not port.PlaceBuyOrder(PeerToB.MarketName, buynumber, buyingPrice):
                            print("Error on placing buy order ... Time : ", time())

                else:
                    print("Buying not done : ", PeerToB.MarketCurrency.Ccy , " Min Trade size not met -> " , round(PeerToB.MinTradeSize,4))

        except :
            print("Error on buying part")

        try:
            for PeerToS in ToSell:
                PeerToS.RefreshRealTime()

                sellingPrice = float(PeerToS.Mid())

                for item in port.Account:
                    if item['Currency'] == PeerToS.MarketCurrency.Ccy:
                        shares = item['Available']
    
                        if shares != 0:
                            print(PeerToS.MarketCurrency.Ccy, "shares ", shares)
    
                        if shares > PeerToS.MinTradeSize :
                            print("Selling ", PeerToS.MarketCurrency.Ccy, " -> ", round(shares, 2), " at ", round(sellingPrice,4), " ( Last = ", round(PeerToS.Last,4), " )" )
                            if not port.PlaceSellOrder(PeerToS.MarketName, shares, sellingPrice):
                                print("Error on placing sell order ... Time : ", time())
                        else:
                            print("Selling not done : ", PeerToS.MarketCurrency.Ccy , " Min Trade size not met -> " , round(PeerToS.MinTradeSize,4))
        except:
            print("Error on selling part")

        try:
            port.CancelOutDatedOrder(30)
        except:
            print("Error on cancelling orders")


main()
