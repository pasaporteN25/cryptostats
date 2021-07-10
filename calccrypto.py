from scrapcrypto import *

class calculadora:

    def __init__(self):
        self.dolar = dolarhoy()
        self.awa = gestorcryptoawa()
        self.usd = self.dolar.usdsListInt()
        self.btc = self.awa.infoCoinRanking()


    def btctoars(self):

        return self.usd*self.btc


    def calcSatoshi(self,monto):
        #1 satoshi = 0.00000001 BTC


        satoshinars = self.btctoars()/100000000
        res = int(monto/satoshinars)/100000000
        #satoshis to btc=
        res = '{:.9f}'.format(res)
        print('Precios usados: ', self.usd,' / ',self.btc) #En btc

        #Diferencia con los ars depende de la cotizacion
        #satoshinusd = self.btc/1000000000
        #print((monto/int(self.usd))*satoshinusd)

        return res




#calc = calculadora()

#print(calc.calcSatoshi(1000))