import time
import cv2
import numpy as np
from scipy import stats
import RPi.GPIO as GPIO
from ard_mer import ard_mer
from ultra_sonic import ultra_sonic

# Global variables
i = 0
a = []
passenger_count = 0
servo1 = None

def initialize_servo():
    global servo1
    # Set GPIO mode
    GPIO.setmode(GPIO.BOARD)
    # Set pin 11 as an output, and set servo1 as pin 11 as PWM
    GPIO.setup(11, GPIO.OUT)
    servo1 = GPIO.PWM(11, 50)  # Note 11 is pin, 50=50Hz pulse
    servo1.start(0)
    time.sleep(2)

def motor(duty):
    if duty <= 7:
        servo1.ChangeDutyCycle(duty)
        time.sleep(1)

def face_detection():
    global i, a
    face_cascade = cv2.CascadeClassifier('/home/pi/opencv/data/haarcascades/haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)
        frame = cv2.resize(frame, (0, 0), fx=0.2, fy=0.2)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        
        i = 0
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 5)
            i += 1
            cv2.putText(frame, 'face num' + str(i), (x - 10, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
            a.append(i)
        
        cv2.imshow('Test', frame)
        k = cv2.waitKey(1) & 0xff
        if k == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

def count_passengers():
    global passenger_count
    m = stats.mode(a)
    passenger_count = int(m[0])

def flap_control(co2_level):
    if co2_level >= 1000:
        if passenger_count == 0:
            print("No passenger detected \nFlap is closed")
        else:
            print(f"{passenger_count} passenger(s) detected")
            duty = 3 + (passenger_count - 1)
            print(f"Flap Opening for {18 * passenger_count} degrees")
            motor(duty)
        
        print('\nWaiting for fresh air to fill in')
        time.sleep(2)
        max = ard_mer()
        co2ppm = max.call()
        print('\nAir refilled')
        print("\nNew CO2 level is {} ppm".format(co2ppm))
        time.sleep(2)
        
        print('\nCO2 under Optimal level')
        print("Flap Closing..")
        servo1.ChangeDutyCycle(2)
        time.sleep(0.5)
        servo1.ChangeDutyCycle(0)

def main():
    print('Starting...System')
    print('\nStarting...Ultrasonic scan')
    uls = ultra_sonic()
    ul = uls.call()
    print("UL:", ul)
    
    if ul == 1:
        print('Opening Camera..')
        face_detection()
        print('\nDetecting the passengers count..')
        count_passengers()
        print('Detected the passengers count Successfully..')
        print("Starting CO2 Sensor..")
        max = ard_mer()
        co2ppm = max.call()
        print("CO2: {} ppm".format(co2ppm))
        print("\nAssuming CO2 level is above optimal level for test case")
        co2_ = 1000
        print("\nStarting Servo Motor")
        initialize_servo()
        flap_control(co2_)
        
        print('\nCycle Completed Successfully..')
    else:
        print('Ultrasonic scan failed.')

if __name__ == "__main__":
    main()
