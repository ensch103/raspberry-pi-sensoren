from MCP3008 import MCP3008
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

adc = MCP3008()

try:
    print("Press CTRL+C to abort.")

    ro = helper.read_file("calibrated.txt")
    ro_lpg  = float(ro[0])
    ro_co   = float(ro[1])
    ro_ozon = float(ro[2])
    ro_lq   = float(ro[3])

    values = helper.read_file("curves_backup.txt")
    mq7_steigung_CO  = float(values[0])
    mq7_y_CO         = float(values[1])
    mq7_steigung_LPG = float(values[2])
    mq7_y_LPG        = float(values[3])
    mq7_steigung_CH4 = float(values[4])
    mq7_y_CH4        = float(values[5])

    while True:
        now = datetime.now()
        dt_string   = now.strftime("%d/%m/%Y %H:%M:%S")
        value_mq4   = adc.read(channel_mq4)
        value_mq7   = adc.read(channel_mq7)
        value_mq131 = adc.read(channel_mq131)
        value_mq135 = adc.read(channel_mq135)

        #10-Bit AD-Wandler: 2^10 = 1024 Werte: Spannung = (ADC Wert ÷ 1023) * Versorgungsspannung
        volt_mq4   = helper.calc_voltage(value_mq4, vc)
        volt_mq7   = helper.calc_voltage(value_mq7, vc)
        volt_mq131 = helper.calc_voltage(value_mq131, vc)
        volt_mq135 = helper.calc_voltage(value_mq135, vc)

        rs_mq4   = helper.calc_resistance(volt_mq4, rl_mq4, vc)
        rs_mq7   = helper.calc_resistance(volt_mq7, rl_mq7, vc)
        rs_mq131 = helper.calc_resistance(volt_mq131, rl_mq131, vc)
        rs_mq135 = helper.calc_resistance(volt_mq135, rl_mq135, vc)

        print("value_mq4: %.2fV    value_mq7: %.2fV    value_mq131: %.2fV    value_mq135: %.2fV" % (value_mq4, value_mq7, value_mq131, value_mq135)) #TODO: remove
        print("volt_mq4: %.2fV    volt_mq7: %.2fV    volt_mq131: %.2fV    volt_mq135: %.2fV" % (volt_mq4, volt_mq7, volt_mq131, volt_mq135)) #TODO: remove
        print("Rs_LPG: %.2f Ohm   Rs_CO: %.2f Ohm   Rs_Ozon: %.2f Ohm   Rs_LQ: %.2f Ohm" % (rs_mq4, rs_mq7, rs_mq131, rs_mq135)) #TODO: remove

        #für jedes Gas, das mit jedem der Sensoren gemessen werden kann (pro Sensor mehr als einen ppm-Wert)
        #mq4_ppm_lpg  = helper.MQGetPercentage(rs_lpg / ro_lpg, )
        mq7_ppm_co   = helper.MQGetPercentage(rs_mq7 / ro_co, mq7_steigung_CO, mq7_y_CO)
        #mq131_ppm_ozon = helper.MQGetPercentage(rs_ozon / ro_ozon, 2)
        #mq135_ppm_lq   = helper.MQGetPercentage(rs_lq / ro_lq, 3)

        with open("results.txt", "a") as file:
            file.write("%s %f %f %f %f %f" % (dt_string, rs_mq4, rs_mq7, rs_mq131, rs_mq135, mq7_ppm_co))
        print("ppm co:", mq7_ppm_co) #TODO: remove
        sleep(2)

except KeyboardInterrupt:
    print("Abbruch durch User")
