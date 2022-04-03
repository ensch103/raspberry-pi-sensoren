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

def MQGetGasPercentage(self, rs_ro_ratio, gas_id):
    if (gas_id == self.GAS_LPG):
        return self.MQGetPercentage(rs_ro_ratio, self.LPGCurve)
    elif (gas_id == self.GAS_CO):
        return self.MQGetPercentage(rs_ro_ratio, self.COCurve)
    elif (gas_id == self.GAS_OZON):
        return self.MQGetPercentage(rs_ro_ratio, self.OzoneCurve)
    elif (gas_id == self.GAS_LQ):
        return self.MQGetPercentage(rs_ro_ratio, self.AirQualityCurve)
    return 0

def MQGetPercentage(self, rs_ro_ratio, pcurve):
    return 0
    # y = mx+b
    #return (math.pow(10, (((math.log10(rs_ro_ratio) - pcurve[1]) / pcurve[2]) + pcurve[0])))