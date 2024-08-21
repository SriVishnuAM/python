import speech_recognition as sr
import pyttsx3
import spacy
import requests
import pyautogui
from datetime import datetime
from simpleeval import SimpleEval
from PIL import Image
import pytesseract
from googletrans import Translator
import random
import sys

# Load the small English model
nlp = spacy.load("en_core_web_sm")

# Initialize the text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)    # Speed of speech
engine.setProperty('volume', 0.9)  # Volume level (0.0 to 1.0)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Changing the index changes the voice

# API keys and URLs
WEATHER_API_KEY = 'your_openweathermap_api_key_here'
WEATHER_API_URL = 'http://api.openweathermap.org/data/2.5/weather'
NEWS_API_KEY = 'your_newsapi_key_here'
NEWS_API_URL = 'https://newsapi.org/v2/top-headlines'

# Initialize Google Translator
translator = Translator()

# Configure Tesseract executable path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def speak(text):
    """Convert text to speech."""
    print(f"Bot: {text}")
    engine.say(text)
    engine.runAndWait()

def listen():
    """Listen for audio input and return recognized text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Adjusting for ambient noise...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Listening...")
        try:
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=10)
            print("Audio received, processing...")
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            return command.lower()
        except sr.WaitTimeoutError:
            print("Listening timed out.")
            speak("Listening timed out. Please try again.")
            return None
        except sr.UnknownValueError:
            print("Sorry, I didn't understand that.")
            speak("Sorry, I didn't understand that.")
            return None
        except sr.RequestError as e:
            print(f"Request error: {e}")
            speak("Sorry, there was an error with the speech recognition service.")
            return None

def get_weather(city):
    """Fetch the current weather for a given city."""
    params = {
        'q': city,
        'appid': WEATHER_API_KEY,
        'units': 'metric'  # Use 'imperial' for Fahrenheit
    }
    try:
        response = requests.get(WEATHER_API_URL, params=params)
        data = response.json()
        
        if data.get('cod') != 200:
            return "Sorry, I couldn't fetch the weather information. Please check the city name and try again."
        
        description = data['weather'][0]['description']
        temp = data['main']['temp']
        return f"The weather in {city} is currently {description} with a temperature of {temp}°C."
    
    except Exception as e:
        print(f"Error fetching weather data: {e}")
        return "Sorry, I couldn't fetch the weather information at the moment."

def get_time():
    """Return the current time."""
    now = datetime.now()
    return now.strftime("The current time is %I:%M %p.")

def calculate_math(expression):
    """Evaluate a mathematical expression safely."""
    evaluator = SimpleEval()
    try:
        result = evaluator.eval(expression)
        return f"The result is {result}."
    except Exception as e:
        print(f"Math evaluation error: {e}")
        return "Sorry, I couldn't perform the calculation. Please try again."

def take_screenshot():
    """Take a screenshot and save it as 'screenshot.png'."""
    try:
        screenshot = pyautogui.screenshot()
        screenshot.save("screenshot.png")
        return "Screenshot taken and saved as 'screenshot.png'."
    except Exception as e:
        print(f"Screenshot error: {e}")
        return "Sorry, I couldn't take a screenshot."

def get_news():
    """Fetch the latest news headlines."""
    params = {
        'country': 'us',
        'apiKey': NEWS_API_KEY
    }
    try:
        response = requests.get(NEWS_API_URL, params=params)
        data = response.json()
        headlines = [article['title'] for article in data['articles'][:5]]
        return "Here are the latest news headlines: " + ", ".join(headlines)
    except Exception as e:
        print(f"Error fetching news: {e}")
        return "Sorry, I couldn't fetch the news at the moment."

def translate_text(text, dest_lang='en'):
    """Translate text to the specified language."""
    try:
        translated = translator.translate(text, dest=dest_lang)
        return translated.text
    except Exception as e:
        print(f"Error translating text: {e}")
        return "Sorry, I couldn't translate the text."

def describe_image(image_path):
    """Describe the contents of an image using Tesseract OCR."""
    try:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img)
        return text if text.strip() else "No text found in the image."
    except Exception as e:
        print(f"Error processing image: {e}")
        return "Sorry, I couldn't process the image."

def play_trivia():
    """Play a simple trivia game."""
    questions = {
        "What is the capital of France?": "Paris",
        "What is 2 + 2?": "4",
        "Who wrote 'To Kill a Mockingbird'?": "Harper Lee"
    }
    question, answer = random.choice(list(questions.items()))
    return question, answer

def start_trivia():
    """Start a trivia game."""
    question, answer = play_trivia()
    speak(question)
    user_answer = listen()
    if user_answer and answer.lower() in user_answer:
        speak("Correct!")
    else:
        speak(f"Incorrect. The answer is {answer}.")

def process_command(command):
    """Process the command using spaCy and respond accordingly."""
    if not command:
        return
    
    doc = nlp(command)
    tokens = [token.text.lower() for token in doc]
    
    if any(name in tokens for name in ["siddharth", "siddarth"]):
        speak("The rich man, right?")
        
    elif any(name in tokens for name in ["vishnu"]):
        speak("The rizzler, right?")
        
    elif "exit" in tokens or "goodbye" in tokens:
        speak("Goodbye!")
        sys.exit(0)
        
    elif "open" in tokens and "camera" in tokens:
        speak("The Camera has been opened.")
        # Add camera logic if needed
        
    elif "weather" in tokens and "in" in tokens:
        city_index = tokens.index("in") + 1
        if city_index < len(tokens):
            city = " ".join(tokens[city_index:])
            weather_info = get_weather(city)
            speak(weather_info)
        else:
            speak("Please specify the city for the weather update.")
        
    elif "time" in tokens or "current time" in tokens:
        time_info = get_time()
        speak(time_info)
        
    elif "calculate" in tokens or "what is" in tokens:
        if "calculate" in tokens:
            expression_index = tokens.index("calculate") + 1
        else:
            expression_index = tokens.index("what") + 2
        
        if expression_index < len(tokens):
            expression = " ".join(tokens[expression_index:])
            result = calculate_math(expression)
            speak(result)
        else:
            speak("Please provide a mathematical expression to calculate.")
        
    elif "screenshot" in tokens:
        screenshot_info = take_screenshot()
        speak(screenshot_info)
        
    elif "news" in tokens:
        news_info = get_news()
        speak(news_info)
        
    elif "translate" in tokens:
        if "to" in tokens:
            language_index = tokens.index("to") + 1
            if language_index < len(tokens):
                language = tokens[language_index]
                text = " ".join(tokens[tokens.index("translate") + 1:])
                translation = translate_text(text, dest_lang=language)
                speak(translation)
            else:
                speak("Please specify the target language for translation.")
        else:
            speak("Please include 'to' followed by the target language in your translation request.")
        
    elif "trivia" in tokens:
        start_trivia()
        
    elif "image" in tokens and "describe" in tokens:
        image_path = "path_to_image.jpg"  # Replace with actual image path
        description = describe_image(image_path)
        speak(description)
        
    else:
        speak("I'm not sure how to respond to that. Can you ask something else?")

if __name__ == "__main__":
    print("Starting the voice-enabled chatbot...")
    speak("Hello! I am your voice-enabled chatbot. Say 'exit' to stop.")
    
    while True:
        command = listen()
        process_command(command)
