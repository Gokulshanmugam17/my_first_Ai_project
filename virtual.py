import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import os
import time
import subprocess
from ecapture import ecapture as ec
import wolframalpha
import requests
import random
import tkinter as tk
from tkinter import ttk, scrolledtext
import threading

print('Loading your AI personal assistant - Suji')

# Initialize pyttsx3 for offline speech
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Female voice

# Global variable to access GUI text display
gui_output = None

def speak(text):
    """Speak with correct pronunciation of 'Suji' as 'Soojie'"""
    if gui_output:
        gui_output.insert(tk.END, f"Suji: {text}\n")
        gui_output.see(tk.END)

    # Force correct pronunciation in speech only
    fixed_text = text.replace("Suji", "Soojie")
    engine.say(fixed_text)
    engine.runAndWait()

def wishMe():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Hello, Good Morning")
    elif 12 <= hour < 18:
        speak("Hello, Good Afternoon")
    else:
        speak("Hello, Good Evening")

def takeCommand():
    """Listen and recognize voice command"""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        if gui_output:
            gui_output.insert(tk.END, "Listening...\n")
            gui_output.see(tk.END)
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
        try:
            statement = r.recognize_google(audio, language='en-in')
            if gui_output:
                gui_output.insert(tk.END, f"You: {statement}\n")
                gui_output.see(tk.END)
            print(f"User said: {statement}\n")
        except Exception:
            speak("Pardon me, please say that again.")
            return "None"
        return statement

def run_suji():
    wishMe()
    speak("Loading your AI personal assistant Suji")

    while True:
        speak("Tell me, how can I help you now?")
        statement = takeCommand().lower()

        if statement == 0 or statement == "none":
            continue

        if "good bye" in statement or "stop" in statement:
            speak('Your personal assistant Suji is shutting down. Good bye!')
            break

        elif 'wikipedia' in statement:
            speak('Searching Wikipedia...')
            statement = statement.replace("wikipedia", "")
            results = wikipedia.summary(statement, sentences=3)
            speak("According to Wikipedia")
            speak(results)

        elif "play video" in statement:

            speak("What video should I play?")


            video_name = takeCommand()


            if video_name != "None":
                speak(f"Searching for {video_name} on YouTube")
                webbrowser.open_new_tab(f"https://www.youtube.com/results?search_query={video_name}")



        elif 'open youtube' in statement:
            webbrowser.open_new_tab("https://www.youtube.com")
            speak("YouTube is open now")

        elif 'open google' in statement:
            webbrowser.open_new_tab("https://www.google.com")
            speak("Google is open now")

        elif 'open gmail' in statement:
            webbrowser.open_new_tab("https://mail.google.com")
            speak("Gmail is open now")

        elif 'open camera' in statement or 'take a photo' in statement:
            subprocess.run('start microsoft.windows.camera:', shell=True)
            speak("Opening camera")

        elif 'suggest a movie' in statement or 'recommend any movie' in statement:

            speak("Here’s a movie you might enjoy")
            movies = ["The Shawshank Redemption", "96", "Nayakan", "Thalapathi ","anbe sivam", "Forrest Gump"]
            movie = random.choice(movies)
            speak(movie)
            webbrowser.open_new_tab(f"https://www.google.com/search?q={movie}+movie")


        elif "weather condition" in statement:
            api_key = "8ef61edcf1c576d65d836254e11ea420"
            base_url = "https://api.openweathermap.org/data/2.5/weather?"
            speak("What is the city name?")
            city_name = takeCommand()
            complete_url = base_url + "appid=" + api_key + "&q=" + city_name
            response = requests.get(complete_url)
            x = response.json()
            if x["cod"] != "404":
                y = x["main"]
                current_temperature = y["temp"]
                current_humidity = y["humidity"]
                z = x["weather"]
                weather_description = z[0]["description"]
                speak(f"Temperature: {current_temperature} Kelvin")
                speak(f"Humidity: {current_humidity}%")
                speak(f"Weather description: {weather_description}")
            else:
                speak("City not found.")

        elif 'time' in statement:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The time is {strTime}")

        elif 'who are you' in statement or 'what can you do' in statement:
            speak('I am Suji, your personal assistant. I can open apps, fetch information, tell the weather, and more!')

        elif 'open map' in statement or 'show me directions' in statement:
            speak("Where do you want to go?")
            destination = takeCommand()
            webbrowser.open(f"https://www.google.com/maps/place/{destination}")
            speak(f"Showing directions to {destination}")

        elif "who made you" in statement or "who created you" in statement:
            speak("I was built by GOKUL SM")

        elif "open calculator" in statement:
            speak("Opening Calculator")
            subprocess.Popen("calc.exe")


        elif 'news' in statement:
            webbrowser.open_new_tab("https://timesofindia.indiatimes.com/home/headlines")
            speak("Here are today's top headlines")

        elif 'search' in statement:
            statement = statement.replace("search", "")
            webbrowser.open_new_tab(f"https://www.google.com/search?q={statement}")
            speak(f"Here’s what I found for {statement}")

        elif 'ask' in statement:
            speak('Ask me a computational or geographical question now')
            question = takeCommand()
            app_id = "R2K75H-7ELALHR35X"
            client = wolframalpha.Client(app_id)
            res = client.query(question)
            answer = next(res.results).text
            speak(answer)

        elif "log off" in statement or "sign out" in statement:
            speak("Ok, your PC will log off in 10 seconds. Make sure to close all applications.")
            subprocess.call(["shutdown", "/l"])

# --- GUI (Black Background + White Text with Output Display) ---

def start_gui():
    global gui_output
    root = tk.Tk()
    root.title("Suji - AI Personal Assistant")
    root.geometry("600x500")
    root.configure(bg='black')

    style = ttk.Style()
    style.theme_use('clam')
    style.configure('TButton', font=('Segoe UI', 12), padding=10, foreground='white', background='black')
    style.configure('TLabel', font=('Segoe UI', 16), background='black', foreground='white')

    title = ttk.Label(root, text="Suji - Your AI Assistant")
    title.pack(pady=10)

    gui_output = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=('Consolas', 12), bg='black', fg='white', height=15)
    gui_output.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    def threaded_run():
        t = threading.Thread(target=run_suji)
        t.start()

    start_btn = ttk.Button(root, text="Start Assistant", command=threaded_run)
    start_btn.pack(pady=10)

    quit_btn = ttk.Button(root, text="Quit", command=root.destroy)
    quit_btn.pack(pady=5)

    root.mainloop()

# Run GUI
if __name__ == "__main__":
    start_gui()
