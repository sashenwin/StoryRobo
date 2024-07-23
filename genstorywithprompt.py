import requests
import speech_recognition as sr
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
import io


# Function to speak a prompt
def speak_prompt(text):
    tts = gTTS(text=text, lang='en')
    audio_io = io.BytesIO()
    tts.write_to_fp(audio_io)
    audio_io.seek(0)
    audio = AudioSegment.from_mp3(audio_io)
    play(audio)

# Function to capture speech and convert to text
def capture_speech():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    print("Listening...")
    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        # Convert speech to text
        text = recognizer.recognize_google(audio)
        print(f"Captured Speech: {text}")
        return text
    except sr.UnknownValueError:
        print("Sorry, I could not understand the audio.")
        return ""
    except sr.RequestError:
        print("Sorry, there was an issue with the speech recognition service.")
        return ""

# Function to generate a story using the Gemini API
def generate_story(prompt_text, api_key):
    api_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent"
    
    # Modify the payload to request a story of approximately 100 words
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": f"Generate a short story of about 100 words about {prompt_text}"}
                ]
            }
        ]
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(f"{api_url}?key={api_key}", json=payload, headers=headers)

    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        print(response.text)
        response.raise_for_status()  # Check if the request was successful

    response_json = response.json()
    try:
        story_text = response_json['candidates'][0]['content']['parts'][0]['text']
        return story_text
    except (KeyError, IndexError) as e:
        print(f"Error extracting story text: {e}")
        return ""

# Function to convert text to speech and play it
def play_story(story_text):
    tts = gTTS(text=story_text, lang='en')
    audio_io = io.BytesIO()
    tts.write_to_fp(audio_io)
    audio_io.seek(0)
    audio = AudioSegment.from_mp3(audio_io)
    play(audio)

# Main execution
def main():
    # Speak the initial prompt
    speak_prompt("Hi. I'm Blah. What do you want to hear a story about?")
    
    # Capture user input via microphone
    user_input = capture_speech()
    
    if user_input:
        # Generate the story based on user input
        api_key = "AIzaSyDz5jzw8dSz7EEaMfK_T45FZsaNsilTnz4"  # Replace with your API key
        story_text = generate_story(user_input, api_key)
        
        if story_text:
            # Optionally trim the story to about 100 words
            story_text = ' '.join(story_text.split()[:100])
            
            # Convert the generated story to speech and play it
            play_story(story_text)
        else:
            print("No story text received.")
    else:
        print("No input received.")

if __name__ == "__main__":
    main()