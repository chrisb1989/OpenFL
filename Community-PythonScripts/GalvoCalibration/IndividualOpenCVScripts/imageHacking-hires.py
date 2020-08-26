#!/usr/bin/python
# import the necessary packages
import cv2
import numpy as np

origImg = cv2.imread("images/newtarget.png")
targetImg = origImg.copy()
#targetImg = cv2.imread("images/circles.png")
#targetImg = cv2.imread("images/lit.png")

# Downsample for speed
#targetImg = cv2.GaussianBlur(origImg, (7,7),0)
sizeX = targetImg.shape[0]
sizeY = targetImg.shape[1]
#targetImg = cv2.resize(targetImg, (int(sizeX), int(sizeY)))
#origImg = cv2.resize(targetImg, (int(sizeX), int(sizeY)))

#Grayscale
targetImg = cv2.cvtColor(targetImg, cv2.COLOR_BGR2GRAY)
cv2.imwrite("images/gray.png", targetImg)

# Invert the image to then THRESH_TRUNC off some of the crosshairs
# This helps with computing the image gradient, also pre-inverting
# it for the alpha blend
inverseImg = cv2.bitwise_not(targetImg)

# A loop to try some different thresholds.
# Ended up landing on 145-150 - leave the commented loop in case it's needed later
threshVal=142
#for threshVal in range(110, 132, 2):
_ ,truncInvImg = cv2.threshold(inverseImg, threshVal, 255, cv2.THRESH_TRUNC)
fname = "images/truncated_inv_" + str(threshVal) + ".png"
cv2.imwrite(fname, truncInvImg)

# Extract the background gradient with a large-kernel Gaussian blur
gradientImg = cv2.GaussianBlur(truncInvImg, (401,401),0)
cv2.imwrite("images/gradientImg.png", gradientImg)

# Now alpha-blend the inverted background gradient with the image
alpha = 0.5
blendedImg = cv2.addWeighted(targetImg, alpha, gradientImg, (1.0 - alpha), 0.0)
cv2.imwrite("images/blendedImg.png", blendedImg)

# Clahe tile-based histogram stretching:
#clahe = cv2.createCLAHE(clipLimit=4.0, tileGridSize=(16,16))
#claheImg = clahe.apply(blendedImg)
#cv2.imwrite("images/claheImg.png", targetImg)

# Chop off everything except the target circles
threshVal=132
#for threshVal in range(128, 150, 2):
#_ ,outImg = cv2.threshold(blendedImg, threshVal, 255, cv2.THRESH_BINARY)
_ ,outImg = cv2.threshold(blendedImg, threshVal, 255, cv2.THRESH_BINARY)
fname = "images/gaussianBlendedThreshold-" + str(threshVal) + ".png"
cv2.imwrite(fname, outImg)

circleImg = outImg
#sizeX = int(circleImg.shape[0]) * 2
#sizeY = int(circleImg.shape[1]) * 2
#circleImg = cv2.resize(circleImg, (sizeX, sizeY))
#origImg = cv2.resize(origImg, (sizeX, sizeY))
circleImg = cv2.GaussianBlur(circleImg, (11,11),0)
cv2.imwrite("images/circleImg.png", circleImg)

# Here is a multi-nested loop for exploring HoughCircles() parameters.
# In fairly extensive testing, the most important parameters appear to be
# minDist and maxSize, at least for this application.
# minDist needs to be set to something larger than the closest two circles
# you want to detect, or else it gives a lot of false positives. maxSize seems
# quite sensitive to the exact size of the circle you are trying to detect.
# In this case, a value of 4 for circles 10 pixels across seems to work pretty
# reliably.

'''
for minDist in range (220,280,5):
    for sigma in np.arange (1.8, 2.6, 0.2):
        for parm1 in range (25,60,10):
            for parm2 in range (50,60,10):
                for minSize in range (2,6,1):
                    for maxSize in range (2,5,1):
                        fname = str(minDist) + "-" + str(parm1) + "-" + str(parm2)
                        fname += "-" + str(minSize) + "-" + str(maxSize) + "-{:3.1f}".format(sigma) + ".png"
                        print "Info: " + fname
                        circles = []
                        circles = cv2.HoughCircles(circleImg, cv2.HOUGH_GRADIENT, sigma,
                            minDist, parm1, parm2, minSize, maxSize)
                        try:
                            circleCnt = (len(circles[0]))
                        except:
                            circleCnt = 0
                        if ((circleCnt >= 25)):
                            thisImg = origImg.copy()
                            smallCircleCount = 0
                            for i in circles[0,:]:
                                thisRad = float(i[2])
                                # draw the outer circle
                                if thisRad < 8.0:
                                    smallCircleCount += 1
                                    cv2.circle(thisImg,(i[0],i[1]),i[2],(0,255,0),3)
                            if( smallCircleCount >=25 ):
                                print  "Found " + str(len(circles[0])) + " small circles in " + fname
                                cv2.imwrite("images/" + fname, thisImg)
                            else:
                                print "Small circles were only " + str(smallCircleCount) + " of " + str(len(circles[0])) + "\n"
                        else:
                            print "Not enough circles!"
exit()
'''

#minDist=120; parm1 = 10; parm2 = 10; minSize = 5; maxSize = 2
minDist=270; parm1 =100; parm2 = 200; minSize = 3; maxSize = 4
circles = cv2.HoughCircles(circleImg, cv2.HOUGH_GRADIENT, 1.8,
    minDist, parm1, parm2, minSize, maxSize)

try:
    print("Found " + str(len(circles[0])) + " circles")
except:
    print("I didn't find any circles")
    exit()

print circles
for i in circles[0,:]:
    # draw the outer circle
    cv2.circle(origImg,(i[0],i[1]),i[2],(0,255,0),3)
    # draw the center of the circle
    cv2.circle(origImg,(i[0],i[1]),2,(0,255,0),2)

origImg = cv2.resize(origImg, (int(sizeX/2), int(sizeY/2)))


cv2.imshow('detected circles',origImg)
cv2.waitKey(0)
