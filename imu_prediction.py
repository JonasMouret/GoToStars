import math
import time
import board
import busio
import adafruit_mpu6050
# Set initial time
previous_time = time.time()

# Define the Kalman filter variables
Q_angle = 0.001
Q_gyro = 0.003
R_angle = 0.03





# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Create the MPU6050 instance
mpu = adafruit_mpu6050.MPU6050(i2c)

# Define the conversion factor from raw accelerometer data to degrees
ACC_FACTOR = 180 / math.pi


# Define the Kalman filter function
def kalman_filter(angle, rate, dt):
    # Initialize the Kalman filter variables
    x_angle = 0
    x_bias = 0
    P_00 = 0
    P_01 = 0
    P_10 = 0
    P_11 = 0
    # Time update equations
    x_angle += dt * (rate - x_bias)
    P_00 += -dt * (P_10 + P_01) + Q_angle * dt
    P_01 += -dt * P_11
    P_10 += -dt * P_11
    P_11 += + Q_gyro * dt
    
    # Measurement update equations
    y = angle - x_angle
    S = P_00 + R_angle
    K_0 = P_00 / S
    K_1 = P_10 / S
    
    x_angle += K_0 * y
    x_bias += K_1 * y
    P_00 -= K_0 * P_00
    P_01 -= K_0 * P_01
    P_10 -= K_1 * P_00
    P_11 -= K_1 * P_01
    
    return x_angle

# Main loop
while True:
    # Get current time
    current_time = time.time()

    # Compute time difference
    dt = current_time - previous_time

    # Update previous_time
    previous_time = current_time

    # Read the raw accelerometer data
    accel_x, accel_y, accel_z = mpu.acceleration
    

    # Calculate the roll and pitch angles from the accelerometer data
    roll = math.atan2(accel_y, accel_z) * ACC_FACTOR
    pitch = math.atan2(-accel_x, math.sqrt(accel_y * accel_y + accel_z * accel_z)) * ACC_FACTOR
    
    # Read the raw gyro data
    gyro_x, gyro_y, gyro_z = mpu.gyro
    
    # Calculate the rate of change of the roll and pitch angles from the gyro data
    gyro_x_rate = gyro_x / 131.0
    gyro_y_rate = gyro_y / 131.0
    
    # Calculate the elapsed time since the last loop iteration
    current_time = time.monotonic()
    dt = current_time - previous_time
    previous_time = current_time
    
    # Apply the Kalman filter to the roll angle
    roll_angle = kalman_filter(roll, gyro_x_rate, dt)
    
    # Apply the Kalman filter to the pitch angle
    pitch_angle = kalman_filter(pitch, gyro_y_rate, dt)
    
    # Print the roll and pitch angles
    print("Roll angle: {:.2f}".format(roll_angle))
    print("Pitch angle: {:.2f}".format(pitch_angle))
    
    # Delay until the next loop iteration
    time.sleep(0.01)
