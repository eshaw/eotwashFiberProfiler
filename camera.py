from picamera import PiCamera
from time import sleep
import serial

camera = PiCamera()
ser = serial.Serial('/dev/ttyACM0')
 

camera.resolution = (2592, 240)
camera.framerate = 5
camera.shutter_speed = 100
camera.iso = 50
camera.start_preview()
#camera.exposure_mode = 'sports'
camera.image_effect = 'none'
camera.awb_gains = (0.9,0.0)
camera.awb_mode = 'off'
#camera.contrast = 10
sleep(5)
camera.exposure_mode = 'off'
#camera.start_recording('/home/pi/Desktop/Fiber_Scan_Test/Sep_27/Motor_Freq_Test/Hz3200SpeedTest/Speed_0.07.h264')
for i in range(0,1,1):
    #curStr = str(i)
    #ser.write('%d\n' %i)
    #ser.write('-10\n')
    #sleep(1)
    #camera.capture('/home/pi/Desktop/Fiber_Scan_Test/Fall_2017/December_6/Qz2-%s.jpg'%i)
    camera.capture('Qztest.jpg')
    #ser.write('-10\n')
    #sleep(1)
#camera.stop_recording()
speed = camera.exposure_speed
print('the speed is %d' %speed )
camera.stop_preview()
#ser.write('4000\n')
