import numpy as np
import numpy.linalg as la
import matplotlib.pyplot as plt

'''MQ4 data'''
#TODO: MQ4, MQ131, MQ135 Geraden
'''MQ7 data'''
ppm_CO    = [50, 100, 400, 1000, 4000]
ratio_CO  = [1.58, 1., 0.363, 0.218, 0.087]

ppm_LPG   = [50, 100, 400, 1000, 4000]
ratio_LPG = [9., 8., 6.6, 6., 5.]

ppm_CH4   = [50, 100, 400, 1000, 4000]
ratio_CH4 = [14.17, 13.53, 12.33, 11.5 , 9]
'''MQ131 data'''
'''MQ135 data'''

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
    mq7_steigung_CO, mq7_y_CO = get_Straight(ppm_CO, ratio_CO)
    mq7_steigung_LPG, mq7_y_LPG = get_Straight(ppm_LPG, ratio_LPG)
    mq7_steigung_CH4, mq7_y_CH4 = get_Straight(ppm_CH4, ratio_CH4)
    #TODO: alle Steigungen und y-Achsenabschnitte
    with open("curves.txt", "w+") as file: #should create file
        #file.write(mq4 daten)
        file.write("%f\n%f\n%f\n%f\n%f\n%f"
                    %(mq7_steigung_CO, mq7_y_CO, mq7_steigung_LPG, mq7_y_LPG, mq7_steigung_CH4, mq7_y_CH4))
        #file.write(mq131 daten)
        #file.write(mq135 daten)
    file.close()

write_curve_data()