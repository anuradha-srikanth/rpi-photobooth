from gpiozero import Button
from time import gmtime, strftime
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import RPi.GPIO as GPIO
import time
from time import gmtime, strftime

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)

on_button = GPIO.input(18)
capture_button = GPIO.input(20)

''' initialize the camera and grab a reference 
to the raw camera capture'''
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))
# edit this to point to an actual location
url = "home/desktop"
output = strftime(url + "/image-%d-%m %H:%M.png", gmtime())

# allow the camera to warmup
time.sleep(0.1)


#there is also a video preview in the camera variable to show live feed
def videofeed_on():
    print "videofeed on"

    # capture frames from the camera
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        # grab the raw NumPy array representing the image, 
        # then initialize the timestamp
        # and occupied/unoccupied text
        image = frame.array

        # show the frame
        cv2.imshow("Frame", image)
        key = cv2.waitKey(1) & 0xFF

        # clear the stream in preparation for the next frame
        rawCapture.truncate(0)

        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            break

def take_picture():
    print "picture should be captured"

    # grab an image from the camera
    camera.capture(rawCapture, format="bgr")
    if output:
        camera.capture(output)
    image = rawCapture.array
     
    # display the image on screen and wait for a keypress
    cv2.imshow("Image", image)
    cv2.waitKey(0)


def next_filter():
    print "add next filter"

while on_button:
    on_button = GPIO.input(18)
    
if on_button == False:
    print('Button Pressed')
    videofeed_on();
    time.sleep(0.2)
    while take_picture:
        take_picture = GPIO.input(20)

if take_picture == False:
    take_picture()
    time.sleep(0.2)






#on_button.when_pressed = videofeed_on()
# capture_button.when_pressed = take_picture()
# next_filter.when_pressed = next_filter()
