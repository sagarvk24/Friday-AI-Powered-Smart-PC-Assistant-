import pyttsx3
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
import os
import tempfile

class TextToSpeech:
    def __init__(self, mode="offline", voice_id=None, rate=170, volume=0.9):
        self.mode = mode.lower()

        if self.mode == "offline":
            self.setup_offline_engine(voice_id, rate, volume)

    def setup_offline_engine(self, voice_id, rate, volume):
        self.engine = pyttsx3.init(driverName='sapi5')
        voices = self.engine.getProperty('voices')

        if voice_id is not None and 0 <= voice_id < len(voices):
            self.engine.setProperty('voice', voices[voice_id].id)
        else:
            self.engine.setProperty('voice', voices[0].id)

        self.engine.setProperty('rate', rate)
        self.engine.setProperty('volume', volume)

    def soften_audio(self, sound, tempo=0.95):
        """Makes the voice calmer and softer"""
        return sound._spawn(sound.raw_data, overrides={
            "frame_rate": int(sound.frame_rate * tempo)
        }).set_frame_rate(sound.frame_rate)

    def speak(self, text):
        if not text:
            print("⚠️ No text provided to speak.")
            return

        print(f"🗣️ User says: {text}")

        if self.mode == "offline":
            self.engine.say(text)
            self.engine.runAndWait()

        elif self.mode == "online":
            try:
                tts = gTTS(text=text, lang='en', slow=False)  
                fd, path = tempfile.mkstemp(suffix=".mp3")
                os.close(fd)

                tts.save(path)
                audio = AudioSegment.from_file(path, format="mp3")
                calm_audio = self.soften_audio(audio, tempo=1.1)  
                play(calm_audio)
                os.remove(path)

            except Exception as e:
                print(f"❌ Error using gTTS: {e}")
                print("⚠️ Falling back to offline mode...")

                if not hasattr(self, 'engine'):
                    self.setup_offline_engine(voice_id=1, rate=170, volume=0.9)

                self.engine.say(text)
                self.engine.runAndWait()

    def list_voices(self):
        if self.mode == "offline":
            voices = self.engine.getProperty('voices')
            for idx, voice in enumerate(voices):
                print(f"Voice {idx}: {voice.name} ({voice.id})")
        else:
            print("🔊 Voice listing only available in offline mode.")

if __name__ == "__main__":
    tts = TextToSpeech(mode="online")
    tts.speak("Hey! You are doing really well. I’m so proud of you. Just keep going, okay?")

