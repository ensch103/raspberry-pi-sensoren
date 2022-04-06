from MCP3008 import MCP3008
import geradenberechnung
from mq import *

try:
    print("Press CTRL+C to abort.")
    #mq = MQ();
    geradenberechnung.write_curve_data()
    while True:
        #hier sind auch die Clean_air_faktoren wichtig
        #kalibrieren
        print("Calibrating...")
        self.Ro = self.MQCalibration(self.MQ_PIN)
        #berechnete Werte für ro in Datei "calibrated.txt" schreiben (Reihenfolge: lpg, co, ozon, lq)
        ro_lpg = 1000
        ro_co = 2000
        ro_ozon = 1200
        ro_lq = 1300
        with open("calibrated.txt", "w") as file:
            print("%f" % (ro_lpg), file=file)
            print("%f" % (ro_co), file=file)
            print("%f" % (ro_ozon), file=file)
            print("%f" % (ro_lq), file=file)
except KeyboardInterrupt:
    print("Abbruch durch User")
