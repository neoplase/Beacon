import orderbook
import portfolio
from peer import peer
import time

def Strategy():

    try :
        file = open('pnl.log', 'w',0)
    except:
        print("ERROR PNL Output")

    print("Launching algorithm ...")

    port = portfolio.portfolio("a19827699f5e4d8a8e7b32729df8c690", "62bda7d2f09f461ba5e45b6644bb35f5")
    print("Computing Portfolio ...")

    port.Refresh()
    port.ComputeValue()

    Peer = peer()

    while not Peer.GetInformations("USDT-XMR"):
        print('Retrying ...')

    i = 0

    timetosleep = 5
    myBidPrice = 0.0
    myAskPrice = 0.0

    while True:

        i = i +1

        if i % 10 == 0 :

            try :
                port.ComputeValue()
                file.write('PNL : ' + str(port.ValueInUSD) + '\n')

            except:
                print('Unable to compute Value')


        Orderbook = orderbook.OrderBook(Peer.MarketName)
        Refreshed = False



        while not Refreshed:

            try:
                Orderbook.Refresh()
                port.Refresh()
                Refreshed = True
            except:
                print('Retry to refresh orderbook and portfolio')

        shares = 0
        Balance = 0

        for item in port.Account:
            if item['Currency'] == Peer.MarketCurrency.Ccy:
                shares = item['Available']
                Balance = item['Balance']


        if shares > 0 :

            print('Already have position, waiting for lock')

            sellingPrice = Orderbook.AskPrice - Orderbook.AskPrice * 0.0001

            myAskPrice = Orderbook.AskPrice - Orderbook.AskPrice * 0.0001

            print("Selling ", Peer.MarketCurrency.Ccy, " -> ", round(shares, 2), " at ",
                  round(sellingPrice, 4), " ( Last = ", round(Peer.Last, 4), " )")

            try:
                if not port.PlaceSellOrder(Peer.MarketName, shares, sellingPrice):
                    print("Error on placing sell order ... Time : ", time.time())
            except:
                print("Oops : Selling not done")

        elif Balance != 0 :
            if myAskPrice != Orderbook.AskPrice :
                try:
                    port.CancelOutDatedOrder(timetosleep)
                    myAskPrice = 0
                except:
                    print('Error on cancelling orders')

        else :

            if (Orderbook.AskPrice - Orderbook.BidPrice) / Orderbook.MidPrice > 0.0075 and myBidPrice == 0.0 :

                print('Spread is above than 1%')

                buyingPrice = Orderbook.BidPrice + Orderbook.BidPrice * 0.0001

                myBidPrice = buyingPrice

                buyingNumber = (50.0 / 100.0) * port.Cash / buyingPrice

                if buyingNumber > Peer.MinTradeSize:
                    print("Buying ", Peer.MarketCurrency.Ccy, " -> ", round(buyingNumber, 2), " at ", round(buyingPrice, 4),
                          " Last = ", round(Peer.Last, 4), " ) ")
                    try:
                        if not port.PlaceBuyOrder(Peer.MarketName, buyingNumber, buyingPrice):
                            print("Error on placing buy order ... Time : ", time.time())
                    except:
                        print("Oops : Buy not done")
                else:
                    print("Buying not done : ", Peer.MarketCurrency.Ccy, " Min Trade size not met -> ",
                          round(Peer.MinTradeSize, 4))

            elif myBidPrice !=  Orderbook.BidPrice and (Orderbook.AskPrice - Orderbook.BidPrice) / Orderbook.MidPrice > 0.0075:
                try:
                    port.CancelOutDatedOrder(timetosleep)
                    myBidPrice = 0.0
                except:
                    print('Error on cancelling orders')
            else :
                print('Spread is : '  + str(round((Orderbook.AskPrice - Orderbook.BidPrice) / Orderbook.MidPrice  * 100, 2)) + ' % ===>  Nothing to do')








