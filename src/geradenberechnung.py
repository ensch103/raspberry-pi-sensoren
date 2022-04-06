import numpy as np
import numpy.linalg as la
import matplotlib.pyplot as plt

'''MQ4 data'''
ppm_mq4_CH4   = [400, 1000, 2000, 5000, 9000]
ratio_mq4_CH4 = [0.2, 0.1, 0.07, 0.04, 0.03]
'''MQ7 data'''
ppm_mq7_CO   = [10, 100, 400, 1000]
ratio_mq7_CO = [0.23, 0.063, 0.03, 0.02]
'''MQ131 data'''
ppm_mq131_Ozon   = [0.01, 0.05, 0.1, 0.2, 0.5, 1]
ratio_mq131_Ozon = [1, 2, 2.6, 4, 6, 8]
'''MQ135 data'''
ppm_mq135_toluol   = [10, 100, 200, 500, 1000]
ratio_mq135_toluol = [0.7, 0.31, 0.22, 0.15, 0.11]

ppm_mq135_NH3   = [10, 100, 200, 500, 1000]
ratio_mq135_NH3 = [0.65, 0.26, 0.18, 0.12, 0.09]

ppm_mq135_H2   = [10, 100, 200, 500, 1000]
ratio_mq135_H2 = [0.57, 0.2, 0.13, 0.085, 0.06]

def get_Straight(ppm, ratio):
    assert len(ppm) == len(ratio)
    n = len(ppm)

    ppm_log10 = np.log10(ppm)
    ratio_log10 = np.log10(ratio)

    fig = plt.figure(1)
    plt.plot(ppm, ratio, "g*")
    fig = plt.figure(2)
    plt.plot(ppm_log10, ratio_log10, "r*")

    ''' lineares Ausgleichsproblem '''
    # A*x = v
    # x = (a, b).T

    A = np.hstack((ppm_log10.reshape(n, 1), np.ones_like(ppm_log10).reshape(n, 1)))
    v = ratio_log10.reshape(n, 1)

    a, b = la.solve(A.T @ A, A.T @ v)

    # print(A)
    # print(v)
    # print(a, b)

    # f(x) = a*x + b
    f = lambda x: a * x + b

    xn = np.linspace(1.70, 3.6, 300)
    plt.plot(xn, f(xn))

    return a, b #a:Steigung b:y-Achsenabschnitt

def write_curve_data():
    mq4_steigung_CH4, mq4_y_CH4 = get_Straight(ppm_mq4_CH4, ratio_mq4_CH4)
    mq7_steigung_CO, mq7_y_CO = get_Straight(ppm_mq7_CO, ratio_mq7_CO)
    mq131_steigung_ozon, mq131_y_ozon = get_Straight(ppm_mq131_Ozon, ratio_mq131_Ozon)
    mq135_steigung_toluol, mq135_y_toluol = get_Straight(ppm_mq135_toluol, ratio_mq135_toluol)
    mq135_steigung_NH3, mq135_y_NH3 = get_Straight(ppm_mq135_NH3, ratio_mq135_NH3)
    mq135_steigung_H2, mq135_y_H2 = get_Straight(ppm_mq135_H2, ratio_mq135_H2)
    with open("curves.txt", "w") as file:
        file.write("%f\n%f\n" %(mq4_steigung_CH4, mq4_y_CH4))
        file.write("%f\n%f\n" %(mq7_steigung_CO, mq7_y_CO))
        file.write("%f\n%f\n" %(mq131_steigung_ozon, mq131_y_ozon))
        file.write("%f\n%f\n" %(mq135_steigung_toluol, mq135_y_toluol))
        file.write("%f\n%f\n" %(mq135_steigung_NH3, mq135_y_NH3))
        file.write("%f\n%f\n" %(mq135_steigung_H2, mq135_y_H2))
    file.close()

write_curve_data()