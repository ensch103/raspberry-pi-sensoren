import time
import math
from MCP3008 import MCP3008

def read_file(file):
    values = []
    with open(file, "r") as file:
        for zeile in file:
            values.append(zeile)
    return values


def calc_voltage(value, vc):
    return (value / 1023.0) * vc


def calc_resistance(volt, rl, vc):
    return ((vc / volt) - 1) * rl

def MQGetPercentage(rs_ro_ratio, steigung, y_achsenabschnitt):
    # y = mx+b
    # x = (y - b) / m
    # 10, (((math.log10(rs_ro_ratio) - pcurve[1]) / pcurve[2]) + pcurve[0]))
    print("rs_ro_ratio:", rs_ro_ratio, "y-Achsenabschnitt:", y_achsenabschnitt, "steigung:", steigung)
    concentration_ppm = math.pow(10, (rs_ro_ratio - y_achsenabschnitt) / steigung)
    return concentration_ppm
