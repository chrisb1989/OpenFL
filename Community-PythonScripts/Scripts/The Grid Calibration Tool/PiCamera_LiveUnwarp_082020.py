# import the necessary packages
from imutils.video import VideoStream
import datetime
import argparse
import imutils
import time
import cv2
import numpy as np
import yaml

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--picamera", type=int, default=-1,
	help="whether or not the Raspberry Pi camera should be used")
args = vars(ap.parse_args())
# initialize the video stream and allow the cammera sensor to warmup
vs = VideoStream(usePiCamera=args["picamera"] > 0).start()
time.sleep(2.0)

# import the calibration data
camCalDataYaml = open("calibration_matrix.yaml")
camCalData = yaml.load(camCalDataYaml, Loader=yaml.FullLoader)
mtx = np.asarray(camCalData['camera_matrix'])
dist = np.asarray(camCalData['dist_coeff'])

# a function that finds the brightest spot and draws a circle around it
def brightSpot():
	# create a grey version of the stream
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	# apply a Gaussian blur to the grey version then find the brightest region
	gray = cv2.GaussianBlur(gray, (5, 5, 0))
	(minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(gray)
	cv2.circle(img, maxLoc, 5, (255, 0, 0), 2)
	# display the results in a window called LaserPoint
	# wait 1 millisecond
	cv2.waitKey(1)


# loop over the frames from the video stream
while True:
	frame = vs.read()
	# unwarp the stream
	img = cv2.undistort(frame, mtx, dist)
	# run the brightSpot function to find the laser point
	brightSpot()
	cv2.imshow("LaserPoint", img)
	# break the while loop if user presses 'q' key
	if cv2.waitKey(1000) & 0xFF == ord('q'):
		break


# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()