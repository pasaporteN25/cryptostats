from tkinter import *
from tkinter import Tk, Text, ttk, messagebox
import time
#
import numpy as np
import matplotlib.pyplot as plt
#
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
#
from scrapcrypto import *
#from calccrypto import *
from dolar101 import *


class guicrypto:
    def __init__(self):
        self.root = Tk()
        self.root.title("Aconcagua Crypto")
        self.root.geometry("1000x630")
        self.root.resizable(0, 0)
        self.listademonedas()
        self.datosvarios()
        self.cabecera()
        self.centro()

        self.ml()


    def datosvarios(self):
        lista = ["Vol 24hs", "en btc", "propio", "Cap. en USD", "Cap. en btc", "Circ. disp.", "Circ. total", "Circ. max/total", "Cambio 24hs", "Cambio % 1h"
                 , "Cambio % 24hs", "Cambio % 7d", "Otros camb.", "Cambio 24hs btc", "Cambio % 1h ", "Cambio % 24h"]
        #podria tener esta lista serializada en un pickle o en mongo? seria mejor??


        for n in range(0,16):
            self.varyvolinfo.insert(n, lista[n])


    def placedolar(self):
        #dolar = dolarhoy().usdsListInt()
        dolar = dolars()
        self.dolares = Label (self.framehead, text="Dolar ref {}".format(dolar.usdwan()),font=("Comic Sans", 15))
        self.dolares.grid(row=0, column=0)
        self.sypm = Label(self.framehead, text="| S&P Merval {}".format(dolar.spmervalwan()),font=("Comic Sans", 15))
        self.sypm.grid(row=0, column=1)
        self.gold = Label(self.framehead, text="| Gold {}".format(dolar.orousd()),font=("Comic Sans", 15))
        self.gold.grid(row=0, column=2)
        self.oil = Label(self.framehead, text="| Petróleo {}".format(dolar.oilusd()), font=("Comic Sans", 15))
        self.oil.grid(row=0, column=3)


    def cajabajo(self):
        #frame para la calculadora de ars to crypto con reflejo de los usd que serian
        pass

    def centro(self):
        self.framecenter = Frame(self.root)
        self.framecenter.place(x=385, y=70)
        fig = Figure(figsize=(6,5), dpi=100)
        #x = np.arange(0, 5, .01)
        #y = 10 * np.pi * x

        plot = fig.add_subplot(111) #.plot(x, y)
        plot.plot(np.random.randint(100, size=[6]))
        plt.show()

        canvas = FigureCanvasTkAgg(fig, master=self.framecenter)
        canvas.draw()

        toolbar = NavigationToolbar2Tk(canvas, self.framecenter, pack_toolbar=False)
        toolbar.update()

        canvas.mpl_connect("key_press_event", lambda event: print(f"you pressed {event.key}"))
        canvas.mpl_connect("key_press_event", key_press_handler)

        #button = Button(master=self.framecenter, text="Quit", command=self.framecenter.quit)
        #button.pack(side=BOTTOM)
        toolbar.pack(side=BOTTOM, fill=X)
        canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)



    def cabecera(self):

        self.framehead = Frame(self.root)
        self.framehead.place(x=200, y=15)
        self.framehead.config(bd = 5, bg="black")
        #yield
        self.placedolar()

        #El dolar me genera delay al iniciar
        #Traer dato de base de datos y despues pedirlo mientras se ejecuta el programa


    def datosMoneda(self):
        self.precio = Label(self.root, font=("Comic Sans", 22))
        self.precio.place(x=10, y=15)

        self.cotizacionCoin = Label(self.root, font=("Comic Sans", 22))
        self.cotizacionCoin.place(x=210, y=60)
        self.cotizacionCoin1 = Label(self.root, font=("Comic Sans", 15))
        self.cotizacionCoin1.place(x=210, y=110)

        frame1 = Frame(self.root)
        frame1.place(x=140, y=150)

        self.varyvolinfo = Listbox(frame1, width=18, height=17)
        self.varyvolinfo.config(bg="white")
        self.varyvolinfo.grid(row=0, column=0)
        self.varyvol = Listbox(frame1, width=20, height=17)
        self.varyvol.config(bg="gray")
        self.varyvol.grid(row=0, column=1)



    def callback(self,event):
        eleccion = event.widget.curselection()
        if eleccion:
            index = eleccion[0]
            data = event.widget.get(index)
            x = 0
            for dato in self.awa.coins:
                if dato == data:
                    link = self.awa.urls[x]
                    self.awa.infoCoin(link)
                    self.ultimaselec = dato
                    break
                else:
                    x+=1

            self.precio.config(text=data)
            self.cotizacionCoin.config(text=self.awa.currentCoinValues[0])
            self.cotizacionCoin1.config(text=self.awa.currentCoinValues[1])
            self.varyvol.delete(0, 'end')
            x=0

            try:
                for y in range(0, 8):
                    self.varyvol.insert(y, self.awa.currentCoinVariation[y])

                for y in range(0, 8):
                    self.varyvol.insert(y, self.awa.currentCoinVolume[y])
            except IndexError as e:
                print("Accediste al Bitcoin, arregla el ", e)


        else:
            self.precio.config(text="")



    def listademonedas(self):
        self.awa = gestorcryptoawa()
        self.datosMoneda()

        frame = Frame(self.root)
        frame.place(x=10, y=50)

        monedas = Listbox(frame, width=20, height=25)
        for y in range(0,200):
            monedas.insert(y,self.awa.coins[y])

        monedas.bind("<<ListboxSelect>>", self.callback)

        monedas.pack()



    def ml(self):
        self.root.mainloop()



#PS>C:\Users\Lucas\AppData\Roaming\Python\Python39\Scripts> .\pyinstaller --onefile cryptostats\main.py

