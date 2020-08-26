import time
 
import cv2
import numpy as np
from imutils.video import VideoStream
import imutils
import matplotlib.pyplot as plt
import time
 
# Are we using the Pi Camera?
usingPiCamera = True
# Set initial frame size.
frameSize = (2464, 2464)
 
# Initialize mutithreading the video stream.
vs = VideoStream(src=0, usePiCamera=usingPiCamera, resolution=frameSize,
		framerate=15).start()
# Allow the camera to warm up.
time.sleep(2.0)


autoCrop = vs.read()
gray = cv2.cvtColor(autoCrop, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (11,11),0)
th, gray = cv2.threshold(gray, 25, 255, cv2.THRESH_BINARY)
cnts = cv2.findContours(gray, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[-2]
s1 = 200
s2 = 5000
xcnts = [] 
for cnt in cnts: 
	if s1<cv2.contourArea(cnt) <s2: 
		xcnts.append(cnt)
cornerMarkers = []
for spot in xcnts:
	M = cv2.moments(spot)
	cornerX = int(M["m10"] / M["m00"])
	cornerY = int(M["m01"] / M["m00"])
	cornerMarkers.append([cornerX, cornerY])
corn = np.asarray(cornerMarkers)

pts1 = np.float32([[corn[3][0],corn[3][1]],[corn[2][0],corn[2][1]],[corn[1][0],corn[1][1]],[corn[0][0],corn[0][1]]])
pts2 = np.float32([[0,0],[1690,0],[0,1690],[1690,1690]])
M = cv2.getPerspectiveTransform(pts1,pts2)
dst = cv2.warpPerspective(autoCrop,M,(1690,1690))
cv2.imwrite("frame_after.png", dst)
cv2.imwrite("frame_before.png", autoCrop)

cv2.waitKey(0) & 0xFF == ord('q')
 
# Cleanup before exit.
cv2.destroyAllWindows()
vs.stop()