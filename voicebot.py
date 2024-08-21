import speech_recognition as sr
import pyttsx3
import spacy

# Load the small English model
nlp = spacy.load("en_core_web_sm")

def speak(text):
    print(text)
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            speak("Sorry, I didn't understand that.")
            return None
        except sr.RequestError:
            speak("Sorry, there was an error with the speech recognition service.")
            return None

                
def process_command(command):
    """Process the command using spaCy and respond accordingly."""
    if not command:
        return
    
    # Process the command with spaCy NLP
    doc = nlp(command)
    tokens = [token.text.lower() for token in doc]
    
    if "hello" in tokens:
        speak("Hello! How can I help you today?")
        
    elif "exit" in tokens or "goodbye" in tokens:
        speak("Goodbye!")
        sys.exit(0)
        
    elif "open" in tokens and "camera" in tokens:
        speak("The Camera has been opened.")
        # Here, you can add the logic to actually open the camera if needed
        
    else:
        speak("I'm not sure how to respond to that. Can you ask something else?")
        
if __name__ == "__main__":
    print("Starting the voice-enabled chatbot...")
    speak("Hello! I am your voice-enabled chatbot. Say 'exit' to stop.")
    
    while True:
        command = listen()
        process_command(command)