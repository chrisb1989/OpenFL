# import the necessary packages
from imutils.video import VideoStream
import datetime
import argparse
import imutils
import time
import cv2
import numpy as np

# Are we using the Pi Camera?
usingPiCamera = True
# Set initial frame size.
frameSize = (1808, 1808)
 
# Initialize mutithreading the video stream.
vs = VideoStream(src=0, usePiCamera=usingPiCamera, resolution=frameSize,
		framerate=32).start()
# Allow the camera to warm up.
time.sleep(2.0)

# Auto Crop Parameters - Run at program start:

autoCrop = vs.read()
gray = cv2.cvtColor(autoCrop, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (11,11),0)
th, gray = cv2.threshold(gray, 30,255, cv2.THRESH_BINARY)
cnts = cv2.findContours(gray, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[-2]
s1 = 900
s2 = 4500
xcnts = [] 
for cnt in cnts: 
	if s1<cv2.contourArea(cnt) <s2: 
		xcnts.append(cnt)
cornerMarkers = []
for spot in xcnts:
	Mo = cv2.moments(spot)
	cornerX = int(Mo["m10"] / Mo["m00"])
	cornerY = int(Mo["m01"] / Mo["m00"])
	cornerMarkers.append([cornerX, cornerY])
corn = np.asarray(cornerMarkers)
print(corn)
pts1 = np.float32([[corn[3][0],corn[3][1]],[corn[2][0],corn[2][1]],[corn[1][0],corn[1][1]],[corn[0][0],corn[0][1]]])
pts2 = np.float32([[0,0],[1690,0],[0,1690],[1690,1690]])
Mom = cv2.getPerspectiveTransform(pts1,pts2)

img = vs.read()
img = cv2.warpPerspective(img,Mom,(1690,1690))
img = cv2.rotate(img, cv2.ROTATE_180)
#Grayscale
targetImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
inverseImg = cv2.bitwise_not(targetImg)
for threshVal in range(150, 160, 10):
	_ ,truncInvImg = cv2.threshold(inverseImg, threshVal, 255, cv2.THRESH_TRUNC)
gradientImg = cv2.GaussianBlur(truncInvImg, (201,201),0)
time.sleep(0.1)
alpha = 0.5
blendedImg = cv2.addWeighted(targetImg, alpha, gradientImg, (1.0 - alpha), 0.0)
time.sleep(0.1)
_ ,outImg = cv2.threshold(blendedImg, 140, 255, cv2.THRESH_BINARY)
time.sleep(0.1)
im2, contoursMid, hierarchy = cv2.findContours(outImg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
time.sleep(0.1)
pointsInImg = []
for c in contoursMid:
	# calculate moments for each contour
	M = cv2.moments(c)
	# calculate x,y coordinate of center
	cX = int(M["m10"] / M["m00"])
	cY = int(M["m01"] / M["m00"])
	pointsInImg.append([cX,cY])
#	cv2.circle(img, (cX, cY), 25, (0, 0, 255), 2)
	#cv2.rectangle(img,(cX+15,cY-15),(cX-15,cY+15),(0,255,0),3)
	#cv2.imwrite("centerpoints.png", img)
time.sleep(0.1)
gridImg = cv2.resize(outImg,None,fx=0.25, fy=0.25, interpolation = cv2.INTER_CUBIC)
time.sleep(0.1)
# cv2.imshow("final", gridImg) # For testing
#for point in pointsInImg:
	#print(type(point[0]), type(point[1]))
	
# loop over the frames from the video stream
while True:
	liveImg = vs.read()
	liveImg = cv2.warpPerspective(liveImg,Mom,(1690,1690))		
	liveImg = cv2.rotate(liveImg, cv2.ROTATE_180)
	# run the brightSpot function to find the laser point
	# create a grey version of the stream
	gray2 = cv2.cvtColor(liveImg, cv2.COLOR_BGR2GRAY)
	# apply a Gaussian blur to the grey version then find the brightest region
	gray2 = cv2.GaussianBlur(gray2, (7, 7),0)
	(minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(gray2)
	time.sleep(0.1)
	cv2.circle(liveImg, maxLoc, 25, (0, 0, 255), 2)
	for point in pointsInImg:
		cv2.circle(liveImg, (point[0], point[1]), 25, (0, 255, 0), 2)
	cv2.waitKey(1)
	#cv2.imshow("gray2", gray) # for testing
	time.sleep(0.1)
	cv2.imwrite("LaserPoint.png", liveImg)
	liveImg = cv2.resize(liveImg,None,fx=0.25, fy=0.25, interpolation = cv2.INTER_CUBIC)
	time.sleep(0.1)
	cv2.imshow("LaserPoint", liveImg)
	# break the while loop if user presses 'q' key
	if cv2.waitKey(1000) & 0xFF == ord('q'):
		break

cv2.destroyAllWindows()
vs.stop()
