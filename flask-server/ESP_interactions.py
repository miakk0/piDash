import serial

def read_sensor_data(esp_port):
    baud_rate = 9600
    """Read temperature and humidity from ESP8266 and update the GUI."""
    try:
        with serial.Serial(esp_port, baud_rate, timeout=1) as ser:
            while True:
                raw_data = ser.readline().decode('utf-8').strip()
                if raw_data:
                    data = raw_data.split()
                    return {"humidity": data[0], "temperature": data[1]}
    except serial.SerialException:
        return f"Invalid serial port name: {esp_port}"
    except UnicodeDecodeError:
        return f"Error reading from serial port: {esp_port}"