import smbus
import math
import time

# Adresse I2C du module GY-521
address = 0x68

# Initialise le bus I2C
bus = smbus.SMBus(1)

# Configure l'IMU
bus.write_byte_data(address, 0x6B, 0x00)
bus.write_byte_data(address, 0x1B, 0x08)

# Lit les données de l'IMU
def read_word(address, register):
    high = bus.read_byte_data(address, register)
    low = bus.read_byte_data(address, register + 1)
    value = (high << 8) + low
    return value

# Convertit une valeur signée de 16 bits en entier
def convert_to_int(data):
    if data > 32767:
        data = data - 65536
    return data

# Calcule la position en degrés
def get_position():
    # Lit les données de l'accéléromètre et du gyroscope
    acc_x = read_word(address, 0x3B)
    acc_y = read_word(address, 0x3D)
    acc_z = read_word(address, 0x3F)
    gyro_x = read_word(address, 0x43)
    gyro_y = read_word(address, 0x45)
    gyro_z = read_word(address, 0x47)

    # Convertit les données en entiers signés
    acc_x = convert_to_int(acc_x)
    acc_y = convert_to_int(acc_y)
    acc_z = convert_to_int(acc_z)
    gyro_x = convert_to_int(gyro_x)
    gyro_y = convert_to_int(gyro_y)
    gyro_z = convert_to_int(gyro_z)

    # Calcule l'angle d'inclinaison en radians
    roll = math.atan2(acc_y, acc_z)
    pitch = math.atan2(-acc_x, math.sqrt(acc_y * acc_y + acc_z * acc_z))

    # Convertit l'angle d'inclinaison en degrés
    roll = math.degrees(roll)
    pitch = math.degrees(pitch)

    # Calcule la rotation totale en degrés
    dt = 0.01 # intervalle de temps entre deux lectures (en secondes)
    gyro_x = gyro_x / 131
    gyro_y = gyro_y / 131
    gyro_z = gyro_z / 131

    rotation_x = gyro_x * dt
    rotation_y = gyro_y * dt
    rotation_z = gyro_z * dt

    # Ajoute la rotation à l'angle d'inclinaison
    roll = roll + rotation_x
    pitch = pitch + rotation_y

    # Retourne les angles d'inclinaison et de rotation
    return (roll, pitch, rotation_z)

while True:
    roll, pitch, rotation_z = get_position()
    print("roll=%.2f pitch=%.2f rotation_z=%.2f" % (roll, pitch, rotation_z))
    time.sleep(1)

