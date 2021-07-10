import sqlite3
from sqlite3 import Error
import pymongo
from datetime import datetime

class gestormdb:
    def __init__(self):
        self.client = pymongo.MongoClient("mongodb://localhost:27017")
        self.db = self.client["prueba"]
        self.tabla1 = self.db["monedas"]

    def insertar(self,name,url,price,ts):
        self.tabla1.insert_one({
            "nombre": name,
            "url":url,
            "precio":price,
            "timestamp":ts
        })

    #Con esta lista podria ajustar los parametros y generalizar los metodos

    def getList(self,dict):
        return list(dict.keys())

    def buscar(self,nombre):
        query = {
            "nombre":nombre
        }
        resp = self.tabla1.find_one(query)
        key = self.getList(resp)
        #print(resp)
        print(resp[key[3]])

    def actualizar(self,precio):
        self.tabla1.update_one({
            "nombre": "btc",
            "precio": 55000
        }, {
            "$set": {
                "precio": precio
            }

        })


    def eliminar(self,nombre):
        self.tabla1.delete_one({"nombre":nombre})

#-----AWA control------#

    def conexionAwa(self):
        self.db = self.client["CoinsyUrls"]
        tablAwa = self.db["awaData"]
        return tablAwa

    def guardarAwaCoins(self, nombres, urls):
        tablAwa = self.conexionAwa()

        for x in range(0, 200):
            dicc = {"nombre":nombres[x],"url":urls[x]}
            tablAwa.insert_one(dicc)

    def buscarAwaCoins(self, nombre):
        tablAwa = self.conexionAwa()
        query = {"nombre":nombre}
        resp = tablAwa.find_one(query)
        print(resp)

    def traerAwaCoins(self):
        tablAwa = self.conexionAwa()

        nombres = []
        urls = []
        for x in tablAwa.find():
            nombres.append(x['nombre'])
            urls.append(x['url'])

        return nombres,urls


    #------#

    def datoscomprabtc(self):
        self.db = self.client["misMovimientos"]
        self.tabla = self.db["Compras"]

        ars = int(input("Costo en ars: "))
        btc = float(input("Btc recibido: "))
        #El price deberia entrar como int pero hay que ver que no rompa nada
        price = input("1 btc era igual a: ")
        pag = input("Pagina de compra:")

        dia = int(input("dia: "))
        mes = int(input("mes: "))
        fecha = datetime(2021,mes,dia,0,0)

        ts = datetime.timestamp(fecha)


        try:
            self.tabla.insert_one({
                "ars": ars,
                "btc": btc,
                "preciocompleto": price,
                "Pagina: ": pag,
                "timestamp": ts
            })
            print("Guardado en la Base de Datos")
        except TypeError as e:
            print("Ocurrio un error ", e)


    def borrarmibtc(self):
        self.db = self.client["misMovimientos"]
        self.tabla = self.db["Compras"]

        cant = input("cantidad a borrar:")
        btc = float(input("total btc: "))

        try:
            self.tabla.delete_one({"preciocompleto": cant, "btc":btc})
        except TypeError:
            print("No se que paso")


    def traerdatosmisbtc(self):
        self.db = self.client["misMovimientos"]
        tabla = self.db["Compras"]

        totalars = 0
        totalbtc = 0
        preciopromedio = 0
        totaltransf = 0

        for x in tabla.find():
            totalars+=x['ars']
            totalbtc+=x['btc']
            preciopromedio+=int(x['preciocompleto'])
            totaltransf+=1


        print("Total invertido en ars: ",totalars)
        print("BTCs comprados: ", totalbtc)
        print("Precio promedio de compra: ", int(preciopromedio/totaltransf))
        print("Precio promedio en usd: ", int(preciopromedio/(totaltransf*170)))


    def maindatoscomprabtc(self):
        x = True
        while x:
            elec = int(input("1.Guardar 2.Borrar entrada 3.Calculos 4.Salir"))

            if elec == 1:
                self.datoscomprabtc()
            elif elec == 2:
                self.borrarmibtc()
            elif elec == 3:
                self.traerdatosmisbtc()
            elif elec == 4:
                x = False











#gestor = gestormdb()

#gestor.insertar("eth","jk25sdl",5000,123456785)


#gestor.actualizar(53500)

#try:
#    gestor.buscar("eth")
#except AttributeError as e:
#    print("Error por ", e)

#gestor.eliminar("eth")

#Tablas a crear para scrapy:
#
#Nombre y urls para el scrapy
#
#nombre, precio, url si se puede, la procedencia, timestamp
#Y eso hacerlo para que monedas??
#

#mio = gestormdb()
#mio.datoscomprabtc()
#mio.traerdatosmisbtc()