from MCP3008 import MCP3008 as adc
import helper
#from mq import *
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

#adc = MCP3008()

try:
    print("Press CTRL+C to abort.")
    #mq = MQ()

    ro = helper.read_file("Ro.txt")
    ro_lpg  = ro[0]
    ro_co   = ro[1]
    ro_ozon = ro[2]
    ro_lq   = ro[3]
    print("ro_lpg:", ro_lpg, "ro_co:", ro_co, "ro_ozon:", ro_ozon, "ro_lq:", ro_lq)
    while True:
        value_lpg  = adc.read(channel_mq4)
        value_co   = adc.read(channel_mq7)
        value_ozon = adc.read(channel_mq131)
        value_lq   = adc.read(channel_mq135)

        #10-Bit AD-Wandler: 2^10 = 1024 Werte: Spannung = (ADC Wert ÷ 1023) * Versorgungsspannung
        volt_lpg  = helper.calc_voltage(value_lpg, vc)
        volt_co   = helper.calc_voltage(value_co, vc)
        volt_ozon = helper.calc_voltage(value_ozon, vc)
        volt_lq   = helper.calc_voltage(value_lq, vc)

        rs_lpg  = helper.calc_resistance(volt_lpg, rl_mq4, vc)
        rs_co   = helper.calc_resistance(volt_co, rl_mq7, vc)
        rs_ozon = helper.calc_resistance(volt_ozon, rl_mq131, vc)
        rs_lq   = helper.calc_resistance(volt_lq, rl_mq135, vc)

        ppm_lpg  = helper.MQGetGasPercentage(rs_lpg / ro_lpg, 0)
        ppm_co   = helper.MQGetGasPercentage(rs_co / ro_co, 1)
        ppm_ozon = helper.MQGetGasPercentage(rs_ozon / ro_ozon, 2)
        ppm_lq   = helper.MQGetGasPercentage(rs_lq / ro_lq, 3)

        print("volt_LPG: %.2fV    volt_CO: %.2fV    volt_Ozon: %.2fV    volt_LQ: %.2fV" % (volt_lpg, volt_co, volt_ozon, volt_lq))
        print("Rs_LPG: %.2f Ohm   Rs_CO: %.2f Ohm   Rs_Ozon: %.2f Ohm   Rs_LQ: %.2f Ohm" % (rs_lpg, rs_co, rs_ozon, rs_lq))

        sleep(1)
except KeyboardInterrupt:
    print("Abbruch durch User")
