# Importation des bibliothèques nécessaires
import smbus
import time
import math
from gps import *
from skyfield.api import load, wgs84

lat, lon = 0 , 0

# Initialisation du GPS
while lat == 0 and lon == 0:
    lat, lon = gps_lat_lon()

# Initialisation de l'IMU
bus = smbus.SMBus(1)
address = 0x68

bus.write_byte_data(address, 0x6b, 0)
time.sleep(0.5)

# Définition des constantes
deg_to_rad = math.pi/180.0

# Chargement des données de la carte du ciel
planets = load('de421.bsp')
earth, _ = planets['earth'], planets['sun']

# Fonction de conversion des données de l'IMU en angles d'élévation et d'azimut
def get_orientation():
    # Lecture des données de l'IMU
    acc_x = bus.read_word_data(address, 0x3b)
    acc_y = bus.read_word_data(address, 0x3d)
    acc_z = bus.read_word_data(address, 0x3f)
    gyro_x = bus.read_word_data(address, 0x43)
    gyro_y = bus.read_word_data(address, 0x45)
    gyro_z = bus.read_word_data(address, 0x47)

    # Conversion des données en unités physiques
    acc_x = acc_x / 16384.0
    acc_y = acc_y / 16384.0
    acc_z = acc_z / 16384.0
    gyro_x = gyro_x / 131.0
    gyro_y = gyro_y / 131.0
    gyro_z = gyro_z / 131.0

    # Calcul de l'angle d'élévation
    pitch = math.atan2(acc_y, math.sqrt(acc_x**2 + acc_z**2))
    pitch = pitch / deg_to_rad

    # Calcul de l'angle d'azimut
    roll = math.atan2(-acc_x, acc_z)
    roll = roll / deg_to_rad
    yaw = gyro_z * 0.001 + math.atan2(math.sin(roll*deg_to_rad)*math.cos(pitch*deg_to_rad), math.cos(roll*deg_to_rad))
    yaw = yaw / deg_to_rad

    return pitch, yaw

# Fonction de récupération des données de position géographique du GPS
# def get_position():
#     while True:
#         report = session.next()
#         if report['class'] == 'TPV':
#             if hasattr(report, 'lat') and hasattr(report, 'lon'):
#                 return report.lat, report.lon

# Fonction de calcul de la position de la visée du télescope
def calculate_target_position():
    # Récupération des données d'orientation et de position
    pitch, yaw = get_orientation()
    ts = load.timescale()
    # lat, lon = get_position()

    # Calcul de la position de la cible sur le ciel
    observer = earth + wgs84.latlon(lat, lon)
    time_now = ts.now()  # Obtient l'instant présent
    ra, dec, _ = observer.at(time_now).radec()

    # Conversion des angles en degrés
    ra = ra.hours * 15
    dec = dec.degrees

    # Calcul de l'angle d'élévation de la cible
    target_elevation = dec - pitch

    # Calcul de l'angle d'azimut de la cible
    target_azimuth = ra - yaw
    if target_azimuth < 0:
        target_azimuth += 360

    # Affichage des résultats
    print("Orientation: Pitch = {:.2f}°, Yaw = {:.2f}°".format(pitch, yaw))
    print("Position: Latitude = {:.6f}, Longitude = {:.6f}".format(lat, lon))
    print("Target position: Elevation = {:.2f}°, Azimuth = {:.2f}°".format(target_elevation, target_azimuth))

    # Retourne la position de la cible
    return target_elevation, target_azimuth

# Fonction de calcul de la position de la cible
def calculate_target_position_test():
    # Récupération des données d'orientation et de position
    pitch, yaw = get_orientation()
    lat, lon = get_position()

    # Calcul de la position de la cible sur le ciel
    observer = earth + wgs84.latlon(lat, lon)
    ra, dec, _ = observer.at(planets['sun']).radec()

    # Conversion des angles en degrés
    ra = ra.hours * 15
    dec = dec.degrees

    # Calcul de l'angle d'élévation de la cible
    target_elevation = dec - pitch

    # Calcul de l'angle d'azimut de la cible
    target_azimuth = ra - yaw
    if target_azimuth < 0:
        target_azimuth += 360

    # Retourne la position de la cible
    return target_elevation, target_azimuth

while True:
    calculate_target_position()
    time.sleep(1)