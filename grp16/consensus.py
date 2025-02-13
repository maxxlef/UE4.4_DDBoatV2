import socket
import sys
import os
import time
import quoicouroblib as rb
import numpy as np

# Assure-toi que les modules sont correctement importés
sys.path.append(os.path.join(os.path.dirname(__file__), 'drivers-ddboat-v2'))

import imu9_driver_v2 as imudrv
import arduino_driver_v2 as arddrv
import gps_driver_v2 as gpsdrv


# Création des objets IMU et Arduino
imu = imudrv.Imu9IO()
ard = arddrv.ArduinoIO()

print("Debut")
numero_bateau = socket.gethostname()[6:8]

filename ="calib_" + numero_bateau + ".txt"
print(int(numero_bateau))
print(filename)
rb.calc_b_A_from_file(filename)
t0=time.time()

def mission_jour_2():
    lat_m=48.20010  
    long_m=-3.01573
    rb.suivre_vecteur(int(numero_bateau), t0,lat_m,long_m)

while True:
    try:
        mission_jour_2()
    except :
        if KeyboardInterrupt:
            break
        else:
            pass
