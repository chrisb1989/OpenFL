# import the necessary packages
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

# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((6*9,3), np.float32)
objp[:,:2] = np.mgrid[0:9,0:6].T.reshape(-1,2)

# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.

# function for saving files with numpy
def writeCalFile(filename, data):
	with open(filename, 'w') as outfile:
		outfile.write('# Array shape: {0}\n'.format(data.shape))

		for data_slice in data:
			np.savetxt(outfile, data_slice, fmt='%-7.0f')
			outfile.write('# New slice\n')

# # iterator for first while loop:
# iterator = 0

# # loop over the frames from the video stream
# while iterator < 5:
# 	frame = vs.read()
# 	# convert from BGR color to grayscale:
# 	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
# 	# show the grayscale image feed (for testing)
# 	#cv2.imshow('gray', gray)
# 	# # Find the chess board corners
# 	ret, corners = cv2.findChessboardCorners(gray, (9,6),None)
# 	# # If found, add object points, image points (after refining them)
# 	if ret == True:
# 		objpoints.append(objp)
# 		corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
# 		imgpoints.append(corners2)
# 		# Draw and display the corners
# 		img = cv2.drawChessboardCorners(gray, (9,6), corners2,ret)
# 		# cv2.imshow('frame', frame)
# 		# calibration
# 		#cv2.imshow('img', img)
# 		#cv2.waitKey(0)
# 		ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
# 		time.sleep(.1)
# 		h,  w = img.shape[:2]
# 		newcameramtx, roi=cv2.getOptimalNewCameraMatrix(mtx,dist,(w,h),1,(w,h))
# 		# undistort
# 		# mapx,mapy = cv2.initUndistortRectifyMap(mtx,dist,None,newcameramtx,(w,h),5)
# 		mapx, mapy = cv2.initUndistortRectifyMap(mtx, dist, None, newcameramtx, (w, h), cv2.CV_16SC2)
# 		dst = cv2.remap(img,mapx,mapy,cv2.INTER_LINEAR)
# 		# crop the image
# 		#x,y,w,h = roi
# 		#dst = dst[y:y+h, x:x+w]
# 		cv2.imshow('dst', dst)
# 		iterator += 1
# 		cv2.waitKey(0)


# 	# break the while loop if user presses 'q' key
# 	if cv2.waitKey(1000) & 0xFF == ord('q'):
# 		break

# writeCalFile("mapx.txt", mapx)
# writeCalFile("mapy.txt", mapy)

while True:
	frame = vs.read()
	shapex = (480, 640, 2)
	shapey = (480, 640)
	file_mapx = "mapx.txt"
	file_mapy = "mapy.txt"
	mapx = np.loadtxt(file_mapx)
	mapy = np.loadtxt(file_mapy)
	mapx = mapx.reshape(shapex)
	mapy = mapy.reshape(shapex)
	unwarped = cv2.remap(frame,mapx.astype(np.int16),mapy.astype(np.int16),cv2.INTER_LINEAR)
	cv2.imshow('unwarped', unwarped)
	cv2.waitKey(1)
	# break the while loop if user presses 'q' key
	if cv2.waitKey(1000) & 0xFF == ord('q'):
		break

# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()