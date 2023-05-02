import serial
import time
import pynmea2


def gps_lat_lon():
    # Ouvrir le port série sur le Raspberry Pi
    ser = serial.Serial('/dev/ttyAMA0', 9600, timeout=1)

    while True:
        # Lire les données du port série
        data = ser.readline().decode('ascii', errors='replace')

        if data.startswith('$GPGGA'):
            # Analyser les données NMEA à l'aide de la bibliothèque pynmea2
            msg = pynmea2.parse(data)

            return msg.latitude, msg.longitude
            
