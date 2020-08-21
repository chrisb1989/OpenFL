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

# # termination criteria
# criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
# objp = np.zeros((6*9,3), np.float32)
# objp[:,:2] = np.mgrid[0:9,0:6].T.reshape(-1,2)

# # Arrays to store object points and image points from all the images.
# objpoints = [] # 3d point in real world space
# imgpoints = [] # 2d points in image plane.

camCalDataYaml = open("calibration_matrix.yaml")
camCalData = yaml.load(camCalDataYaml, Loader=yaml.FullLoader)
mtx = np.asarray(camCalData['camera_matrix'])
dist = np.asarray(camCalData['dist_coeff'])


# print("type of mtx is: "+str(type(mtx)))
# print("dir of mtx is: "+str(dir(mtx)))
# print("dir of dist is: "+str(dir(dist)))
# print("type of dist is: "+str(type(dist)))


# loop over the frames from the video stream
while True:
	frame = vs.read()
	# h,  w = frame.shape[:2]
	img = cv2.undistort(frame, mtx, dist)
	# undistort
	# mapx,mapy = cv2.initUndistortRectifyMap(mtx,dist,None,newcameramtx,(w,h),5)
	# img = cv2.remap(frame,mapx,mapy,cv2.INTER_LINEAR)
	# crop the image
	#x,y,w,h = roi
	#dst = dst[y:y+h, x:x+w]
	cv2.imshow("frame", frame)
	cv2.imshow('img', img)
	cv2.waitKey(1)
	# break the while loop if user presses 'q' key
	if cv2.waitKey(1000) & 0xFF == ord('q'):
		break


# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()