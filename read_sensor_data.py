import serial
import time

# Open serial port
ser = serial.Serial('COM5', 9600)  # Adjust 'COM3' with your Arduino's port

try:
    while True:
        # Read data from serial port
        data = ser.readline().decode().strip()
        # Split data into NPK values
        npk_values = data.split(',')
        if len(npk_values) == 3:
            nitrogen = float(npk_values[0])
            phosphorous = float(npk_values[1])
            potassium = float(npk_values[2])
            # Process the data as needed
            print("Nitrogen:", nitrogen, "mg/kg")
            print("Phosphorous:", phosphorous, "mg/kg")
            print("Potassium:", potassium, "mg/kg")
        else:
            print("Nitrogen:", nitrogen, "mg/kg")
            print("Phosphorous:", phosphorous, "mg/kg")
            print("Potassium:", potassium, "mg/kg")
        time.sleep(2)  # Delay for 2 seconds
except KeyboardInterrupt:
    ser.close()  # Close serial port on Ctrl+C
