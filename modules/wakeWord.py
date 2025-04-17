import pvporcupine
import pyaudio
import struct

class WakeWordDetector:
    def __init__(self, keyword="friday"): 
        self.keyword = keyword
        self.porcupine = pvporcupine.create(keywords=[self.keyword])
        self.audio_stream = None

    def start_listening(self):
        self.audio_stream = pyaudio.PyAudio().open(
            rate=self.porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=self.porcupine.frame_length
        )

        print("🎤 Waiting for wake word: Hey Friday...")

        while True:
            audio_frame = self.audio_stream.read(self.porcupine.frame_length, exception_on_overflow=False)
            audio_data = struct.unpack_from("h" * self.porcupine.frame_length, audio_frame)

            result = self.porcupine.process(audio_data)
            if result >= 0:
                print("✅ Wake word detected! Activating FRIDAY...")
                break

        self.audio_stream.close()

if __name__ == "__main__":
    detector = WakeWordDetector()
    detector.start_listening()
