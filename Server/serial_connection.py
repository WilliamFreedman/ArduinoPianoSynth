# piano_server.py (USB serial version)

import serial
import threading
import time

arduino_conn = None  # Will hold the serial.Serial object


def start_serial(port='/dev/tty.usbmodem48CA435D669C2', baud=9600):
    global arduino_conn
    try:
        arduino_conn = serial.Serial(port, baud, timeout=1)
        time.sleep(2)  # Let Arduino reset

        # Send handshake to let Arduino know we're ready
        arduino_conn.write(b"!")

        print(f"Connected to Arduino on {port}")
    except Exception as e:
        print("Failed to open serial port:", e)
        return

    try:
        while True:
            if arduino_conn.in_waiting:
                data = arduino_conn.readline().decode(errors='ignore').strip()
                if data:
                    print(f"Arduino says: {data}")
    except Exception as e:
        print("Serial connection closed:", e)
    finally:
        arduino_conn.close()

def send_to_arduino(message):
    if arduino_conn:
        try:
            if isinstance(message, str):
                message = message.encode()
            arduino_conn.write(message)
            print(f"Sent to Arduino: {message}")
        except Exception as e:
            print("Failed to send to Arduino:", e)
    else:
        print("Arduino not connected.")


# To use this with the GUI, import and start the thread there
if __name__ == "__main__":
    threading.Thread(target=start_serial, daemon=True).start()
    input("Press Enter to quit...\n")
