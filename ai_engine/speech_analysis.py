import speech_recognition as sr

FILLER_WORDS = ["uh", "um", "like", "you know", "actually", "basically"]

recognizer = sr.Recognizer()
recognizer.energy_threshold = 300

mic = sr.Microphone()

print("🎙️ AI Interview Intelligence - Speech Analysis")
print("Please speak clearly for 10–15 seconds...\n")

with mic as source:
    recognizer.adjust_for_ambient_noise(source, duration=1)
    audio = recognizer.listen(source, timeout=5, phrase_time_limit=15)

try:
    text = recognizer.recognize_google(audio)
    print("📝 Transcribed Text:")
    print(text)

    text_lower = text.lower()

    filler_count = sum(text_lower.count(word) for word in FILLER_WORDS)
    total_words = len(text.split())

    clarity_score = max(0, 100 - filler_count * 10)

    if filler_count <= 1:
        confidence = "High"
    elif filler_count <= 3:
        confidence = "Medium"
    else:
        confidence = "Low"

    print("\n📊 Speech Analysis Report")
    print(f"Total Words     : {total_words}")
    print(f"Filler Words    : {filler_count}")
    print(f"Clarity Score   : {clarity_score}%")
    print(f"Confidence Level: {confidence}")

except sr.UnknownValueError:
    print("❌ Speech not clear enough. Try again in a quieter place.")
except sr.RequestError as e:
    print(f"❌ Speech service error: {e}")
