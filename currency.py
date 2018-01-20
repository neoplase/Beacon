from bittrex.bittrex import Bittrex

class currency:
	def __init__(self):
		Ccy = ""
		CcyLong = ""
		MinConfirmation = 0.0
		TxFee = 0.0
		IsActive = False
		CoinType = ""
		BaseAddress = ""

	def GetInformation(self, CcyName):
		BittrexCo = Bittrex(None,None)
		Data = BittrexCo.get_currencies()

		if Data['success']:
			Res = Data['result']
			for item in Res:
				if item['Currency'] == CcyName :
					self.Ccy = item['Currency']
					self.TxFee = item['TxFee']
					self.CcyLong = item['CurrencyLong']
					self.CoinType = item['CoinType']
					self.MinConfirmation = item['MinConfirmation']
					self.IsActive = item['IsActive']
					self.BaseAddress = item['BaseAddress'] 
					return True
			return False

	def Print(self):
		print "Ccy : " , self.Ccy
		print "CcyLong : " , self.CcyLong
		print "TxFee : " , self.TxFee
		print "CoinType : ", self.CoinType
		print "MinConfirmation : " , self.MinConfirmation
		print "IsActive : " , self.IsActive
		print "BaseAddress : " , self.BaseAddress
