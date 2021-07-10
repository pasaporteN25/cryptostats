from bs4 import BeautifulSoup
import requests
import json

class dolars:
    def __init__(self):
        print("iniciando usds counter")
        self.orousd()


    def usdwan(self):
        req = requests.get('https://mercados.ambito.com//dolarrava/cl/variacion').json()
        return req['compra']

    def spmervalwan(self):
        req = requests.get('https://mercados.ambito.com//indice/.merv/variacion-ultimo').json()
        return req['ultimo']

    def orousd(self):
        req = requests.get('https://mercados.ambito.com//metales/oro-nueva-york/variacion-ultimo').json()
        return req['venta']

    def oilusd(self):
        req = requests.get('https://mercados.ambito.com//petroleo/variacion-ultimo').json()
        return req['ultimo']


#x = dolars()
