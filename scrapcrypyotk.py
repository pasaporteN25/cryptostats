from tkinter import *
from tkinter import Tk, Text, ttk, messagebox
from scrapcrypto import *
import time
from calccrypto import *

root = Tk()
root.title("Crypto 101")
root.geometry("800x500")
#root.configure(background="#006")
root.resizable(0,0)

awa = gestorcryptoawa()
usds = dolarhoy()
calc = calculadora()
updateC = IntVar()
statscoin = BooleanVar()
aconvertir = IntVar()

def consulta():
    n = 0
    link = ""
    for dato in awa.coins:
        if dato == monedas.get():
            link = awa.urls[n]
            break
        n=n+1

    tsActual = savetime()
    actAhora = tsActual.getfechayhora()
    #de la misma forma que guardo el tiempo guardo la ultima moneda con timestamp

    #El tiempo de pedido tiene que ser por cada moneda, no general
    #Valores no se borran se pisan en la interfaz

    if actAhora >= 30:
        awa.infoCoin(link)
        ts = tsActual.estampaActual()
        tsActual.guardar(ts)
        mostrarInfoCrypto()
        if updateC.get():
            cotizaBvalue.after(30000, consulta)
    else:
        pass
    #Lo puedo mejorar, updateC es el primer if y duplico el valor de awa.infoCoin
    #O actualiza todas siempre o no actualiza nunca!

    cotizaUvalue.config(text=awa.currentCoinValues[0])

    if monedas.get() != "Bitcoin":
        cotizaBvalue.config(text=awa.currentCoinValues[1])
        #time.sleep(10)
    else:
        awa.currentCoinValues[1] = 1
        cotizaBvalue.config(text="1")



def calcbtars():
    monto = aconvertir.get()
    if monto is not None:
        resp = calc.calcSatoshi(monto)
        outputbtc.config(text=resp)
    else:
        print("Monto no valido!")


    #Actualizar la lista con cierta frecuencia, sino usar una copia en BD que se va a actualizando
    #Primero pisando sin guardar y despues vemos
    #Separar la consulta del boton que muestra el precio.
    #La consulta se genera y no se permite generar otra en menos de 1 min
    #Mientras tanto al gui se le pasa un dato guardado en cache

def mostrarUsd():
    usds.getUSDS()
    usdblue = Label(root, text="USD Blue: \n\n USD Banco Nacion: \n\n USD Bolsa: \n\n USD Liqui: \n\n USD Solidario:").place(x=100, y=270)
    usdblueValuec1 = Label(root, text=usds.cotizacion[0]).place(x=210, y=270)
    usdblueValuev1 = Label(root, text=usds.cotizacion[1]).place(x=260, y=270)
    usdblueValuec2 = Label(root, text=usds.cotizacion[2]).place(x=210, y=300)
    usdblueValuev2 = Label(root, text=usds.cotizacion[3]).place(x=260, y=300)
    usdblueValuec3 = Label(root, text=usds.cotizacion[4]).place(x=210, y=330)
    usdblueValuev3 = Label(root, text=usds.cotizacion[5]).place(x=260, y=330)
    usdblueValuec4 = Label(root, text=usds.cotizacion[6]).place(x=210, y=360)
    usdblueValuev4 = Label(root, text=usds.cotizacion[7]).place(x=260, y=360)
    usdblueValuev5 = Label(root, text=usds.cotizacion[8]).place(x=260, y=390)

def cleanInfo():

    variacion1.config(text='')
    variacion2.config(text='')
    variacion3.config(text='')
    variacion4.config(text='')

    volumen1.config(text='')
    volumen2.config(text='')
    volumen3.config(text='')
    volumen4.config(text='')


def mostrarInfoCrypto():
    if statscoin.get():
        variacion = awa.currentCoinVariation
        volumen = awa.currentCoinVolume
        cleanInfo()

        variacion1.config(text=variacion[0])
        variacion2.config(text=variacion[1])
        variacion3.config(text=variacion[2])
        variacion4.config(text=variacion[3])

        volumen1.config(text=volumen[0])
        volumen2.config(text=volumen[1])
        volumen3.config(text=volumen[2])
        volumen4.config(text=volumen[3])

    elif not statscoin.get():
        cleanInfo()

    #Faltaria hacer que sean configs en lugar de crear las etiquetas todx el tiempo
    #Quiza si inicializo las etiquetas de una...


titulo = Label(root, text="Mundo Crypto 1", fg='#000', font=("Comic Sans", 22))
titulo.place(x=250, y=10)

coinEtiq = Label(root, text="Monedas: ").place(x=20, y=70)
monedas = Spinbox(root, values=awa.coins)
monedas.place(x=100, y=70)
CoinBoton = Button(root, text="Consulta", command=lambda : consulta()).place(x=250, y=68)

#crear un boton de update que condicione un while true dentro de un frame
Checkbutton(root, text="Mantener actualizado", variable=updateC).pack(anchor="w")

#Calculadora ars to btc
inputars = Entry(root, textvariable=aconvertir).place(x=350, y=100)
#inputars.focus()
etiqsatoshi = Label(root, text="  =  ").place(x=450,y=100)
outputbtc = Label(root, text='')
outputbtc.place(x=480, y=100)
etiqbtc = Label(root, text="BTC").place(x=580, y=100)
btnbtccalc = Button(root, text="Calcular", command=lambda : calcbtars()).place(x =550, y= 150)

#Cotizacion de cryptos
cotizaU = Label(root, text="Cotizacion en usd: ").place(x=100, y=130)
cotizaUvalue = Label(root, text="")
cotizaUvalue.place(x=210, y=130)

cotizaB = Label(root, text="Cotizacion en BTC: ").place(x=100, y=170)
cotizaBvalue = Label(root, text="")
cotizaBvalue.place(x=210, y=170)
#cotizaBvalue.after(30000,consulta())
#Agregar horario local
#Hacer de esto una clase?? Como?

#Stats coins tira error si no se hizo primero una consulta
cryptoVar = Label(root, text="Variacion %").place(x=400, y=240)
variacion1 = Label(root, text='')
variacion1.place(x=440, y=270)
variacion2 = Label(root, text='')
variacion2.place(x=440, y=300)
variacion3 = Label(root, text='')
variacion3.place(x=440, y=330)
variacion4 = Label(root, text='')
variacion4.place(x=440, y=360)
cryptoVol = Label(root, text="Volumen %").place(x=500, y=240)
volumen1 = Label(root, text='')
volumen1.place(x=540, y=270)
volumen2 = Label(root, text='')
volumen2.place(x=540, y=300)
volumen3 = Label(root, text='')
volumen3.place(x=540, y=330)
volumen4 = Label(root, text='')
volumen4.place(x=540, y=360)


usdon = Checkbutton(root, text="Ver cotizacion de dolares", onvalue=1, offvalue=0, command=lambda : mostrarUsd()).pack(anchor="w")
Checkbutton(root, text="Ver Stats Coins", onvalue=True, offvalue=False, variable=statscoin,command=lambda : mostrarInfoCrypto()).pack(anchor="w")


comven = Label(root, text="Compra   |   Venta").place(x=210, y=220)



#Condicionar si aparecen o no estos datos
#evaluar la condicion del checkbutton

root.mainloop()

#pido el dato, actualizo la DB si es la primera vez y sino para operar tomo el dato guardado en memoria del programa
#Si no es la primera vez y paso mas de X tiempo en timestamp, actualizo el dato, lo muestro y despues lo guardo
#junto con un nuevo timestamp