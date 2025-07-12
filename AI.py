import speech_recognition as sr
import pyttsx3
import subprocess
import sys
import time
import cohere
import json
import os
from dotenv import load_dotenv

load_dotenv()

# Get Cohere API key from environment variable or use placeholder
cohere_api_key = os.getenv('COHERE_API_KEY', 'your_cohere_api_key_here')
co = cohere.Client(cohere_api_key)

recognizer = sr.Recognizer()
tts_engine = pyttsx3.init()
tts_engine.setProperty('rate', 150)
tts_engine.setProperty('volume', 1.0)

FACE_FILE = "face.py"
OBJECT_FILE = "object.py"
TEXT_FILE = "text.py"
EMERGENCY_FILE = "emergency.py"
USER_DATA_FILE = "user_data.json"

def load_user_data():
    try:
        with open(USER_DATA_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"name": "", "questions": [], "preferences": {}}

def save_user_data(data):
    with open(USER_DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def update_user_data(command):
    user_data = load_user_data()
    if "my name is" in command:
        user_data["name"] = command.split("my name is")[-1].strip()
    else:
        user_data["questions"].append(command)
    save_user_data(user_data)

def speak(text):
    tts_engine.say(text)
    tts_engine.runAndWait()

def listen_for_command():
    with sr.Microphone() as source:
        print("Listening...", end="\r")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        try:
            audio = recognizer.listen(source, timeout=None)
            command = recognizer.recognize_google(audio).lower()
            print(f"Heard: '{command}'")
            update_user_data(command)
            return process_with_cohere(command)
        except sr.WaitTimeoutError:
            return None
        except sr.UnknownValueError:
            print("Could not understand audio")
            return None
        except sr.RequestError as e:
            print(f"Speech recognition error: {e}")
            return None

def process_with_cohere(command):
    if command.strip() in ["help", "activate face", "activate object", "activate text", "stop"]:
        return command
    response = co.generate(
        model='command',
        prompt=f"Refine this user command: {command}",
        max_tokens=50
    )
    refined_command = response.generations[0].text.strip().lower()
    print(f"Refined command: {refined_command}")
    return refined_command

def run_script(script_name):
    try:
        subprocess.run([sys.executable, script_name], check=True)
    except subprocess.CalledProcessError as e:
        speak("Error running the script.")
        print(f"Error: {e}")
    except FileNotFoundError:
        speak("Script not found.")
        print(f"Error: {script_name} not found")

def main():
    user_data = load_user_data()
    if user_data["name"]:
        speak(f"Welcome back {user_data['name']}, how can I assist you?")
    else:
        speak("Hello! What is your name?")
        name_command = listen_for_command()
        if name_command and "my name is" in name_command:
            update_user_data(name_command)

    print("Vision AI started. Listening for commands...")

    while True:
        command = listen_for_command()
        
        if command:
            if command.strip() == "stop":
                speak("Stopping the program.")
                print("Program stopped by user.")
                sys.exit()
            elif command.strip() == "activate face":
                speak("Activating face recognition model.")
                run_script(FACE_FILE)
            elif command.strip() == "activate object":
                speak("Activating object detection model.")
                run_script(OBJECT_FILE)
            elif command.strip() == "activate text":
                speak("Activating text recognition model")
                run_script(TEXT_FILE)
            elif command.strip() == "help":
                speak("Sending emergency alert.")
                run_script(EMERGENCY_FILE)
            else:
                response = co.generate(
                    model='command',
                    prompt=f"Respond conversationally to: {command}",
                    max_tokens=50
                )
                ai_reply = response.generations[0].text.strip()
                speak(ai_reply)
                print(f"AI Response: {ai_reply}")

            print("Returning to listening mode...")
            speak("How can I help you?")
        
        time.sleep(0.1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        speak("Shutting down Vision AI.")
        print("Shutting down...")
