import serial
import time
import numpy as np

def read_data_from_arduino(port, baudrate):
    # Initialize serial connection
    ser = serial.Serial(port, baudrate, timeout=1)
    time.sleep(2)  # Allow time for the connection to establish
    return ser

def main():
    port = 'COM5'  # Adjust the port as necessary
    baudrate = 9600

    ser = read_data_from_arduino(port, baudrate)

    try:
        arr = []
        i = 0
        while i < 30:
            if ser.in_waiting > 0:
                # Read a line of data from the serial port
                line = ser.readline().decode('utf-8').strip()
                i += 1
                # Ensure the data line is not empty
                if not line:
                    continue
                res = line.split(',')

                # Check if the data has at least 4 elements (N, P, K, and moisture)
                if len(res) < 4:
                    continue
                else:
                    try:
                        temp = list(map(float, line.split(',')))
                        arr.append(temp)
                    except ValueError as e:
                        print(f"Error converting data to float: {e}")

                # Short delay between readings
                time.sleep(0.01)

        # Convert the list to a NumPy array
        nparr = np.array(arr)

        # Calculate the mean along the columns
        col_means = np.mean(nparr, axis=0)

        print("Mean along each column:", col_means)

    except KeyboardInterrupt:
        print("Stopping the program.")
    finally:
        ser.close()

if __name__ == "__main__":
    main()
