from gpiozero import Button
from time import gmtime, strftime
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np
import RPi.GPIO as GPIO
# import time
from time import gmtime, strftime



GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(20, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#on_button = GPIO.input(18)
#capture_button = GPIO.input(20)

''' initialize the camera and grab a reference 
to the raw camera capture'''
camera = PiCamera()
camera.resolution = (320, 240)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(320, 240))
# edit this to point to an actual location
url = "/home/pi/Documents/rpi-photobooth/pictures"
output = strftime(url + "/image-%d-%m %H:%M.png", gmtime())

# allow the camera to warmup
time.sleep(0.1)


#there is also a video preview in the camera variable to show live feed
def videofeed_on():
    print "videofeed on"

    face_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_eye.xml')

    # capture frames from the camera
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        # grab the raw NumPy array representing the image, 
        # then initialize the timestamp
        # and occupied/unoccupied text

        image = frame.array
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # show the frame
        faces = face_cascade.detectMultiScale(gray, 1.3, 5) 
        print len(faces)
        for (x,y,w,h) in faces:
            cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,0),2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = image[y:y+h, x:x+w]
            eyes = eye_cascade.detectMultiScale(roi_gray)
            for (ex,ey,ew,eh) in eyes:
                cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
        
        cv2.imshow("Frame", image)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()
        key = cv2.waitKey(1) & 0xFF

        # clear the stream in preparation for the next frame
        rawCapture.truncate(0)

        '''
        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            break
            '''
        capture_button = GPIO.input(20);
        if capture_button == False: break

def take_picture():
    print "picture should be captured"

    # grab an image from the camera
    camera.capture(rawCapture, format="bgr")
    if output:
        print "Picture saved"
        camera.capture(output)
    image = rawCapture.array

    # display the image on screen and wait for a keypress
    cv2.imshow("Image", image)
    #capture_button = GPIO.input(20)
    #while capture_button:
    #    capture_button = GPIO.input(20)
    # interval = 0
    cv2.waitKey(10000)
    
    # cv2.waitKey(1)
    # cv2.destroyAllWindows()
    # cv2.waitKey(1)
    print "Finished waiting"
    # on_button = GPIO.input(18)
    # if on_button == False:
    #     videofeed_on()

def next_filter():
    print "add next filter"

def main():
    while True:
        on_button = GPIO.input(18)
        while on_button:
            on_button = GPIO.input(18)

        if on_button == False:
            print('Button Pressed')
            videofeed_on()
            #time.sleep(0.2)
            take_picture()

main()
'''
    while take_picture:
        print "Hello"
        take_picture = GPIO.input(20)
    

if take_picture == False:
    take_picture()
    time.sleep(0.2)
    '''

#on_button.when_pressed = videofeed_on()
# capture_button.when_pressed = take_picture()
# next_filter.when_pressed = next_filter()

