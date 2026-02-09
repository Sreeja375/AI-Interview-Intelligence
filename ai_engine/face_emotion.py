import cv2
import math

# Load Haar cascades
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)
eye_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_eye.xml"
)
mouth_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_smile.xml"
)

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Camera not accessible")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.3,
        minNeighbors=5
    )

    for (x, y, w, h) in faces:
        # Draw face box
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        roi_gray = gray[y:y + h, x:x + w]
        roi_color = frame[y:y + h, x:x + w]

        eyes = eye_cascade.detectMultiScale(roi_gray, 1.1, 5)
        mouths = mouth_cascade.detectMultiScale(roi_gray, 1.7, 20)

        eye_count = len(eyes)
        mouth_open = len(mouths) > 0

        # Emotion logic
        if mouth_open and eye_count >= 2:
            emotion = "Confident / Speaking"
        elif eye_count < 2:
            emotion = "Low Energy / Nervous"
        else:
            emotion = "Neutral"

        # Confidence score (simple heuristic)
        confidence = min(100, eye_count * 30 + (40 if mouth_open else 10))

        # Display text
        cv2.putText(frame, f"Emotion: {emotion}",
                    (x, y - 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                    (0, 255, 0), 2)

        cv2.putText(frame, f"Confidence: {confidence}%",
                    (x, y - 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                    (255, 0, 0), 2)

        # Draw eyes
        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(roi_color,
                          (ex, ey),
                          (ex + ew, ey + eh),
                          (255, 255, 0), 2)

        # Draw mouth
        for (mx, my, mw, mh) in mouths:
            cv2.rectangle(roi_color,
                          (mx, my),
                          (mx + mw, my + mh),
                          (0, 0, 255), 2)

    cv2.imshow("AI Interview Intelligence (OpenCV)", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
