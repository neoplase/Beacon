from sklearn.linear_model import LinearRegression

class Model:

    def __init__(self):
        self.Constant = 0
        self.Coefficients = []
        self.TimeWindow = 0
        self.jLag = 0

    def Calibrate(self,Orderbooks, timeWindow, jLag):
        if len(Orderbooks) < timeWindow + jLag + 1 :
            self.TimeWindow = timeWindow
            self.jLag = jLag

            PriceChanges = []

            for i in range(1,len(Orderbooks) - self.TimeWindow):
                tmp = 0

                for j in range(1, self.TimeWindow):
                    tmp = tmp + (Orderbooks[i+j].MidPrice - Orderbooks[i].MidPrice)/self.TimeWindow

                PriceChanges.append(tmp)


        else :
            print("Not Enough Data to calibrate")
            return False

    def PriceChangePrediction(self, Orderbooks):
                return 0