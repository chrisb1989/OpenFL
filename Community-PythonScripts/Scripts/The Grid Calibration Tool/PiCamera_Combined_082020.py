# import the necessary packages
from imutils.video import VideoStream
import datetime
import argparse
import imutils
import time
import cv2
import numpy as np
import yaml
import glob

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--picamera", type=int, default=-1,
	help="whether or not the Raspberry Pi camera should be used")
args = vars(ap.parse_args())
# initialize the video stream and allow the cammera sensor to warmup
vs = VideoStream(usePiCamera=args["picamera"] > 0).start()
time.sleep(2.0)

def selectOptions():
	print(""" \n
		Enter A Number to Select An Option, then press Enter: \n
		1) Capture Calibration Images \n
		2) Run Calibration Routine \n
		3) View Calibrated Image Stream \n
		""")
	selection = raw_input()
	if int(selection) == 1:
		captureImages()
	elif int(selection) == 2:
		imageCalibration()
	elif int(selection) == 3:
		viewStream()
	else:
		print("You Must Select A Number")

def captureImages():
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
	cv2.destroyAllWindows()

def imageCalibration():
	# termination criteria
	criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
	# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
	objp = np.zeros((6*9,3), np.float32)
	objp[:,:2] = np.mgrid[0:9,0:6].T.reshape(-1,2)
	# Arrays to store object points and image points from all the images.
	objpoints = [] # 3d point in real world space
	imgpoints = [] # 2d points in image plane.

	images = glob.glob(r'savedImage_*.jpg')

	# path = 'results'
	# pathlib.Path(path).mkdir(parents=True, exist_ok=True) 

	found = 0
	for fname in images:  # Here, 10 can be changed to whatever number you like to choose
	 	img = cv2.imread(fname) # Capture frame-by-frame
		#print(images[im_i])
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		# Find the chess board corners
		ret, corners = cv2.findChessboardCorners(gray, (9,6), None)
		# If found, add object points, image points (after refining them)
		if ret == True:
			objpoints.append(objp)   # Certainly, every loop objp is the same, in 3D.
			corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
			imgpoints.append(corners2)
			# Draw and display the corners
			img = cv2.drawChessboardCorners(img, (9,6), corners2, ret)
			found += 1
			cv2.imshow('img', img)
			cv2.waitKey(1000)
			# if you want to save images with detected corners 
			# uncomment following 2 lines and lines 5, 18 and 19
			# image_name = path + '/calibresult' + str(found) + '.png'
			# cv2.imwrite(image_name, img)

	print("Number of images used for calibration: ", found)

	# When everything done, release the capture
	# cap.release()
	cv2.destroyAllWindows()

	# calibration
	ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

	#transform the matrix and distortion coefficients to writable lists
	data = {'camera_matrix': np.asarray(mtx).tolist(),
	        'dist_coeff': np.asarray(dist).tolist()}

	# and save it to a file
	with open("calibration_matrix.yaml", "w") as f:
	    yaml.dump(data, f)


def viewStream():
	# import the calibration data
	camCalDataYaml = open("calibration_matrix.yaml")
	camCalData = yaml.load(camCalDataYaml, Loader=yaml.FullLoader)
	mtx = np.asarray(camCalData['camera_matrix'])
	dist = np.asarray(camCalData['dist_coeff'])
	targetImg = vs.read()
	targetImg = cv2.undistort(targetImg, mtx, dist)
	targetImg = cv2.rotate(targetImg, cv2.ROTATE_180)
	targetImg = targetImg[75:425,130:480]
	targetImg = cv2.cvtColor(targetImg, cv2.COLOR_BGR2GRAY)
	targetImg = cv2.GaussianBlur(targetImg, (7, 7),0)
	targetImg = cv2.Canny(targetImg, 80.0, 40.0, 3, L2gradient=True)
	_ ,targetImg = cv2.threshold(targetImg, 160, 255, cv2.THRESH_BINARY)
	kernel = cv2.getStructuringElement(	cv2.MORPH_RECT, (3,3))
	targetImg = cv2.morphologyEx(targetImg, cv2.MORPH_CLOSE, kernel, iterations=5)
	targetImg = cv2.morphologyEx(targetImg, cv2.MORPH_OPEN, kernel, iterations=1)
	im2, contours, hierarchy = cv2.findContours(targetImg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	for cnt in contours:
		retval = cv2.boundingRect(cnt)
		centerX = retval[0] + retval[2] / 2
		centerY = retval[1] + retval[3] / 2
		cv2.rectangle(targetImg, (retval[0], retval[1]), (retval[0]+retval[2], retval[1]+retval[3]), 100)
		# print(retval) # for testing only remove later
		targetImg[centerX, centerY] = 100
	cv2.imwrite("target.png", targetImg)

	# loop over the frames from the video stream
	while True:
		img = vs.read()
		# unwarp the stream
		img = cv2.undistort(img, mtx, dist)
		img = cv2.rotate(img, cv2.ROTATE_180)
		img = img[75:425,130:480]
		# run the brightSpot function to find the laser point
		# create a grey version of the stream
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		# apply a Gaussian blur to the grey version then find the brightest region
		gray = cv2.GaussianBlur(gray, (5, 5),0)
		(minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(gray)
		cv2.circle(img, maxLoc, 5, (255, 0, 0), 2)
		# display the results in a window called LaserPoint
		# wait 1 millisecond
		cv2.waitKey(1)
		#cv2.imshow("gray", gray2) # for testing
		cv2.imshow("LaserPoint", img)
		cv2.imshow("TargetLayer", targetImg)
		#cv2.imshow("threshold", im2)
		# break the while loop if user presses 'q' key
		if cv2.waitKey(1000) & 0xFF == ord('q'):
			break
	cv2.destroyAllWindows()

while True:
	print("Welcome. To continue enter any key, or enter Q to quit.")
	userResponse = raw_input()
	if userResponse == '':
		selectOptions()
	elif userResponse.lower() == 'q':
		break
	continue

# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()