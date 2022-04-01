from MCP3008 import MCP3008
from mq import *
from time import sleep

# MQ4: Erdgas- und Methansensor (LPG)
# MQ7: CO-Sensor (CO)
# MQ131: Ozonsensor (Ozon)
# MQ135: Luftqualitätssensor (LQ)

vc = 5  # Versorgungsspannung in Volt
# Lastwiderstand RL für die jeweiligen Sensoren in Ohm
rl_mq4   = 1488
rl_mq7   = 1461
rl_mq131 = 1000
rl_mq135 = 1474
# channel am AD-Wandler, an dem die jeweiligen Sensoren angeschlossen sind
channel_mq4   = 0
channel_mq7   = 1
channel_mq131 = 2
channel_mq135 = 3

adc = MCP3008()

def calc_voltage(value, vc):
    return (value / 1023.0) * vc

def calc_resistance(volt, rl, vc):
    return ((vc / volt) - 1) * rl

try:
    print("Press CTRL+C to abort.")
    mq = MQ();
    while True:
        value_lpg = adc.read(channel_mq4)
        value_co = adc.read(channel_mq7)
        value_ozon = adc.read(channel_mq131)
        value_lq = adc.read(channel_mq135)

        #10-Bit AD-Wandler: 2^10 = 1024 Werte: Spannung = (ADC Wert ÷ 1023) * Versorgungsspannung
        volt_lpg  = calc_voltage(value_lpg, vc)
        volt_co   = calc_voltage(value_co, vc)
        volt_ozon = calc_voltage(value_ozon, vc)
        volt_lq   = calc_voltage(value_lq, vc)

        rs_lpg  = calc_resistance(volt_lpg, rl_mq4, vc)
        rs_co   = calc_resistance(volt_co, rl_mq7, vc)
        rs_ozon = calc_resistance(volt_ozon, rl_mq131, vc)
        rs_lq   = calc_resistance(volt_lq, rl_mq135, vc)

        print("volt_LPG: %.2fV    volt_CO: %.2fV    volt_Ozon: %.2fV    volt_LQ: %.2fV" % (volt_lpg, volt_co, volt_ozon, volt_lq))
        print("Rs_LPG: %.2f Ohm   Rs_CO: %.2f Ohm   Rs_Ozon: %.2f Ohm   Rs_LQ: %.2f Ohm" % (rs_lpg, rs_co, rs_ozon, rs_lq))

        sleep(1)
except KeyboardInterrupt:
    print("Abbruch durch User")
