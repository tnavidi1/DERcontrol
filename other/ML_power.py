import pypower
import sklearn
from sklearn import preprocessing
from pypower.api import runpf, ppoption, makeYbus
from aggregate import aggregate
import numpy as np
from numpy import array
from first_svm import svm_train
from keras_first_network import nn_train
from sampling import Resampling
from forecaster_primitive import predict
import matplotlib.pyplot as plt



def case4gs():
    """Power flow data for 4 bus, 2 gen case from Grainger & Stevenson.
    Please see L{caseformat} for details on the case file format.

    This is the 4 bus example from pp. 337-338 of I{"Power System Analysis"},
    by John Grainger, Jr., William Stevenson, McGraw-Hill, 1994.

    @return: Power flow data for 4 bus, 2 gen case from Grainger & Stevenson.
    """
    ppc = {"version": '2'}

    ##-----  Power Flow Data  -----##
    ## system MVA base
    ppc["baseMVA"] = 100.0

    ## bus data
    # bus_i type Pd Qd Gs Bs area Vm Va baseKV zone Vmax Vmin
    ppc["bus"] = array([
        [0, 1, 50, 30.99, 0, 0, 1, 1, 0, 230, 1, 1.1, 0.9],
        [1, 1, 170, 105.35, 0, 0, 1, 1, 0, 230, 1, 1.1, 0.9],
        [2, 1, 200, 123.94, 0, 0, 1, 1, 0, 230, 1, 1.1, 0.9],
        [3, 2, 80, 49.58, 0, 0, 1, 1, 0, 230, 1, 1.1, 0.9]
    ])

    ## generator data
    # bus, Pg, Qg, Qmax, Qmin, Vg, mBase, status, Pmax, Pmin, Pc1, Pc2,
    # Qc1min, Qc1max, Qc2min, Qc2max, ramp_agc, ramp_10, ramp_30, ramp_q, apf
    ppc["gen"] = array([
        [3, 318, 0, 100, -100, 1.00, 100, 1, 318, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        #[0, 0, 0, 100, -100, 1, 100, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ])

    ## branch data
    # fbus, tbus, r, x, b, rateA, rateB, rateC, ratio, angle, status, angmin, angmax
    ppc["branch"] = array([
        [0, 1, 0.01008, 0.0504, 0.1025, 250, 250, 250, 0, 0, 1, -360, 360],
        [0, 2, 0.00744, 0.0372, 0.0775, 250, 250, 250, 0, 0, 1, -360, 360],
        [1, 3, 0.00744, 0.0372, 0.0775, 250, 250, 250, 0, 0, 1, -360, 360],
        [2, 3, 0.01272, 0.0636, 0.1275, 250, 250, 250, 0, 0, 1, -360, 360]
    ])

    return ppc


"""
Runs runpf on the ppc and returns the voltage ppc
"""
def pre_runpf(ppc, pLoad, rLoad):
    ppc['bus'][:, 2] = pLoad.flatten()
    ppc['bus'][:, 3] = rLoad.flatten()

    ppopt = ppoption(VERBOSE=0, OUT_ALL=0)  # this is just so the function does not print the output when run

    ppc_out = runpf(ppc, ppopt)
    runVoltage = ppc_out[0]['bus'][:, 7]

    return runVoltage


def runpf_ex(real_power, reactive_power, ppc):
    voltage_array = np.zeros((np.size(real_power, 0), np.size(real_power, 1)))

    for i in range(np.size(real_power, 1)):
        pLoad = real_power[:,i]
        rLoad = reactive_power[:,i]

        voltage = pre_runpf(ppc, pLoad, rLoad)
        voltage_array[:, i] = voltage
    return voltage_array

def classify(voltage_array, V_max, V_min):
    #for i in range(np.size(voltage_array, 0)):
        #print(i, np.mean(voltage_array[i]))
    over = voltage_array > V_max
    under = voltage_array < V_min
    voltage_array = np.zeros(np.shape(voltage_array))

    voltage_array[over] = 1
    voltage_array[under] = -1

    #print(voltage_array)
    return voltage_array

def svm_ML(new_data_stacked, voltage_classified):
    svm_train(new_data_stacked.T, voltage_classified[30].T)
    #svm_train(new_data_stacked.T, voltage_classified[60].T)
    #svm_train(new_data_stacked.T, voltage_classified[80].T)
    #svm_train(new_data_stacked.T, voltage_classified[100].T)
    #svm_train(new_data_stacked.T, voltage_classified[120].T)

def nn_ML(new_data_stacked, voltage_classified, loss, activation_1, activation_2, activation_3, epochs, batch_size):
    nn_train(new_data_stacked.T, voltage_classified.T, loss, activation_1, activation_2, activation_3, epochs, batch_size)


if __name__ == '__main__':
    print('program beginning')

    #NON-SOLAR

    '''
    # tan of arccos of 0.85 is 0.6197
    p_to_q_factor = 0.6197
    V_max = 1.0
    V_min = 0.97
    
    network_data = np.load('/Users/waelabid/Desktop/Research/DERcontrol/other/network_data.npz')
    old_ppc = network_data['ppc'][()]
    old_ppc['gen'][:,5] = 1.022
    '''

    '''
    print(old_ppc['bus'])
    old_data = np.genfromtxt('res_avg_load_data_5min_2days_no_headers.csv', delimiter=',')

    new_data_real = aggregate(old_data, old_ppc['bus'][:, 2])
    new_data_reactive = new_data_real * p_to_q_factor
    new_data_stacked = np.vstack((new_data_real, new_data_reactive))

    voltage_array = runpf_ex(new_data_real, old_ppc)
    voltage_classified = classify(voltage_array, V_max, V_min)

    np.savez('ML_power', new_data_stacked=new_data_stacked, voltage_classified=voltage_classified)
    '''

    #SOLAR



    '''
    training_data = np.load('ML_power.npz')
    new_data_stacked = training_data['new_data_stacked']
    voltage_classified = training_data['voltage_classified']

    #new_data_stacked_normalized = sklearn.preprocessing.normalize(new_data_stacked)
    #nn_ML(new_data_stacked_normalized, voltage_classified, 'binary_crossentropy', 'linear', 'linear', 'tanh', 300, 25)
    #svm_ML(new_data_stacked_normalized, voltage_classified)

    node_idx = [1, 7, 15, 22, 30, 37, 45, 52, 60] #do not modify reactive power, only real power (first half of the array)
    solar_penetration = 0.15

    DataDict = np.load('/Users/waelabid/Desktop/Research/DERcontrol/other/solar_data.npz')
    sNormFull = np.matrix(DataDict['sNormFull'])

    res = Resampling(sNormFull, 60, 5)
    sNormFull_upsampled = res.upsampling(sNormFull, 60, 5, np.size(new_data_stacked, 1))

    for i in node_idx:
        solar = predict(np.array(solar_penetration), 0.03) * np.mean(new_data_stacked[i]) * predict(sNormFull_upsampled, 0.05)
        new_data_stacked[i] -= solar.flatten()


    #re-classifying after adding solar
    voltage_array = runpf_ex(new_data_stacked[:np.size(new_data_stacked, 0)/2], new_data_stacked[np.size(new_data_stacked, 0)/2:], old_ppc)
    voltage_classified = classify(voltage_array, V_max, V_min)
    print(voltage_classified[30])

    plt.figure(0)
    plt.plot(voltage_array[30])
    plt.plot(0.97)
    plt.plot(1)
    plt.show()

    over = 0
    under = 0
    within = 0
    for i in range(np.size(voltage_classified, 0)):
        for j in range(np.size(voltage_classified, 1)):
            if voltage_classified[i,j] > 0:
                over += 1
            elif voltage_classified[i,j] < 0:
                under += 1
            else:
                within += 1
    print('over, under, within')
    print(over, under, within)

    np.savez('ML_power_solar', new_data_stacked=new_data_stacked, voltage_classified=voltage_classified, voltage_array=voltage_array)
    '''




    training_data = np.load('ML_power_solar.npz')
    new_data_stacked = training_data['new_data_stacked']
    voltage_classified = training_data['voltage_classified']
    voltage_array = training_data['voltage_array']

    #print(voltage_classified[30])


    #print(np.shape(voltage_classified))
    #print(voltage_classified)
    #print(np.shape(voltage_array))
    #print(voltage_array)
    new_data_stacked_normalized = sklearn.preprocessing.normalize(new_data_stacked)
    #print(np.shape(new_data_stacked_normalized))


    '''
    over = 0
    under = 0
    within = 0
    for i in range(np.size(voltage_classified, 0)):
        print(i, voltage_classified[i])
        for j in range(np.size(voltage_classified, 1)):
            if voltage_classified[i, j] > 0:
                over += 1
            elif voltage_classified[i, j] < 0:
                under += 1
            else:
                within += 1
    print('over, under, within')
    print(over, under, within)
    '''

    #nodes over chosen: 1, 6, 12, 35, 55
    #nodes within chosen: 57, 63
    #nodes under chosen: 64, 65, 78, 120

    #nn_ML(new_data_stacked, voltage_classified, 'binary_crossentropy', 'linear', 'linear', 'tanh', 100, 10)
    svm_ML(new_data_stacked, voltage_classified)
