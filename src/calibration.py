import geradenberechnung
import helper

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

ro_clean_air_factor_mq4   = 1
ro_clean_air_factor_mq7   = 1
ro_clean_air_factor_mq131 = 1
ro_clean_air_factor_mq135 = 1

try:
    print("Calibrating... Press CTRL+C to abort.")
    geradenberechnung.write_curve_data()

    ro_mq4   = helper.MQCalibration(channel_mq4, ro_clean_air_factor_mq4, rl_mq4, vc)
    ro_mq7   = helper.MQCalibration(channel_mq7, ro_clean_air_factor_mq7, rl_mq7, vc)
    ro_mq131 = helper.MQCalibration(channel_mq131, ro_clean_air_factor_mq131, rl_mq131, vc)
    ro_mq135 = helper.MQCalibration(channel_mq135, ro_clean_air_factor_mq135, rl_mq135, vc)

    #berechnete Werte für ro in Datei "calibrated.txt" schreiben (Reihenfolge: mq4, mq7, mq131, mq135)
    with open("calibrated.txt", "w") as file:
        file.write("%f" % (ro_mq4))
        file.write("%f" % (ro_mq7))
        file.write("%f" % (ro_mq131))
        file.write("%f" % (ro_mq135))

except KeyboardInterrupt:
    print("Abbruch durch User")
