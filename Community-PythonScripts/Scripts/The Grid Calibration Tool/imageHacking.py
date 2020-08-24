#!/usr/bin/python
# import the necessary packages
import cv2

targetImg = cv2.imread("images/01_warped.png")
#targetImg = cv2.imread("images/lit.png")
#Grayscale
targetImg = cv2.cvtColor(targetImg, cv2.COLOR_BGR2GRAY)
cv2.imwrite("images/gray.png", targetImg)

inverseImg = cv2.bitwise_not(targetImg)

for threshVal in range(150, 160, 10):
    _ ,truncInvImg = cv2.threshold(inverseImg, threshVal, 255, cv2.THRESH_TRUNC)
    fname = "images/truncated_inv_" + str(threshVal) + ".png"
    cv2.imwrite(fname, truncInvImg)

#for threshVal in range(180, 200, 10):
#    _ ,truncInvImg = cv2.threshold(inverseImg, threshVal, 255, cv2.THRESH_TRUNC)
#    fname = "images/truncated_inv_" + str(threshVal) + ".png"
#    cv2.imwrite(fname, truncInvImg)

#_, targetImg = cv2.threshold(inverseImg, 100, 255, cv2.THRESH_TOZERO_INV)
#cv2.imwrite("images/trunc.png", targetImg)

# Stretch the histogram
#stretchedImg = cv2.equalizeHist(targetImg)
#cv2.imwrite("images/stretched.png", stretchedImg)

# Clahe tile-based histogram stretching:
#clahe = cv2.createCLAHE(clipLimit=1.0, tileGridSize=(16,16))
#targetImg = clahe.apply(targetImg)
#cv2.imwrite("images/claheImg.png", targetImg)

#_ ,maskImg = cv2.threshold(targetImg, 100, 255, cv2.THRESH_BINARY)
#cv2.imwrite("images/maskImg.png", maskImg)

#invMaskImg = cv2.bitwise_not(maskImg)
#cv2.imwrite("images/invMaskImg.png", maskImg)

#maskedImg = cv2.bitwise_or(targetImg, maskImg)
#cv2.imwrite("images/maskedImg.png", maskedImg)

#invMaskedImg = cv2.bitwise_or(targetImg, invMaskImg)
#cv2.imwrite("images/invMaskedImg.png", invMaskedImg)


# Extract the background gradient with a large-matrix Gaussian blur
gradientImg = cv2.GaussianBlur(truncInvImg, (201,201),0)
#gradientImg = cv2.bitwise_not(cv2.GaussianBlur(targetImg, (201,201),0))
#gradientImg = cv2.GaussianBlur(invMaskedImg, (201,201),0)
cv2.imwrite("images/gradientImg.png", gradientImg)

alpha = 0.5
blendedImg = cv2.addWeighted(targetImg, alpha, gradientImg, (1.0 - alpha), 0.0)
cv2.imwrite("images/blendedImg.png", blendedImg)

# Clahe tile-based histogram stretching:
#clahe = cv2.createCLAHE(clipLimit=4.0, tileGridSize=(16,16))
#claheImg = clahe.apply(blendedImg)
#cv2.imwrite("images/claheImg.png", targetImg)

#gammaImg = cv2.addWeighted(blendedImg, alpha, blendedImg, (1.0-alpha), 60.0)
#cv2.imwrite("images/gammaImg.png", gammaImg)

# Stretch the histogram#
#stretchedImg = cv2.equalizeHist(blendedImg)
#cv2.imwrite("images/stretched.png", stretchedImg)

#alpha = 0.8
#blendedImg = cv2.addWeighted(blendedImg, alpha, stretchedImg, (1.0 - alpha), 0.0)
#cv2.imwrite("images/stretchedBlended.png", blendedImg)


# Alpha blend the stretched image with the gradientImg
#targetImg = cv2.multiply(alpha, stretchedImg)
#cv2.imwrite("images/alphaBlended.png", targetImg)

#Subtract the gradient from the stretched image
#cv2.subtract(targetImg, gradientImg, targetImg, invMaskImg)
#cv2.imwrite("images/gradientSubtracted.png", targetImg)

# targetImg = cv2.Canny(targetImg, 80.0, 40.0, 3, L2gradient=True)
# cv2.imwrite("05_canny.png", targetImg)

#cv2.adaptiveThreshold(targetImg,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
#            cv2.THRESH_BINARY,11,2)
#cv2.imwrite("images/adaptiveThresh255.png", bar)

#for threshVal in range(110,190, 5):
_ ,outImg = cv2.threshold(blendedImg, threshVal, 255, cv2.THRESH_BINARY)
_ ,outImg = cv2.threshold(blendedImg, 130, 255, cv2.THRESH_BINARY)
fname = str(threshVal)
#imgStack=stackImages(0.5, (grayImg, blendedImg, outImg))
while True:
    cv2.imshow(fname, outImg)
    if cv2.waitKey(1) & 0XFF == ord('q'):
        break

targetImg = cv2.GaussianBlur(outImg, (7,7),0)
canny = cv2.Canny(targetImg, 100, 200)

while True:
    cv2.imshow("Canny", canny)
    if cv2.waitKey(1) & 0XFF == ord('q'):
        break

edgePixels = []
for x in range(0, canny.shape[0]):
    for y in range(0, canny.shape[1]):
        if canny[x,y] != 0:
            edgePixels.append([x,y])

print ("I found " + str(len(edgePixels)) + " edge pixels")



#contours, _ = cv2.findContours(outImg, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

#for contour in contours:
#    approx = cv2.approxPolyDP(contour, 0.01*cv2.arcLength(contour, True), True)
#    cv2.drawContours(outImg, [approx], 0, (50,255,100), 5)
#    x = approx.ravel()[0]
#    y = approx.ravel()[1]
#    if len(appprox) == 3:
#        cv2.putText(outImg, "Triangle", (x,y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0,0.0))
#    elif len(approx) == 4:
#        cv2.putText(outImg, "Rectangle", (x,y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0,0.0))
#    elif len(approx) == 5:
#        cv2.putText(outImg, "Pentagon", (x,y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0,0.0))
#    elif len(approx) == 10:
#        cv2.putText(outImg, "Star", (x,y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0,0.0))
#    else:
#        cv2.putText(outImg, "Circle", (x,y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0,0.0))


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
