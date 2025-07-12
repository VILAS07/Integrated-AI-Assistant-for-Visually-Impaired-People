import cv2
import pyttsx3
import threading
import os
import sys
import time
from pathlib import Path
import easyocr
import torch
import speech_recognition as sr


FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))


engine = pyttsx3.init()
engine.setProperty("rate", 150)
engine.setProperty("volume", 1.0)
speech_lock = threading.Lock()

def speak(text):
    """Synchronous text-to-speech with error handling."""
    global engine
    with speech_lock:
        try:
            print(f"Speaking: '{text}'")  
            engine.say(text)
            engine.runAndWait()
        except RuntimeError:
            print("Speech engine error, reinitializing...")
            engine.stop()
            engine = pyttsx3.init()
            engine.setProperty("rate", 150)
            engine.setProperty("volume", 1.0)
            engine.say(text)
            engine.runAndWait()


print(f"PyTorch version: {torch.__version__}")
if torch.cuda.is_available():
    print(f"GPU available: {torch.cuda.get_device_name(0)}, CUDA version: {torch.version.cuda}")
    try:
        reader = easyocr.Reader(['en'], gpu=True)
        print("EasyOCR initialized with GPU support")
    except Exception as e:
        print(f"GPU initialization failed: {e}")
        reader = easyocr.Reader(['en'], gpu=False)
        print("Falling back to CPU due to GPU error")
else:
    print("No GPU detected; using CPU")
    reader = easyocr.Reader(['en'], gpu=False)
    print("EasyOCR initialized with CPU support")

MIN_CONFIDENCE = 0.7

def capture_and_detect_text():
    """Capture a single frame and detect text."""
    cap = cv2.VideoCapture(1)
    if not cap.isOpened():
        print("Error: Cannot access camera")
        return "Camera error"
    
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
    cap.set(cv2.CAP_PROP_FPS, 30)

    ret, frame = cap.read()
    cap.release()
    
    if not ret:
        return "Camera capture failed"
    
    try:
        results = reader.readtext(frame)
        if not results:
            return "No text detected"
        
        detected_text = [text for (_, text, prob) in results if prob > MIN_CONFIDENCE]
        if detected_text:
            full_text = ' '.join(detected_text)
            return full_text
        return "No text detected"
    except Exception as e:
        print(f"OCR error: {e}")
        return f"Error: {str(e)}"

def run_text_recognition():
    """Run text recognition in listening mode with debugging."""
    speak("Text recognition started.")
    print("Text recognition started.")
    last_voice_check = 0
    VOICE_CHECK_INTERVAL = 1.0

    try:
        with sr.Microphone() as source:
            print("Microphone initialized successfully")
    except Exception as e:
        print(f"Microphone initialization failed: {e}")
        return

    while True:
        current_time = time.time()
        if current_time - last_voice_check >= VOICE_CHECK_INTERVAL:
            last_voice_check = current_time
            print("Listening...", end="\r")
            try:
                with sr.Microphone() as source:
                    recognizer = sr.Recognizer()
                    audio = recognizer.listen(source, timeout=2.0, phrase_time_limit=3.0)
                    command = recognizer.recognize_google(audio).lower()
                    print(f"Heard: '{command}'") 
                    if "read the text" in command:
                        text = capture_and_detect_text()
                        speak(text)  
                        print(f"Detected text: {text}")
                    elif "stop" in command:
                        print("Stop command recognized, exiting text.py...")
                        speak("Stopping text recognition.")
                        print("Exiting now.")
                        os._exit(0) 
            except sr.WaitTimeoutError:
                print("No audio detected within timeout")
                print(" " * 20, end="\r")
            except sr.UnknownValueError:
                print("Could not understand audio")
                print(" " * 20, end="\r")
            except sr.RequestError as e:
                print(f"Speech recognition error: {e}")
                print(" " * 20, end="\r")
            except Exception as e:
                print(f"Unexpected error: {e}")
                print(" " * 20, end="\r")

        time.sleep(0.01) 

if __name__ == "__main__":
    run_text_recognition()