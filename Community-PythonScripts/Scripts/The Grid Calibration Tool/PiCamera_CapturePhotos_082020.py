from imutils.video import VideoStream
import datetime
import argparse
import imutils
import time
import cv2
import numpy as np

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--picamera", type=int, default=-1,
	help="whether or not the Raspberry Pi camera should be used")
args = vars(ap.parse_args())
# initialize the video stream and allow the cammera sensor to warmup
vs = VideoStream(usePiCamera=args["picamera"] > 0).start()
time.sleep(2.0)

iterator = 0

while iterator < 10:
	frame = vs.read()
	filename = "savedImage_"+str(iterator)+".jpg"
	cv2.imshow('Image Capture', frame)
	c = cv2.waitKey(0)
	if c == 32:
		cv2.imwrite(filename, frame)
		iterator += 1
	elif c == 27:
		continue
	elif c == ord('a'):
		break
	