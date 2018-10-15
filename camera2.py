from __future__ import print_function
from picamera import PiCamera
from time import sleep
import serial
import time
import io
import imutils
from analysistools import *
from scipy.signal import *
from scipy.ndimage.filters import *
#from imutils.video.pivideostream import PiVideoStream
from PiVideoStream import *
from imutils.video import FPS
from picamera.array import PiRGBArray
from threading import Thread
from multiprocessing import Process
import argparse
import cv2
import numpy as np
import matplotlib.pyplot as plt
import psutil, os, sys
import Queue
import datetime
import glob

def analyze_vs(vstream, fps0, args0):
    #print("Starting Analysis")
    current_frame = 0
    rdats = []
    while fps._numFrames < args0["num_frames"]:
        #frame = vstream.read()
        frame = vstream.queue.get()
        #if len(vstream.queue) > 0:
        #    frame = vstream.queue.popleft()
        if frame != None:
            data = np.fromstring(frame, dtype=np.uint8).reshape((240,2592,3))
            r = data[:,:,2] #stream outputs bgr format
            #plt.imshow(r)
            #plt.show()
            #plt.plot(np.mean(r[145:155,:],axis=0))
            #plt.show()
            #rav = np.mean(r[165:185,:],axis=0)
            #bkg = (np.mean(r[155:165,:],axis=0)+np.mean(r[185:195,:],axis=0))/2.
            rav = np.mean(r[133:143,:],axis=0)
            bkg = (np.mean(r[123:133,:],axis=0)+np.mean(r[143:153,:],axis=0))/2.
            rdat = rav - bkg
            rdats.append(rdat)
            #plt.plot(rdat)
            #plt.show()
            #np.savetxt("test%i.dat"%current_frame,r)
            #f = open("test%i.txt"%current_frame,"w+b")
            #f.write(frame)
            #f.close()
            print(current_frame)
            current_frame += 1
        #print frame
            fps0.update()
        #wait until next frame comes in
        #while fps0._numFrames != vstream.frame_num-1:
            #fps.update()
            #continue
    fps0.stop()
    vstream.stop()
    print("{:.2f}".format(fps0.fps()))
    #plt.plot(rdats[0])
    #plt.show()
    #plt.imshow(r)
    #plt.show()
    return rdats

#p = psutil.Process(os.getpid())
#p.nice(10)

# construct the argument parse and parse the args
num_frames = 420
ap = argparse.ArgumentParser()
ap.add_argument("-n","--num-frames", type=int, default=num_frames,
        help="# of frames to loop over")
ap.add_argument("-d", "--display", type=int, default=-1)
ap.add_argument("-t", "--type", choices=['silica', 'tungsten', 'other'], help="specify the type of fiber for filenames")

pargs = vars(ap.parse_args())

#height = 240
height = 1944
width = 2592
ds = []
indices = []
ser = serial.Serial('/dev/ttyACM0')

PicDir = "/home/pi/Desktop/Fiber_Scan_Test/Summer_2017/August_3/"
FilePrefix = "W1.2mil"

vs = PiVideoStream()
fps = FPS().start()
#p = Process(target=analyze_vs,args=(vs, fps, args))
#p.daemon = True
#p.start()
que = Queue.Queue()
ser.write('-3800\n')
Thread(target=lambda q, vs, fps, pargs: q.put(analyze_vs(vs, fps, pargs)),args=(que, vs, fps, pargs)).start()
vs.start()

rdats = que.get()
ser.write('3800\n')
index = 0
start = time.time()
fit = [1e-4,0,0]
for rdat in rdats:
    pdat0, pdat1 = psd(rdat, len(rdat), 1)
    max_vals = argrelextrema(pdat1,np.greater,order=3)[0]
    #plt.loglog(pdat0,np.sqrt(pdat1))
    #plt.loglog(pdat0[max_vals],np.sqrt(pdat1[max_vals]),'x')
    #plt.show()
    maxloc = np.argmax(pdat1[max_vals])
    if max_vals[maxloc] < 8:
        #maxloc = np.argmax(pdat1[max_vals[1:]])
        maxloc = max_vals[maxloc+1]
    else:
        maxloc = max_vals[maxloc]
    #print(pdat0[maxloc])
    #print(maxloc)
    fit[1] = pdat0[maxloc]
    fit[2] = pdat1[maxloc]
    out = lmfitter(pdat0[maxloc-1:maxloc+2],pdat1[maxloc-1:maxloc+2],lorentz,fit)
    #print(out)
    spacing = 1.0/out[1]
    if spacing > 7.:
        diam = 9.5e-3*660e-9/(spacing*1.12e-6)
        print( diam )
        ds.append(diam)
        indices.append(index)
    index += 1
end = time.time()
print(end-start)

#np.savetxt("rdats1-12-8-2017.dat",np.vstack(rdats))
#np.savetxt("qzfiber7-8-10-2018.dat",np.vstack((indices, ds)).transpose())

os.chdir('/home/pi')

today = str(datetime.date.today())
files_today = glob.glob('*' + today + '*')

np.savetxt("qzfiber" + str(len(files_today)) + "-" + today + "_"+ str(pargs.type) + ".dat",np.vstack((indices, ds)).transpose())
"""
for foo in camera.capture_continuous(stream, 'yuv', use_video_port=True):
    #count += 1
    if count == num_ims:
        break
    stream.seek(0)
    data = stream.getvalue()
    #f = open(PicDir+FilePrefix+"-%i.dat"%count,"w+b")
    #f.write(data)
    #f.close()
    ds.append(data)
    stream.truncate()
    count += 1
"""

#endt = time.time()
#print endt - startt
#ser.write('3000')
#ser.write('\n')
