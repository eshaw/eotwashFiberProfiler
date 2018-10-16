from picamera import PiCamera
from time import sleep

#Initialize camera
camera = PiCamera()
 
#Set optimal settings for camera
camera.resolution = (2592, 240)
camera.framerate = 5
camera.shutter_speed = 100
camera.iso = 50
camera.start_preview()
camera.image_effect = 'none'
camera.awb_gains = (0.9,0.0)
camera.awb_mode = 'off'
sleep(5)
camera.exposure_mode = 'off'

#Take picture
camera.capture('test.jpg')

#Close camera
camera.close()