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
    ro_mq4   = float(ro[0])
    ro_mq7   = float(ro[1])
    ro_mq131 = float(ro[2])
    ro_mq135 = float(ro[3])

    values = helper.read_file("curves.txt")
    mq4_steigung_CH4      = float(values[0])
    mq4_y_CH4             = float(values[1])
    mq7_steigung_CO       = float(values[2])
    mq7_y_CO              = float(values[3])
    mq131_steigung_ozon   = float(values[4])
    mq131_y_ozon          = float(values[5])
    mq135_steigung_toluol = float(values[6])
    mq135_y_toluol        = float(values[7])
    mq135_steigung_NH3    = float(values[8])
    mq135_y_NH3           = float(values[9])
    mq135_steigung_H2     = float(values[10])
    mq135_y_H2            = float(values[11])

    fileNr = int(helper.read_file("fileNr.txt")[0])
    toInc = fileNr
    fileName = "results" + str(fileNr) + ".txt"
    toInc = toInc + 1
    with open("fileNr.txt", "w") as file:
        file.write(str(toInc))

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

        #print("value_mq4: %.2f    value_mq7: %.2f    value_mq131: %.2f    value_mq135: %.2f" % (value_mq4, value_mq7, value_mq131, value_mq135)) #TODO: remove
        #print("volt_mq4: %.2fV    volt_mq7: %.2fV    volt_mq131: %.2fV    volt_mq135: %.2fV" % (volt_mq4, volt_mq7, volt_mq131, volt_mq135)) #TODO: remove
        #print("Rs_LPG: %.2f Ohm   Rs_CO: %.2f Ohm   Rs_Ozon: %.2f Ohm   Rs_LQ: %.2f Ohm" % (rs_mq4, rs_mq7, rs_mq131, rs_mq135)) #TODO: remove

        #für jedes Gas, das mit jedem der Sensoren gemessen werden kann (pro Sensor mehr als einen ppm-Wert)
        mq4_ppm_CH4      = helper.MQGetPercentage(rs_mq4 / ro_mq4, mq4_steigung_CH4, mq4_y_CH4)
        mq7_ppm_CO       = helper.MQGetPercentage(rs_mq7 / ro_mq7, mq7_steigung_CO, mq7_y_CO)
        mq131_ppm_ozon   = helper.MQGetPercentage(rs_mq131 / ro_mq131, mq131_steigung_ozon, mq131_y_ozon)
        mq135_ppm_toluol = helper.MQGetPercentage(rs_mq135 / ro_mq135, mq135_steigung_toluol, mq135_y_toluol)
        mq135_ppm_NH3    = helper.MQGetPercentage(rs_mq135 / ro_mq135, mq135_steigung_NH3, mq135_y_NH3)
        mq135_ppm_H2     = helper.MQGetPercentage(rs_mq135 / ro_mq135, mq135_steigung_H2, mq135_y_H2)

        with open(fileName, "a") as file:
            file.write("%s %f %f %f %f %f %f %f %f %f %f\n" %(dt_string, rs_mq4, rs_mq7, rs_mq131, rs_mq135,
                         mq4_ppm_CH4, mq7_ppm_CO, mq131_ppm_ozon, mq135_ppm_toluol, mq135_ppm_NH3, mq135_ppm_H2))
        #print("date/time: %s rs_mq4: %f rs_mq7: %f rs_mq131: %f rs_mq135: %f" %(dt_string, rs_mq4, rs_mq7, rs_mq131, rs_mq135))
        print("CH4:    %f ppm\n"
              "CO:     %f ppm\n"
              "Ozon:   %f ppm\n"
              "Toluol: %f ppm\n"
              "NH3:    %f ppm\n"
              "H2:     %f ppm\n" %(mq4_ppm_CH4, mq7_ppm_CO, mq131_ppm_ozon, mq135_ppm_toluol, mq135_ppm_NH3, mq135_ppm_H2))
        sleep(1)

except KeyboardInterrupt:
    print("Abbruch durch User")
