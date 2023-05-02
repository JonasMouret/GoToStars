import smbus
import time

# Adresse I2C de l'IMU
IMU_ADDRESS = 0x68

# Adresse des registres
POWER_REG = 0x6B
ACC_CONFIG_REG = 0x1C
GYRO_CONFIG_REG = 0x1B
ACC_X_REG = 0x3B
ACC_Y_REG = 0x3D
ACC_Z_REG = 0x3F
GYRO_X_REG = 0x43
GYRO_Y_REG = 0x45
GYRO_Z_REG = 0x47

# Définir l'adresse du bus I2C
bus = smbus.SMBus(1)

# Activer l'IMU
bus.write_byte_data(IMU_ADDRESS, POWER_REG, 0)
print("IMU activé")

# Configurer l'IMU pour une plage de mesure de +/- 2g pour l'accéléromètre et +/- 250 degrés/s pour le gyroscope
bus.write_byte_data(IMU_ADDRESS, ACC_CONFIG_REG, 0x00)
bus.write_byte_data(IMU_ADDRESS, GYRO_CONFIG_REG, 0x00)

# Fonction pour lire les valeurs de l'IMU
def read_raw_data(reg):
    # Lecture des données brutes sur 16 bits à partir du registre spécifié, avec un codage complément à deux pour les valeurs négatives
    high = bus.read_byte_data(IMU_ADDRESS, reg)
    low = bus.read_byte_data(IMU_ADDRESS, reg + 1)
    value = (high << 8) | low
    if value > 32767:
        value -= 65536
    return value

# Calibrer l'IMU
print("Calibration de l'IMU...")
sum_x = 0
sum_y = 0
sum_z = 0
n = 2000
for i in range(n):
    # Lire les valeurs brutes de l'IMU
    x = read_raw_data(ACC_X_REG)
    y = read_raw_data(ACC_Y_REG)
    z = read_raw_data(ACC_Z_REG)
    print("x =", x, "y =", y, "z =", z)
    # Ajouter les valeurs à la somme totale
    sum_x += x
    sum_y += y
    sum_z += z
    # Attendre 10 ms avant de lire la prochaine valeur
    time.sleep(0.01)
# Calculer les valeurs moyennes
offset_x = sum_x / n
offset_y = sum_y / n
offset_z = sum_z / n
print("Offsets : X =", offset_x, "Y =", offset_y, "Z =", offset_z)
