import cv2
import numpy as np
import pyttsx3
import speech_recognition as sr
import torch
from ultralytics import YOLO

engine = pyttsx3.init()
def speak(text):
    engine.say(text)
    engine.runAndWait()

model = YOLO("yolov8m.pt").to('cuda' if torch.cuda.is_available() else 'cpu')

def estimate_distance(width):
    focal_length = 500
    real_width = 30
    distance = round((real_width * focal_length) / width / 100, 2)
    return distance

def detect_object():
    cap = cv2.VideoCapture(1)
    ret, frame = cap.read()
    if not ret:
        cap.release()
        return

    results = model(frame)
    detected_objects = []

    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
            w = x2 - x1
            distance = estimate_distance(w)
            label = model.names[int(box.cls[0].item())]
            if box.conf[0] > 0.5:
                detected_objects.append((label, distance, box.conf[0]))

    detected_objects.sort(key=lambda x: (x[0] == "person", -x[2]))

    if detected_objects:
        label, distance, _ = detected_objects[0]
        speak(f"It's a {label} at {distance:.2f} meters!")
        print(f"Detected: {label} at {distance:.2f} meters")
    else:
        speak("No clear object detected.")

    cap.release()
    cv2.destroyAllWindows()

def listen_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        speak("Listening")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source)
            command = recognizer.recognize_google(audio).lower()
            print(f"Heard: {command}")
            return command
        except sr.UnknownValueError:
            print("Could not understand the command.")
            return ""

speak("How may I help you?")
while True:
    command = listen_command()
    if "what is this" in command:
        detect_object()
    elif "stop" in command:
        speak("Stopping the program.")
        break
