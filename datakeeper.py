import database
import peer

class DataKeeper:
    def __init__(self):
        self.DB = database.Database()
        self.Path = './DB.sql'

    def Init(self):
        return self.DB.Create_Database(self.Path)

    def CreateTable(self):
        Query = "CREATE TABLE "
        Query = Query + "IF NOT EXISTS "
        Query = Query + "MarketData ("
        Query = Query + "MarketName text NOT NULL,"
        Query = Query + "MinTradeSize double,"
        Query = Query + "IsActive integer,"
        Query = Query + "Created text,"
        Query = Query + "High double,"
        Query = Query + "Low double,"
        Query = Query + "Volume double,"
        Query = Query + "Last double,"
        Query = Query + "BaseVolume double,"
        Query = Query + "TimeStamp text,"
        Query = Query + "Bid double,"
        Query = Query + "Ask double,"
        Query = Query + "OpenBuyOrders integer,"
        Query = Query + "OpenSellOrders integer,"

    def Save(self, Peer, Refresh = False):
        return True