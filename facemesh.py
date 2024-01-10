import cv2
import time
import mediapipe as mp

# Open the video file
cap = cv2.VideoCapture('videos/baseball_training (720p).mp4')

# Initialize variables for frame processing
pTime = 0
mpDraw = mp.solutions.drawing_utils
mpFaceMesh = mp.solutions.face_mesh
faceMesh = mpFaceMesh.FaceMesh(max_num_faces=2)

# Check if the video file opened successfully
if not cap.isOpened():
    print("Error opening video file")
    exit()

while True:
    # Read a frame from the video
    success, img = cap.read()

    # Break the loop if the video ends
    if not success:
        print("Video ended")
        break

    # Convert the frame to RGB format for compatibility with MediaPipe
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Process the frame to detect face landmarks
    results = faceMesh.process(imgRGB)

    # Draw landmarks if faces are detected
    if results.multi_face_landmarks:
        for faceLms in results.multi_face_landmarks:
            # Draw face landmarks with customized connections
            mpDraw.draw_landmarks(img, faceLms, mpFaceMesh.FACEMESH_TESSELATION,
                                  landmark_drawing_spec=None, connection_drawing_spec=mpDraw.DrawingSpec(color=(0, 255, 0), thickness=1, circle_radius=1))

    # Calculate FPS and display it on the frame
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    # Display the frame in a window
    cv2.imshow("Image", img)

    # Check for user input to exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture and close the window
cap.release()
cv2.destroyAllWindows()
