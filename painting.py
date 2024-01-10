import cv2
import os
import numpy as np
import handtracking_module as htm
brushthickness=15
x1=0
x2=0
y1=0
y2=0
xp=0
yp=0
imgCanvas=np.zeros((400,700,3),np.uint8)
folderpath = "header"
myList = os.listdir(folderpath)
print(myList)

overlayList = []
for imPath in myList:
    image = cv2.imread(f'{folderpath}/{imPath}')
    overlayList.append(image)

print(len(overlayList))
header=overlayList[0]
drawColor=(255,0,255)
header_index = 0  # Index to cycle through different header images
if len(overlayList) > 0:
    header = overlayList[header_index]
else:
    print("No header images found")
    exit()

cap = cv2.VideoCapture(0)
cap.set(3, 893)
cap.set(4, 720)
detector=htm.HandDetector(detection_con=0.085)
while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    img=detector.find_hands(img)
    lmList=detector.find_position(img,draw=False)
    if len(lmList)!=0:
        #print(lmList)

         x1,y1=lmList[8][1:]
         x2,y2=lmList[12][1:]
         fingers=detector.fingersUp()
         #print(fingers)

         if fingers[1] and fingers[2]:

             #print("selection mode")
             if y1<100:
                 if 207<x1<250:
                     header=overlayList[0]
                     drawColor=(255,0,0)
                 elif 300<x1<400:
                     header=overlayList[1]
                     drawColor=(0,255,0)
                 elif 450<x1<500:
                     header=overlayList[2]
                     drawColor=(0,0,255)
                 elif 550<x1<600:
                     header=overlayList[3]
                     drawColor=(0,0,0)
                 cv2.rectangle(img, (x1, y1 - 25), (x2, y2 + 25),drawColor, cv2.FILLED)
         if fingers[1] and fingers[2]==False:
             cv2.circle(img,(x1,y1),15,drawColor,cv2.FILLED)
             print("drawing mode")
             if xp==0 and yp==0:
                 xp,yp=x1,y1
             cv2.line(img,(xp,yp),(x1,y1),drawColor,brushthickness)
             cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, brushthickness)
             xp,yp=x1,y1

    # Overlay the header image
    if header is not None:
        # Resize header image to match the width of the video frame
        header_resized = cv2.resize(header, (img.shape[1], 100))  # Resize height to 100 (or adjust as needed)
        img[0:100, 0:img.shape[1]] = header_resized  # Overlay the resized header image

    if not success:
        print("Failed to capture frame from camera")
        break

    cv2.imshow('img', img)
    cv2.imshow('imgCanvas', imgCanvas)
    if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to exit
        break

# Release the capture and close the window
cap.release()
cv2.destroyAllWindows()
