import time
import math
from MCP3008 import MCP3008

#TODO:clean air Faktoren
MQ4_RO_CLEAN_AIR_FACTOR   = 9.83
MQ7_RO_CLEAN_AIR_FACTOR   = 9.83
MQ131_RO_CLEAN_AIR_FACTOR = 9.83
MQ135_RO_CLEAN_AIR_FACTOR = 9.83

CALIBARAION_SAMPLE_TIMES = 50  # define how many samples you are going to take in the calibration phase
CALIBRATION_SAMPLE_INTERVAL = 500  # define the time interval(in miliseconds) between each samples in the cablibration phase

def MQCalibration(mq_pin, ro_clean_air_factor, rl, vc):
    adc = MCP3008()
    val = 0.0
    for i in range(CALIBARAION_SAMPLE_TIMES):  # take multiple samples
        volt = calc_voltage(adc.read(mq_pin), vc)
        val += calc_resistance(volt, rl, vc)
        time.sleep(CALIBRATION_SAMPLE_INTERVAL / 1000.0)

    val = val / CALIBARAION_SAMPLE_TIMES  # calculate the average value
    val = val / ro_clean_air_factor  # divided by RO_CLEAN_AIR_FACTOR yields the Ro according to the chart in the datasheet
    return val

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
    print("rs_ro_ratio:", rs_ro_ratio, "y-Achsenabschnitt:", y_achsenabschnitt, "steigung:", steigung)
    concentration_ppm = math.pow(10, (math.log10(rs_ro_ratio) - y_achsenabschnitt) / steigung)
    return concentration_ppm
