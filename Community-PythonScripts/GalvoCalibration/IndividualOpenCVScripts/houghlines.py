#!/usr/bin/python

# import the necessary packages
import cv2
import numpy as np

img = cv2.imread("images/hires.png")

targetImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#targetImg = cv2.bitwise_not(targetImg)

targetImg = cv2.GaussianBlur(targetImg, (7,7),0)
edges = cv2.Canny(targetImg, 100, 200,apertureSize=3)
cv2.imwrite("images/canny.png", edges)

minLineLength = 80
maxLineGap = 25
lines = cv2.HoughLinesP(edges,1,np.pi/180,100,minLineLength,maxLineGap)

print("Found " + str(len(lines[0])) + " lines.")
for rho,theta in lines[0]:
    a = np.cos(theta)
    b=np.sin(theta)
    x0=a*rho
    y0=b*rho
    x1 = int(x0 + 1000*(-b))
    y1 = int(y0 + 1000*(a))
    x2 = int(x0 - 1000*(-b))
    y2 = int(y0 - 1000*(a))

    cv2.line(img,(x1,y1),(x2,y2),(0,255,0),5)

cv2.imwrite('images/houghlines3.png',img)
