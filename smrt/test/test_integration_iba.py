# coding: utf-8

import numpy as np

# local import
from smrt import make_snowpack, make_model, sensor_list

#
# Ghi: rapid hack, should be splitted in different functions
#

def setup_snowpack(l):


    nl = l//2  # // Forces integer division
    thickness = np.array([0.1, 0.1]*nl)
    thickness[-1] = 100  # last one is semi-infinit
    p_ex = np.array([5e-5]*l)
    temperature = np.array([250.0, 250.0]*nl)
    density = [200, 400]*nl

    # create the snowpack
    snowpack = make_snowpack(thickness=thickness,
                             microstructure_model="exponential",
                             density=density,
                             temperature=temperature,
                             corr_length=p_ex)
    return  snowpack

def test_iba_oneconfig_passive():

    # prepare inputs
    snowpack = setup_snowpack(l=2)

    # create the snowpack
    m = make_model("iba", "dort")

    # create the sensor
    radiometer = sensor_list.amsre('37V')

    # run the model
    res = m.run(radiometer, snowpack)

    print(res.TbV(), res.TbH())
    #absorption with effective permittivity
    # abs(res.TbV() - 248.08794944809972) < 1e-4
    # abs(res.TbH() - 237.3056263719142) < 1e-4

    assert abs(res.TbV() - 248.08744066791073) < 1e-4
    assert abs(res.TbH() - 237.30720491883298) < 1e-4



def test_iba_oneconfig_active():

    # prepare inputs
    snowpack = setup_snowpack(l=2)

    # create the snowpack
    m = make_model("iba", "dort")

    # create the sensor
    radar = sensor_list.active(frequency=19e9, theta_inc=55)

    # run the model
    res = m.run(radar, snowpack)

    print(res.sigmaVV_dB(), res.sigmaHH_dB(), res.sigmaHV_dB())

    #assert abs(res.sigmaVV_dB() - (-24.04497237)) < 1e-4
    #assert abs(res.sigmaHH_dB() - (-24.41628343)) < 1e-4
    #assert abs(res.sigmaHV_dB() - (-51.53673914)) < 1e-4
    assert abs(res.sigmaVV_dB() - (-25.784531777404144)) < 1e-4
    assert abs(res.sigmaHH_dB() - (-25.661186004429812)) < 1e-4
    assert abs(res.sigmaHV_dB() - (-32.33796852861883)) < 1e-4
