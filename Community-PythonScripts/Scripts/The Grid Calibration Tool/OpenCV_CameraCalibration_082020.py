import numpy as np
import cv2
import glob
import time

# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((6*7,3), np.float32)
objp[:,:2] = np.mgrid[0:7,0:6].T.reshape(-1,2)

# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.

# images = glob.glob('*.jpg')

# for fname in images:
#     img = cv2.imread(fname)
#     gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

# This is the rtsp stream capture
cap = cv2.VideoCapture("rtsp://laser:laser@192.168.86.24/live")
#
while True:
    ret, frame = cap.read()
    # convert from BGR color to grayscale:
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # show the grayscale image feed (for testing)
    #cv2.imshow('gray', gray)
    

    # # Find the chess board corners
    ret, corners = cv2.findChessboardCorners(gray, (9,6),None)

    # # If found, add object points, image points (after refining them)
    if ret == True:
        objpoints.append(objp)

        cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
        imgpoints.append(corners)

        # Draw and display the corners
        cv2.drawChessboardCorners(frame, (9,6), corners,ret)
        cv2.imshow('frame', frame)
        cv2.waitKey(0)


    # break the while loop if user presses 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
    	break
    time.sleep(1)

cap.release()
cv2.destroyAllWindows()

