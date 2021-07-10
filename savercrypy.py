from datetime import *
from datetime import timedelta
import time
import pickle
import json
import csv


class savetime:

    def listarMonedas(self):
        print("Monedas")


    def estampaActual(self):
        ts = time.time()
        ts = int(ts)
        return ts

    def guardar(self, ts):
        with open("../a.bat", "wb") as f:
            pickle.dump(ts, f)



    def getfechayhora(self):

        ts = self.estampaActual()
        diferencia = 0

        with open("../a.bat", "rb") as f:
            archivo = pickle.load(f)
            #leer = datetime.utcfromtimestamp(archivo)
            diferencia = ts - archivo

        #Si no existe la crea, si existe la manipula el archivo dat

        return diferencia


        #1 Hora = 3.600s
        #1 Dia = 86.400
        #1 Semana = 604800
        #1 Mes (30.44 dias) = 2.629.743
        #1 Año (365.24 dias) =







#Para la actualizacion de la tabla hacerlo siempre a un horario fijo por dia, semana o mes
#Hacerlo sin preguntar
#
#El modulo tiene que actualizar o bien la tabla o bien los datos de la moneda en particular
#Como controlo el tiempo??

