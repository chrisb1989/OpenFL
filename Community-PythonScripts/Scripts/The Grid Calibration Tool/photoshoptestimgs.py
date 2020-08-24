#!/usr/bin/python
# import the necessary packages
import cv2

stretchedImg = cv2.imread("images/PhotoshopStretch.png")
gradientImg = cv2.imread("images/PhotoshopBlur.png")

stretchedImg = cv2.cvtColor(stretchedImg, cv2.COLOR_BGR2GRAY)
gradientImg = cv2.cvtColor(gradientImg, cv2.COLOR_BGR2GRAY)

alpha = 0.5
blendedImg = cv2.addWeighted(stretchedImg, alpha, gradientImg, (1.0 - alpha), 0.0)
cv2.imwrite("images/blendedImg.png", blendedImg)

# Alpha blend the stretched image with the gradientImg
#targetImg = cv2.multiply(alpha, stretchedImg)
#cv2.imwrite("images/alphaBlended.png", targetImg)

#Subtract the gradient from the stretched image
#cv2.subtract(targetImg, gradientImg, targetImg, invMaskImg)
#cv2.imwrite("images/gradientSubtracted.png", targetImg)

# targetImg = cv2.Canny(targetImg, 80.0, 40.0, 3, L2gradient=True)
# cv2.imwrite("05_canny.png", targetImg)



#cv2.adaptiveThreshold(targetImg,1,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
            #cv2.THRESH_BINARY,11,2)
#cv2.imwrite("images/adaptiveThresh.png", targetImg)

#for threshVal in range(10, 250, 10):
    #_ ,outImg = cv2.threshold(targetImg, threshVal, 255, cv2.THRESH_BINARY_INV)
    #fname = "images/gradientAlpha_threshold_" + str(threshVal) + ".png"
    #cv2.imwrite(fname, outImg)

# kernel = cv2.getStructuringElement(   cv2.MORPH_RECT, (3,3))
# targetImg = cv2.morphologyEx(targetImg, cv2.MORPH_CLOSE, kernel, iterations=5)
# targetImg = cv2.morphologyEx(targetImg, cv2.MORPH_OPEN, kernel, iterations=1)
# im2, contours, hierarchy = cv2.findContours(targetImg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# for cnt in contours:
#   retval = cv2.boundingRect(cnt)
#   centerX = retval[0] + retval[2] / 2
#   centerY = retval[1] + retval[3] / 2
#   cv2.rectangle(im2, (retval[0], retval[1]), (retval[0]+retval[2], retval[1]+retval[3]), 100)
#   # print(retval) # for testing only remove later
#   targetImg[centerX, centerY] = 100
# cv2.imwrite("08_contours.png", im2)# import the necessary packages
import cv2


targetImg = cv2.imread("images/01_warped.png")
targetImg = cv2.rotate(targetImg, cv2.ROTATE_180)
targetImg = targetImg[75:425,130:480]
# cv2.imwrite("01_warped.png", targetImg)
targetImg = cv2.cvtColor(targetImg, cv2.COLOR_BGR2GRAY)
# cv2.imwrite("03_grayscale.png", targetImg)
# targetImg = cv2.GaussianBlur(targetImg, (7, 7),0)
# cv2.imwrite("04_blurred.png", targetImg)
# targetImg = cv2.Canny(targetImg, 80.0, 40.0, 3, L2gradient=True)
# cv2.imwrite("05_canny.png", targetImg)
targetImg = cv2.equalizeHist(targetImg, targetImg)
#cv2.imwrite("06_equalizeHist.png", targetImg)
_ ,targetImg = cv2.threshold(targetImg, 200, 255, cv2.THRESH_BINARY)
cv2.imwrite("07_threshold.png", targetImg)
# kernel = cv2.getStructuringElement(   cv2.MORPH_RECT, (3,3))
# targetImg = cv2.morphologyEx(targetImg, cv2.MORPH_CLOSE, kernel, iterations=5)
# targetImg = cv2.morphologyEx(targetImg, cv2.MORPH_OPEN, kernel, iterations=1)
# im2, contours, hierarchy = cv2.findContours(targetImg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# for cnt in contours:
#   retval = cv2.boundingRect(cnt)
#   centerX = retval[0] + retval[2] / 2
#   centerY = retval[1] + retval[3] / 2
#   cv2.rectangle(im2, (retval[0], retval[1]), (retval[0]+retval[2], retval[1]+retval[3]), 100)
#   # print(retval) # for testing only remove later
#   targetImg[centerX, centerY] = 100
# cv2.imwrite("08_contours.png", im2)
