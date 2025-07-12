import cv2
import numpy as np
import os
import pyttsx3
import speech_recognition as sr

engine = pyttsx3.init()
def speak(text):
    engine.say(text)
    engine.runAndWait()

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()

dataset_path = 'dataset/'
model_path = 'trainer.yml'

if os.path.exists(model_path):
    recognizer.read(model_path)
    labels = {}
    for folder in os.listdir(dataset_path):
        try:
            user_id, user_name = folder.split('.')
            labels[int(user_id)] = user_name
        except ValueError:
            continue
else:
    labels = {}

def train_model():
    faces, ids = [], []
    for folder in os.listdir(dataset_path):
        try:
            user_id, _ = folder.split('.')
            user_id = int(user_id)
        except ValueError:
            continue
        for img in os.listdir(os.path.join(dataset_path, folder)):
            img_path = os.path.join(dataset_path, folder, img)
            face_img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
            if face_img is None:
                continue
            face_img = cv2.resize(face_img, (200, 200))
            faces.append(face_img)
            ids.append(user_id)
    if faces:
        recognizer.train(faces, np.array(ids))
        recognizer.save(model_path)
        print("Model trained successfully.")

if not os.path.exists(model_path) or not labels:
    print("Training model as no trained data found.")
    train_model()

def capture_images(user_name):
    cap = cv2.VideoCapture(1)
    count = 0
    user_id = max(labels.keys(), default=0) + 1
    user_folder = os.path.join(dataset_path, f"{user_id}.{user_name}")
    os.makedirs(user_folder, exist_ok=True)
    while count < 150:
        ret, frame = cap.read()
        if not ret:
            continue
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            count += 1
            face_img = gray[y:y + h, x:x + w]
            face_img = cv2.resize(face_img, (200, 200))
            cv2.imwrite(f'{user_folder}/{count}.jpg', face_img)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        cv2.imshow('Capturing Faces', frame)
        if cv2.waitKey(100) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
    labels[user_id] = user_name
    train_model()
    speak(f"{user_name}'s face saved.")

def recognize_face():
    cap = cv2.VideoCapture(1)
    spoken_names = set()
    while True:
        ret, frame = cap.read()
        if not ret:
            continue
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        if len(faces) > 0:
            for (x, y, w, h) in faces:
                face_img = gray[y:y + h, x:x + w]
                face_img = cv2.resize(face_img, (200, 200))
                try:
                    id_, conf = recognizer.predict(face_img)
                    if conf < 50:
                        name = labels.get(id_, "Unknown Person")
                    else:
                        name = "Unknown"
                except:
                    name = "Unknown"
                if name not in spoken_names:
                    speak(f"its {name}!")
                    spoken_names.add(name)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                cv2.putText(frame, name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        else:
            break
        cv2.imshow('Face Recognition', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

def listen_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening...")
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
    if "recognise" in command:
        recognize_face()
    elif "save the face" in command:
        speak("Please say the name clearly.")
        name = listen_command()
        while not name:
            speak("I couldn't understand. Please say the name again.")
            name = listen_command()
        capture_images(name)
    elif "stop" in command:
        speak("Stopping the program.")
        break
    elif "back" in command:
        continue
