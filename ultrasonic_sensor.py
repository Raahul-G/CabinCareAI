import RPi.GPIO as GPIO
import time

class UltraSonicSensor:
    def __init__(self, trigger_pin=13, echo_pin=15):
        self.trigger_pin = trigger_pin
        self.echo_pin = echo_pin
        self.ul = 0
        self.setup_gpio()

    def setup_gpio(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.trigger_pin, GPIO.OUT)
        GPIO.setup(self.echo_pin, GPIO.IN)
        GPIO.setwarnings(False)

    def distance(self):
        GPIO.output(self.trigger_pin, True)
        time.sleep(0.00001)
        GPIO.output(self.trigger_pin, False)

        start_time = time.time()
        stop_time = time.time()

        while GPIO.input(self.echo_pin) == 0:
            start_time = time.time()

        while GPIO.input(self.echo_pin) == 1:
            stop_time = time.time()

        time_elapsed = stop_time - start_time
        distance = (time_elapsed * 34300) / 2
        return distance

    def call(self):
        while True:
            dist = self.distance()
            print("Measured Distance = %.1f cm" % dist)

            if dist < 0.7:
                self.ul = 1
                print("Door is Closed")
                break

            time.sleep(1)

        return self.ul

def main():
    uls = UltraSonicSensor()
    ul = uls.call()
    print("UL:", ul)

if __name__ == "__main__":
    main()
