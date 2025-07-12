import speech_recognition as sr
import pyttsx3
import subprocess
import sys
import time

recognizer = sr.Recognizer()
tts_engine = pyttsx3.init()
tts_engine.setProperty('rate', 150)
tts_engine.setProperty('volume', 1.0)

FACE_FILE = "face.py"
OBJECT_FILE = "object.py"
TEXT_FILE = "text.py"
EMERGENCY_FILE = "emergency.py"

def speak(text):
    """Convert text to speech."""
    tts_engine.say(text)
    tts_engine.runAndWait()

def listen_for_command():
    """Listen for voice commands."""
    with sr.Microphone() as source:
        print("Listening...", end="\r")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        try:
            audio = recognizer.listen(source, timeout=None)
            command = recognizer.recognize_google(audio).lower()
            print(f"Heard: '{command}'")
            return command
        except sr.WaitTimeoutError:
            return None
        except sr.UnknownValueError:
            print("Could not understand audio")
            return None
        except sr.RequestError as e:
            print(f"Speech recognition error: {e}")
            return None

def run_script(script_name):
    """Run the specified Python script and return to listening mode."""
    try:
        subprocess.run([sys.executable, script_name], check=True)
    except subprocess.CalledProcessError as e:
        speak("Error running the script.")
        print(f"Error: {e}")
    except FileNotFoundError:
        speak("Script not found.")
        print(f"Error: {script_name} not found")

def main():
    # Initial greeting when the code starts
    speak("It's your AI assistant VISION here!! How can I help you?")
    print("Vision AI started. Listening for commands...")
    
    while True:
        command = listen_for_command()
        
        if command:
            if "activate face" in command:
                speak("activating face recognition model.")
                run_script(FACE_FILE)
            elif "activate object" in command:
                speak("activating object detection model.")
                run_script(OBJECT_FILE)
            elif "activate text" in command:
                speak("activating text recognition model")
                run_script(TEXT_FILE)
            elif "help" in command:
                speak("Sending emergency alert.")
                run_script(EMERGENCY_FILE)
            else:
                speak("ask again please....didnt got what u said!!!")
            
            # Prompt for the next command
            print("Returning to listening mode...")
            speak("How can I help you?")
        
        # Prevent high CPU usage
        time.sleep(0.1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        speak("Shutting down Vision AI.")
        print("Shutting down...")