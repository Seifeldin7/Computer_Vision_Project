import cv2
import numpy as np
import math

count = 1


arrOfY =[294, 378, 496, 976, 1018, 1058, 1098, 1136, 1258, 1298, 1338, 1378, 1418, 1456, 1574, 1614, 1656, 1778, 1816, 1896, 2014, 2056]
fault=5

def getQuestionResult(x):
    if  x >= 1116 and x <= 1132:
        return 1
    elif  x >= 1516 and x < 1532:
        return 5
    elif  x >= 1416 and x <= 1432:
        return 4
    elif  x >= 1214 and x <= 1230:
        return 2
    else:
        return 3
def getProgram(x,y):
    if y < 470:
        if x >1246:
            return "MANF"
        elif x >1114:
            return "COMM"
        elif x >982:
            return "ERGY"
        elif x >850:
            return "CESS"
        elif x >718:
            return "BLDG"
        elif x >586:
            return "ENVIR"
        else:
            return "MCTA"
    else:
        if x >850:
            return "HAUD"
        elif x >718:
            return "CISE"
        elif x >586:
            return "MATL"
        else:
            return "LAAR"
def calculateResult(x,y):
    if count == 1:
        if x > 1388 and x < 1392:
            res = "Female"
        else:
            res = "Male"
        f.write("Gender: "+ res + "\n")
    elif count == 2:
        if x > 1000:
            sem = "Summer"
        elif x > 800:
            sem = "Spring"
        else:
            sem = "Fall"
        f.write("Semester: " + sem + "\n")

    elif count == 3:
        f.write("Program: "+getProgram(x,y)+"\n")
    else:
        res = getQuestionResult(x)
        f.write("Q"+str(count-3)+") "+ str(res) + "\n")
def rotateImg(img_before):
    rotated=img_before
    (h, w) = img_before.shape[:2
             ]
    # calculate the center of the image
    (cX,cY) = (w / 2, h / 2)
    img_gray = cv2.cvtColor(img_before, cv2.COLOR_BGR2GRAY)
    img_edges = cv2.Canny(img_gray, 100, 100, apertureSize=3)
    lines = cv2.HoughLinesP(img_edges, 1, math.pi / 180.0, 100, minLineLength=100, maxLineGap=5)

    angles = []

    for x1, y1, x2, y2 in lines[0]:
        angle = math.degrees(math.atan2(y2 - y1, x2 - x1))
        angles.append(angle)

    median_angle = np.median(angles)
    if(median_angle!=0):
        M = cv2.getRotationMatrix2D((cX, cY), median_angle, 1.0)
        cos = np.abs(M[0, 0])
        sin = np.abs(M[0, 1])

        # compute the new bounding dimensions of the image
        nW = int((h * sin) + (w * cos))
        nH = int((h * cos) + (w * sin))

        rotated = cv2.warpAffine(img_before, M, (nW, nH))

    return rotated

def setCount(y):
    for i in range(len(arrOfY)):
        if y < (arrOfY[i]+fault):
            return i+1

fileName = input("Enter output file name :\n")
while True:
    f = open(fileName, "a")
    try:
        imgPath = input("Enter image path type stop to terminate:\n")
    except:
        print("Image not found\n")
    if imgPath == "stop":
        break
	#get the image
    image1 = cv2.imread(imgPath)
	#rotate the image to be vertical
    image1=rotateImg(image1)
	#grayscale
    image = cv2.cvtColor(image1,cv2.COLOR_BGR2GRAY)
    cv2.resize(image1, (600, 400))
	#inverting the image for opening
    image = 255 - image

	#get white only
    ret,image = cv2.threshold(image,250,255,cv2.THRESH_BINARY)
	#circle structuring elemet
    circle_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
	#hit and miss to get the circles
    output_image = cv2.morphologyEx(image, cv2.MORPH_HITMISS, circle_kernel)
	#opening to enlarge them again
    output_image = cv2.morphologyEx(image,cv2.MORPH_OPEN,circle_kernel)
	#get circle edges edges
    edges =cv2.Canny(output_image,150,255,5)

	#get circles using hough circle
    circles = cv2.HoughCircles(edges,cv2.HOUGH_GRADIENT,1,20,
                                param1=255,param2=20,minRadius=0,maxRadius=0)

    circles = np.uint16(np.around(circles))
	#sort the circles by y coordinate
    new_circles = sorted(circles[0],key=lambda x: x[1])

    count=1
	#for each circle check its coordinate and print the result
    for i in new_circles:
        if i[2] > 13 or i[2] < 9:
            continue
        # draw the outer circle
        cv2.circle(image,(i[0],i[1]),i[2],(0,255,0),2)
        # draw the center of the circle
        cv2.circle(image,(i[0],i[1]),2,(0,0,255),3)
        count=setCount(i[1])
        calculateResult(i[0],i[1])
    f.close()


