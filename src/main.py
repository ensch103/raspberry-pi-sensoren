from MCP3008 import MCP3008 as adc
import helper
from time import sleep
from datetime import datetime

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

    ro = helper.read_file("calibrated.txt")
    ro_lpg  = float(ro[0])
    ro_co   = float(ro[1])
    ro_ozon = float(ro[2])
    ro_lq   = float(ro[3])

    values = helper.read_file("curves.txt")
    mq7_steigung_CO  = float(values[0])
    mq7_y_CO         = float(values[1])
    mq7_steigung_LPG = float(values[2])
    mq7_y_LPG        = float(values[3])
    mq7_steigung_CH4 = float(values[4])
    mq7_y_CH4        = float(values[5])

    while True:
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        #TODO: use adc (einkommentieren)
        #value_lpg  = adc.read(channel_mq4)
        #value_co   = adc.read(channel_mq7)
        #value_ozon = adc.read(channel_mq131)
        #value_lq   = adc.read(channel_mq135)
        value_lpg = 100
        value_co = 140
        value_ozon = 120
        value_lq = 130

        #10-Bit AD-Wandler: 2^10 = 1024 Werte: Spannung = (ADC Wert ÷ 1023) * Versorgungsspannung
        volt_lpg  = helper.calc_voltage(value_lpg, vc)
        volt_co   = helper.calc_voltage(value_co, vc)
        volt_ozon = helper.calc_voltage(value_ozon, vc)
        volt_lq   = helper.calc_voltage(value_lq, vc)

        rs_lpg  = helper.calc_resistance(volt_lpg, rl_mq4, vc)
        rs_co   = helper.calc_resistance(volt_co, rl_mq7, vc)
        rs_ozon = helper.calc_resistance(volt_ozon, rl_mq131, vc)
        rs_lq   = helper.calc_resistance(volt_lq, rl_mq135, vc)

        print("volt_LPG: %.2fV    volt_CO: %.2fV    volt_Ozon: %.2fV    volt_LQ: %.2fV" % (volt_lpg, volt_co, volt_ozon, volt_lq)) #TODO: remove
        print("Rs_LPG: %.2f Ohm   Rs_CO: %.2f Ohm   Rs_Ozon: %.2f Ohm   Rs_LQ: %.2f Ohm" % (rs_lpg, rs_co, rs_ozon, rs_lq)) #TODO: remove

        #für jedes Gas, das mit jedem der Sensoren gemessen werden kann (pro Sensor mehr als einen ppm-Wert)
        #mq4_ppm_lpg  = helper.MQGetPercentage(rs_lpg / ro_lpg, )
        mq7_ppm_co   = helper.MQGetPercentage(rs_co / ro_co, mq7_steigung_CO, mq7_y_CO)
        #mq131_ppm_ozon = helper.MQGetPercentage(rs_ozon / ro_ozon, 2)
        #mq135_ppm_lq   = helper.MQGetPercentage(rs_lq / ro_lq, 3)

        with open("results.txt", "a") as file:
            file.write("%s %f %f %f %f" % (dt_string, mq4_ppm_lpg, mq7_ppm_co, mq131_ppm_ozon, mq135_ppm_lq))
        print("ppm co:", mq7_ppm_co) #TODO: remove
        sleep(2)

except KeyboardInterrupt:
    print("Abbruch durch User")
