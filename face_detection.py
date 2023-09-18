import cv2
import time
import numpy as np 
from scipy import stats

def face_dec():
    global i, a
    i = 0
    a = []
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        frame=cv2.flip(frame, 1)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        i = 0
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 5)

            #Increment iterator for each faces in faces
            i = i + 1

            roi_gray = gray[y:y+h, x:x+w]
            roi_color = frame[y:y+h, x:x+w]
            
            #Display the box and faces
            cv2.putText(frame, 'face num' + str(i), (x-10, y-10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

            a.append(i)

            #cv2.putText(frame, str(i), (10, h - 10), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 5, cv2.LINE_AA)

        cv2.imshow('Test', frame)

        k = cv2.waitKey(1) & 0xff
        if k==27:
            break

    cap.release()
    cv2.destroyAllWindows()

def passenger_count():
    global passenger_count
    m = stats.mode(a)
    passenger_count = int(m[0])
    #return ("Total Passenger Count: ", passenger_count)

def flap():
    if passenger_count == 0:
        print("No passenger detected \nFlap is closed")
    elif passenger_count == 1:
        print("One passenger detected \nFlap Opening for 18 degree")
    elif passenger_count == 2:
        print("Two passenger detected \nFlap Opening for 36 degree")
    elif passenger_count == 3:
        print("Three passenger detected \nFlap Opening for 54 degree")
    elif passenger_count == 4:
        print("Four passenger detected \nFlap Opening for 72 degree")
    elif passenger_count == 5:
        print("Five passenger detected \nFlap Opening for 90 degree")
    else:
        print("Passenger Overloading")

face_dec()

passenger_count()

flap()
