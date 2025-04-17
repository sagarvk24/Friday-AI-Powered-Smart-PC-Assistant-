import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from modules.speechRecognition import SpeechRecognizer
from modules.textToSpeech import TextToSpeech
from modules.commands import CommandProcessor

def main():
    recognizer = SpeechRecognizer()
    tts = TextToSpeech(voice_id=1)  # 0 for Male, 1 for Female
    command_processor = CommandProcessor()

    tts.speak("Hey User, I’m ready whenever you are. Just say 'Friday' to begin.")

    while True:
        print("\n✨ Say 'Friday' to begin your command...")
        result = recognizer.start_listening(use_wake_word=True)
        text = result.get("original_text", "")

        if not text:

            
            tts.speak("Sorry, I didn't catch that. Could you repeat?")
            continue

        if text.lower() in ["bye", "stop", "quit", "goodbye"]:
            tts.speak("Goodbye, User! Have a great day.")
            break

        # Special handling for casual talks
        if "who are you" in text.lower():
            response = "I'm Friday, your loyal smart assistant and your Bestie forever 💖"

        else:
            response = command_processor.process_command(text)

            if "Sorry Bestie" in response:
                # NLP fallback if not a recognized command
                verbs = ", ".join(result["verbs"]) if result["verbs"] else "No verbs found"
                nouns = ", ".join(result["nouns"]) if result["nouns"] else "No nouns found"
                response = f"You said: {text}. Detected verbs: {verbs}. Nouns: {nouns}."

        tts.speak(response)

if __name__ == "__main__":
    main()
