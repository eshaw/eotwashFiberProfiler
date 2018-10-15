# import the necessary packages
from picamera.array import PiRGBArray, PiYUVArray
from picamera import PiCamera
from threading import Thread
import cv2
import time
from multiprocessing import Process
import io
from Queue import *
from imutils.video import FPS
import collections

class PiVideoStream:
    def __init__(self, resolution=(2592, 240), framerate=8):
        # initialize the camera and stream
        self.queue = Queue()
        #self.queue = collections.deque()
        self.frame_num = 0
        self.camera = PiCamera(sensor_mode=4)
        self.camera.resolution = resolution
        self.camera.framerate = framerate
        self.camera.shutter_speed = 100
        self.camera.iso = 50
        self.camera.image_effect = 'none'
        self.camera.awb_gains = (0.9,0.0)
        self.camera.awb_mode = 'off'
        time.sleep(5.0)
        self.camera.exposure_mode = 'off'
        self.rawCapture = PiRGBArray(self.camera, size=resolution)
        self.stream = self.camera.capture_continuous(self.rawCapture,format="bgr", use_video_port=True)
        #self.rawCapture = PiYUVArray(self.camera, size=resolution)
        #self.stream = self.camera.capture_continuous(self.rawCapture,format="yuv", use_video_port=True)
        #self.stream = io.BytesIO()
        # initialize the frame and the variable used to indicate
        # if the thread should be stopped
        #self.fps = FPS()
        self.frame = None
        self.stopped = False

    def start(self):
        # start the thread to read frames from the video stream
        #Thread(target=self.update, args=()).start()
        #p = Process(target=self.update, args=())
        #p.start()
        #p.join()
        self.update()
        return self
 
    def update(self):
        # keep looping infinitely until the thread is stopped
        #for f in self.stream:
        #self.fps.start()
        print "Starting Update"
        #for f in self.camera.capture_continuous(self.stream, 'bgr', use_video_port=True):
        for f in self.stream:
            # grab the frame from the stream and clear the stream in
            # preparation for the next frame
            #self.stream.seek(0)
            #self.frame = self.stream.getvalue()
            self.frame = f.array
            self.queue.put(self.frame)
            #self.queue.append(self.frame)
            #print(self.frame_num)
            self.frame_num += 1
            #self.stream.seek(0)
            #self.stream.truncate()
            self.rawCapture.truncate(0)
            #self.fps.update()
            # if the thread indicator variable is set, stop the thread
            # and resource camera resources
            if self.stopped:
                self.stream.close()
                self.rawCapture.close()
                self.camera.close()
                #self.fps.stop()
                #print("{:.2f}".format(self.fps.fps()))
                return

    def read(self):
        # return the frame most recently read
        #tmp_num = self.frame_num
        #while tmp_num == self.frame_num:
        #    continue
        return self.frame

    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True
