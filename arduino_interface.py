import serial

class ArduinoInterface:
    def __init__(self, i=0, max_ppm=0, ppm=0):
        self.i = i
        self.max_ppm = max_ppm
        self.ppm = ppm

    def connect_to_arduino(self, port='/dev/ttyACM0', baud_rate=9600):
        ser = serial.Serial(port, baud_rate, timeout=1)
        ser.flush()
        return ser

    def read_and_update_ppm(self, ser):
        while self.i <= 10:
            read_serial = ser.readline().decode('utf-8').rstrip()
            if len(read_serial) > 0:
                self.ppm = int(read_serial)
            if self.max_ppm < self.ppm:
                self.max_ppm = self.ppm
            self.i += 1

    def call(self):
        try:
            arduino_port = '/dev/ttyACM0'
            arduino_baud_rate = 9600

            ser = self.connect_to_arduino(arduino_port, arduino_baud_rate)
            self.read_and_update_ppm(ser)

            return self.max_ppm

        except serial.SerialException:
            print("Arduino communication error.")
            return None

def main():
    arduino = ArduinoInterface()
    max_ppm = arduino.call()

    if max_ppm is not None:
        print("Max CO2 PPM:", max_ppm)

if __name__ == "__main__":
    main()
