from bs4 import BeautifulSoup
import requests
from savercrypy import savetime
from scryptodb import *
import json

class gestorcryptoawa:

    def __init__(self):
        #awebanalysis
        self.url = 'https://awebanalysis.com/es/'
        self.coins = []
        self.urls = []
        self.currentCoinValues = []
        self.currentCoinVariation = []
        self.currentCoinVolume = []

        self.traerMoedas()


    def getMonedas(self,page):
        monedas = requests.get(self.url+'crypto-currencies-monitor-price/{}/'.format(page))
        soup = BeautifulSoup(monedas.content, 'html.parser')
        datos = soup.find_all('a', {'class': 'crypto_name crypto_name_break'})
        return datos


    def traerMoedas(self):
        x = False
        save = gestormdb()
        if x:
            self.listarMonedas()
            save.guardarAwaCoins(self.coins, self.urls)
            #Aca se guardan los datos
        else:
            self.coins, self.urls = save.traerAwaCoins()


        #Puedo implementar un modulo que permita al usuario actualizar la lista




    def listarMonedas(self):
        #Porque este gestiona los pedidos
        #Aca tengo que revisar hace cuanto se actualizo
        #Y si no esta la variable busco en el congif.json
        #Listo solo las primeras 200 x capitalizacion
        for x in range(0,4):
            datos = self.getMonedas(x+1)
            for item in datos:
                self.coins.append(item.text.strip('\n '))
                self.urls.append(item['href'])
        #despues deberia sacar la listade estas variables como algo global?? o que hacer?


    def infoCoin(self,link):
        req = requests.get(link)
        #Se puede mejorar el pedido de detalles?
        soup = BeautifulSoup(req.content, 'html.parser')
        cotizacion = soup.find_all('td', {'class': 'wbreak_word align-middle coin_price'})
        variaciones = soup.find_all('td', {'class': 'fz16'})
        volumen = soup.find_all('td', {'class': 'coin_price_3'})
        #otrosindicadores = soup.find_all('td',{'class':'coin_price_2'})

        self.currentCoinValues.clear()
        for dato in cotizacion:
            self.currentCoinValues.append(dato.text)
            if link == "https://awebanalysis.com/es/coin-details/bitcoin/":
                self.currentCoinValues.append("₿1")


        self.currentCoinVariation.clear()
        for dato in variaciones:
            self.currentCoinVariation.append(dato.text.strip('\n'))

        self.currentCoinVolume.clear()
        for n in range(0, len(volumen)):
            self.currentCoinVolume.append(volumen[n].text)

        #Funciona de las dos formas

    def infoCoinRanking(self):

        req = requests.get('https://coinranking.com/es/moneda/Qwsogvtv82FCd+bitcoin-btc')
        #req = requests.get('http://coinranking.com/es')
        soup = BeautifulSoup(req.content, 'html.parser')
        #resp = soup.find_all('a', {'profile__link'})
        #print(resp[0]['href'])
        #print(resp[0].text)
        #print(btcprice.strip('\n\n\n$'))
        resp = soup.find_all('div',{'class':'coin-overview__price'})
        btcp = resp[0].text
        btcprice = ''.join(ch for ch in btcp if ch.isdigit())
        btcprice = float(btcprice)/100

        #API KEY
        #coinranking1270bdc3b853e6339eaf3c4b21dfc36ba531b9b3fa7431c4

        return btcprice




class dolarhoy:

    def __init__(self):
        self.url = 'https://www.dolarhoy.com/cotizaciondolar'
        self.tipos = ['blue', 'oficial', 'bolsa', 'contadoconliqui', 'turista']
        self.cotizacion = []


    def getUSDS(self):

        for n in self.tipos:
            add = self.url+n
            pedido = requests.get(add)
            soup = BeautifulSoup(pedido.content, 'html.parser')
            precio = soup.find_all('div', {'class': 'value'})
            self.cotizacion.append(precio[0].text)
            if (n != 'turista'):
                self.cotizacion.append(precio[1].text)

        return self.cotizacion

    def usdsListInt(self):
        usds = self.getUSDS()

        usd = float(usds[7].strip('$'))
        #Retornando el precio del dolar contado con liqui de venta

        return usd

class cryptoapiconsume:
    def __init__(self):
        #/Qwsogvtv82FCd btc
        self.url = 'https://api.coinranking.com/v2/coin/'
        self.headers = {
            'Accepts':'application/json',
            'x-access-token':'coinranking1270bdc3b853e6339eaf3c4b21dfc36ba531b9b3fa7431c4',
        }

        self.uuids = []
        self.coinNames = []
        self.allmarketCap = []
        self.coinPrices = []
        self.coinBPrices = []
        self.cambios24hs = []
        self.ranks = []
        self.Volumenes24hs = []
        self.allCoins()



    def allCoins(self):
        self.url = 'https://api.coinranking.com/v2/coins?limit=100'
        resp = requests.get(self.url, headers=self.headers)
        json_data = json.loads(resp.text)
        for x in range(0,99):
            #print(json_data["data"]["coins"][x]['name'])
            self.uuids.append(json_data["data"]["coins"][x]['uuid'])
            self.coinNames.append(json_data["data"]["coins"][x]['name'])
            self.allmarketCap.append(json_data["data"]["coins"][x]['marketCap'])
            self.coinPrices.append(json_data["data"]["coins"][x]['price'])
            self.coinBPrices.append(json_data["data"]["coins"][x]['btcPrice'])
            self.cambios24hs.append(json_data["data"]["coins"][x]['change'])
            self.ranks.append(json_data["data"]["coins"][x]['rank'])
            self.Volumenes24hs.append(json_data["data"]["coins"][x]['24hVolume'])


    #Campos a ver, dentro de "data":{total de monedas, etc}
    #"coins":[{ uuid,symbol, name, marketCap, price, btcPrice, change (es en 24hs), rank, 24hVolume}]
    #sparkline es otro dato que trae un array de datos para generar un grafico sencillo

    def elegirMoneda(self,moneda):
        encontrado = False
        x = 0
        for dato in self.coinNames:
            if moneda == dato:
                print("Encontrado!")
                encontrado = True
                break
            else:
                encontrado = False
            x+=1

        if encontrado:
            print("Datos de", moneda)
            print("uuid: ", self.uuids[x])
            print("Capitalizacion: $", int(float(self.allmarketCap[x])))
            print("Precio: $", self.coinPrices[x])
            print("Precio BTC: ", self.coinBPrices[x])
            print("Variacion 24hs: ", self.cambios24hs[x])
            print("Volumen 24hs", self.Volumenes24hs[x])




    def ordenarData(self):
        pass



#awa = gestorcryptoawa()


#usds = dolarhoy()
#usds.usdsListInt()
#coinranking api = hotmail + api key: coinranking1270bdc3b853e6339eaf3c4b21dfc36ba531b9b3fa7431c4
#https://developers.coinranking.com/api/documentation/

#app = cryptoapiconsume()
#app.elegirMoneda('Cardano')


#awa.traerMoedas()

#1 Satoshi		0.00038857 USD	0.00000001
#10 Satoshi		0.00388574 USD	0.00000010
#100 Satoshi		0.03885741 USD	0.00000100 	1 Bit / μBTC (you-bit)
#1,000 Satoshi		0.38857406 USD	0.00001000
#10,000 Satoshi		3.88574061 USD	0.00010000
#100,000 Satoshi		38.85740612 USD	0.00100000 	1 mBTC (em-bit)
#1,000,000 Satoshi	388.5740612 USD	0.01000000 	1 cBTC (bitcent)
#10,000,000 Satoshi	3,885.740612 USD	0.10000000
#100,000,000 Satoshi	38,857.406122 USD	1.00000000 	1 Bitcoin - BTC
#
#
#
#
#
#
