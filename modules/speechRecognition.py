from vosk import Model, KaldiRecognizer
import pyaudio
import json
import spacy

# Load spaCy transformer-based model
nlp = spacy.load("en_core_web_trf")

# Path to VOSK model
modelPath = r"vosk-model-en-in-0.5"

class SpeechRecognizer:
    def __init__(self, model_path=modelPath):
        self.model = Model(model_path)
        self.recognizer = KaldiRecognizer(self.model, 16000)
        self.audio_stream = None

    def start_listening(self, use_wake_word=True):
        try:
            self.audio_stream = pyaudio.PyAudio().open(
                format=pyaudio.paInt16,
                channels=1,
                rate=16000,
                input=True,
                frames_per_buffer=8192
            )
            self.audio_stream.start_stream()
            print("🎤 Listening for commands... Say 'Friday' to activate.")
        except Exception as e:
            print(f"❌ Microphone error: {e}")
            return {"original_text": "", "verbs": [], "nouns": []}

        while True:
            data = self.audio_stream.read(4096, exception_on_overflow=False)
            if self.recognizer.AcceptWaveform(data):
                result = json.loads(self.recognizer.Result())
                text = result.get("text", "").strip()

                if not text:
                    continue

                print(f"🗣️ You said: {text}")

                # Wake word check
                if use_wake_word:
                    if not text.lower().startswith("friday"):
                        continue
                    text = text[6:].strip()  

                # Exit commands (for testing/debug)
                if text.lower() in ["exit", "quit", "stop", "bye"]:
                    print("👋 Exiting recognizer loop.")
                    break

                return self.process_text(text)

    def process_text(self, text):
        doc = nlp(text)
        verbs = [token.text for token in doc if token.pos_ == "VERB"]
        nouns = [token.text for token in doc if token.pos_ == "NOUN"]

        return {
            "original_text": text,
            "verbs": verbs,
            "nouns": nouns
        }

    def process_text_only(self, text):
        """Use this for text-only input (no mic)"""
        return self.process_text(text)

    def stop(self):
        if self.audio_stream:
            self.audio_stream.stop_stream()
            self.audio_stream.close()
            print("🛑 Audio stream closed.")

if __name__ == "__main__":
    recognizer = SpeechRecognizer()
    result = recognizer.start_listening()
    print("📝 Recognized Command:", result)
