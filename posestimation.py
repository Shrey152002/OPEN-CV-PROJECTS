import cv2
import mediapipe as mp
import time as time
cap = cv2.VideoCapture('videos/production_id_4994033 (2160p).mp4')
cTime=0
pTime=0
mpDraw = mp.solutions.drawing_utils
mpPose = mp.solutions.pose
pose = mpPose.Pose()

while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = pose.process(imgRGB)
    print(results.pose_landmarks)
    if results.pose_landmarks:
        mpDraw.draw_landmarks(img,results.pose_landmarks,mpPose.POSE_CONNECTIONS)
        for id, lm in enumerate(results.pose_landmarks.landmark):
            h,w,c = img.shape
            print(id,lm.x, lm.y, lm)
            cv2.circle(img, (int(lm.x*w),int (lm.y*h)),10,(255,255,255),cv2.FILLED)
    if not success:
        break


    cTime=time.time()
    fps=1/(cTime-pTime)
    pTime=cTime
    cv2.putText(img, str(int(fps)), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 255), 2, cv2.LINE_AA)
    cv2.imshow('Video', img)
    # Exit the loop if 'q' is pressed
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()