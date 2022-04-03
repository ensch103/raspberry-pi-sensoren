import time
import math
from MCP3008 import MCP3008

GAS_LPG  = 0
GAS_CO   = 1
GAS_OZON = 2
GAS_LQ   = 3

#LPGCurve = []
#COCurve = []
#OzoneCurve = []
#AirQualityCurve = []

def read_file(file):
    ro = []
    with open(file, "r") as file:
        for zeile in file:
            ro.append(zeile)
    return ro

def calc_voltage(value, vc):
    return (value / 1023.0) * vc

def calc_resistance(volt, rl, vc):
    return ((vc / volt) - 1) * rl

def MQGetGasPercentage(rs_ro_ratio, gas_id):
    if (gas_id == GAS_LPG):
        return MQGetPercentage(rs_ro_ratio, y_lpg, steigung_lpg)
    elif (gas_id == GAS_CO):
        return MQGetPercentage(rs_ro_ratio, y_co, steigung_co)
    elif (gas_id == GAS_OZON):
        return MQGetPercentage(rs_ro_ratio, y_ozon, steigung_ozon)
    elif (gas_id == GAS_LQ):
        return MQGetPercentage(rs_ro_ratio, y_lq, steigung_lq)
    return 0

def MQGetPercentage(rs_ro_ratio, y_achsenabschnitt, steigung):
    return 0
    # y = mx+b
    # x = (y - b) / m
    # 10, (((math.log10(rs_ro_ratio) - pcurve[1]) / pcurve[2]) + pcurve[0]))
    concentration_ppm = math.pow10((rs_ro_ratio - y_achsenabschnitt) / steigung)
    return concentration_ppm