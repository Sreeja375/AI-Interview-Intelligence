import cv2
import speech_recognition as sr
import time

# ---------------- FACE CONFIDENCE (SIMPLIFIED) ----------------
def get_face_confidence(duration=5):
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )

    cap = cv2.VideoCapture(0)
    start = time.time()
    detected_frames = 0
    total_frames = 0

    while time.time() - start < duration:
        ret, frame = cap.read()
        if not ret:
            continue

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        total_frames += 1
        if len(faces) > 0:
            detected_frames += 1

        cv2.imshow("Interview - Face Analysis", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    if total_frames == 0:
        return 0

    return int((detected_frames / total_frames) * 100)


# ---------------- SPEECH CLARITY ----------------
def get_speech_clarity():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    fillers = ["uh", "um", "like", "you know", "actually", "basically"]

    print("\n🎙️ Speak for 10 seconds...")

    with mic as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source, phrase_time_limit=10)

    try:
        text = recognizer.recognize_google(audio)
        print("\n📝 Speech Text:")
        print(text)

        text = text.lower()
        filler_count = sum(text.count(f) for f in fillers)

        clarity = max(0, 100 - filler_count * 10)
        return clarity

    except:
        print("Speech not clear")
        return 40


# ---------------- FINAL SCORE ----------------
def final_interview_score(face_conf, speech_clarity):
    final_score = int((face_conf + speech_clarity) / 2)

    if final_score >= 80:
        verdict = "Excellent Interview Performance"
    elif final_score >= 60:
        verdict = "Good Performance, Minor Improvements Needed"
    else:
        verdict = "Needs Improvement"

    return final_score, verdict


# ---------------- MAIN FLOW ----------------
if __name__ == "__main__":
    print("\n🎯 AI INTERVIEW INTELLIGENCE SYSTEM\n")

    print("Step 1: Face Confidence Analysis")
    face_confidence = get_face_confidence()

    print(f"\nFace Confidence Score: {face_confidence}%")

    print("\nStep 2: Speech Analysis")
    speech_clarity = get_speech_clarity()

    print(f"\nSpeech Clarity Score: {speech_clarity}%")

    final_score, feedback = final_interview_score(face_confidence, speech_clarity)

    print("\n🏆 FINAL INTERVIEW RESULT")
    print(f"Final Score : {final_score}%")
    print(f"Feedback    : {feedback}")
