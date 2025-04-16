import pywhatkit
import datetime
import wikipedia
import webbrowser
import speech_recognition as sr
from gtts import gTTS
import pygame
import os
import time

# Initialize the pygame mixer
pygame.mixer.init()


def speak(text):
    tts = gTTS(text=text, lang='en')
    filename = "temp.mp3"
    tts.save(filename)

    try:
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

        pygame.mixer.music.stop()
        pygame.mixer.music.unload()

    except Exception as e:
        print(f"Error playing audio: {e}")
    finally:
        time.sleep(0.5)  # Delay to ensure file is not in use
        if os.path.exists(filename):
            try:
                os.remove(filename)
            except PermissionError:
                print("Couldn't delete temp.mp3, file still in use.")


def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source)
            command = recognizer.recognize_google(audio)
            return command.lower()
        except sr.UnknownValueError:
            speak("Sorry, I didn't catch that.")
            return ""
        except sr.RequestError:
            speak("Could not connect to Google Speech Recognition.")
            return ""


def execute_command(command):
    if "time" in command:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {current_time}")

    elif "search for" in command:
        query = command.replace("search for", "").strip()
        speak(f"Searching for {query}")
        pywhatkit.search(query)

    elif "play" in command:
        song = command.replace("play", "").strip()
        speak(f"Playing {song} on YouTube")
        pywhatkit.playonyt(song)

    elif "wikipedia" in command:
        topic = command.replace("wikipedia", "").strip()
        try:
            summary = wikipedia.summary(topic, sentences=1)
            speak(summary)
        except wikipedia.exceptions.DisambiguationError as e:
            speak("There are multiple entries. Please be more specific.")
        except wikipedia.exceptions.PageError:
            speak("I couldn't find that topic on Wikipedia.")

    elif "open google" in command:
        speak("Opening Google")
        webbrowser.open("https://www.google.com")

    elif "exit" in command:
        speak("Goodbye!")
        exit()

    else:
        speak("I didn't understand that command.")


# Run once
speak("Hello Aiman! How can I assist you?")
command = listen()
if command:
    execute_command(command)


