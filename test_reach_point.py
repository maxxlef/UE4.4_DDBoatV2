import time
import sys
import os
import numpy as np
import csv
import quoicouroblib as rb

# Assure-toi que les modules sont correctement importés
sys.path.append(os.path.join(os.path.dirname(__file__), 'drivers-ddboat-v2'))

import imu9_driver_v2 as imudrv
import arduino_driver_v2 as arddrv

# Création des objets IMU et Arduino
imu = imudrv.Imu9IO()
ard = arddrv.ArduinoIO()

"""
Ce fichier permet de rejoindre un point GPS donné en l'occurence par le point A.
Le fichier csv qui est retourné peut être tracé grâce au ficher 'tracer.py'

Fonctions utilisées dans quoicouroblib.py:

    def projection(ly,lx, lym = 48.199170, lxm = -3.014700):

    def mesure_gps(fichier="/mesures/gps_data.txt"):

    def cap_waypoint(a, p):

    def arret_waypoint(a, p):
    
    def regulation_vitesse(distance, vmax=200, vmin=45, coef=1, middle=4):

    def accel():

    def mag():

    def maintien_cap(acc, bouss, cap_voulu, spd, debug=False):
"""

lat_a, long_a = 48.199014999999996, -3.01479833333333
a = rb.projection(lat_a, long_a)

print("Le point GPS voulu est : lattitude = {}, longitude = {}".format(lat_a, long_a))
print("Ces coordonnées dans le plan sont : x = {}, y = {}".format(a[0], a[1]))

filename = 'points_projection.csv'

# Ouvrir le fichier CSV en mode écriture
with open(filename, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['X', 'Y']) # Écrire l'en-tête du fichier
    
    try:
        while True:
            time.sleep(0.5)
            lat, long = rb.gps_dd()
            print("Mesure GPS du point p: lx ={}, ly ={}".format(lat, long))
            p = rb.projection(lat, long)
            writer.writerow([p[0], p[1]]) # Écrire les coordonnées
            print("Les coordonnees de P dans le plan : {}".format(p))
            print("Les coordonnees de A dans le plan : {}".format(a))
            d = a - p # Vecteur de P vers A
            n = d/np.linalg.norm(d)
            northo = np.array([-n[1], n[0]])
            distance = rb.distance_droite(a,northo,p)
            print("Distance au point A : {}".format(distance))

            # Correction du cap
            cap_d = rb.cap_waypoint(a, p)
            print("Cap vise par cap_d : {}°".format(np.degrees(cap_d)))
            acc = rb.accel()
            bouss = rb.mag()
            spd = 120
            rb.maintien_cap(acc, bouss, cap_d, spd)

            # Condition d'arrêt
            if rb.arret_waypoint(a, p) == True:
                print("La bouee à atteint le point gps")
                ard.send_arduino_cmd_motor(0, 0)

    except KeyboardInterrupt:
        print("Programme interrompu par l'utilisateur.")