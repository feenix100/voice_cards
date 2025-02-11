import speech_recognition as sr

# this app will convert your voice into text

recognizer = sr.Recognizer()

with sr.Microphone() as source:
    print("Say something...")
    recognizer.adjust_for_ambient_noise(source)  # Adjust for background noise
    audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        print(f"You said: {text}")
    except sr.UnknownValueError:
        print("⚠️ Could not understand audio")
    except sr.RequestError:
        print("⚠️ Could not request results from Google Speech Recognition")
