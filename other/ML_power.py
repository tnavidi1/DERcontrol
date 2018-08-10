import pypower
from pypower.api import runpf, ppoption, makeYbus
from aggregate import aggregate
import numpy as np
from numpy import array
from first_svm import svm_train



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
Processes data and returns new_ppc for each time_step
"""
def prep_data(new_data, old_ppc, time_step):
    #tan of arccos of 0.85 is 0.6197
    p_to_q_factor = 0.6197

    column = new_data[:, time_step]
    old_ppc['bus'][:, 2] = column
    old_ppc['bus'][:, 3] = p_to_q_factor * column

    return old_ppc

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

def runpf_ex(new_data, old_ppc):
    voltage_array = np.zeros((np.size(new_data, 0), np.size(new_data, 1)))

    for i in range(np.size(new_data, 1)):
        new_ppc = prep_data(new_data, old_ppc, i)

        pLoad = new_ppc['bus'][:, 2]
        rLoad = new_ppc['bus'][:, 3]

        voltage = pre_runpf(new_ppc, pLoad, rLoad)
        voltage_array[:, i] = voltage
    return voltage_array

def classify(voltage_array, V_max, V_min):
    over = voltage_array > V_max
    under = voltage_array < V_min
    voltage_array = np.zeros(np.shape(voltage_array))
    voltage_array[over] = 1
    voltage_array[under] = -1
    return voltage_array


if __name__ == '__main__':
    # tan of arccos of 0.85 is 0.6197
    p_to_q_factor = 0.6197
    V_max = 1.01
    V_min = 0.95

    old_ppc = case4gs()
    old_data = np.genfromtxt('res_avg_load_data_5min_2days_no_headers.csv', delimiter=',')

    new_data_real = aggregate(old_data, old_ppc['bus'][:, 2])
    new_data_reactive = new_data_real * p_to_q_factor
    new_data_stacked = np.vstack((new_data_real, new_data_reactive))

    voltage_array = runpf_ex(new_data_real, old_ppc)
    voltage_classified = classify(voltage_array, V_max, V_min)

    print(np.shape(new_data_stacked))
    print(np.shape(voltage_classified))

    svm_train(new_data_stacked.T, voltage_classified[0].T)
    svm_train(new_data_stacked.T, voltage_classified[1].T)
    svm_train(new_data_stacked.T, voltage_classified[2].T)

    print(voltage_classified)