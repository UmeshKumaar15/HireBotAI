# import pyttsx3
# import threading

# class TextToSpeech:
#     def __init__(self):
#         self.engine = pyttsx3.init()
#         self.engine.setProperty('rate', 180)
#         self.engine.setProperty('volume', 1.0)
#         self.speech_thread = None  # Thread for speech
#         self.lock = threading.Lock()  # Prevent overlapping speech

#     def set_voice(self, gender="male"):
#         voices = self.engine.getProperty('voices')
#         gender_index = 0  # Default to first voice (male)
#         if gender.lower() == "female":
#             for i, voice in enumerate(voices):
#                 if "female" in voice.name.lower():
#                     gender_index = i
#                     break
#         self.engine.setProperty('voice', voices[gender_index].id)

#     def speak(self, content, gender="male"):
#         with self.lock:  # Prevents multiple speech runs at the same time
#             self.set_voice(gender)

#             # Stop any previous speech loop to prevent conflicts
#             try:
#                 self.engine.endLoop()
#             except RuntimeError:
#                 pass  # Ignore error if the loop is not running

#             # Function to run speech in a separate thread
#             def speak_thread():
#                 self.engine.say(content)
#                 self.engine.runAndWait()

#             # If a thread is already running, wait for it to finish
#             if self.speech_thread and self.speech_thread.is_alive():
#                 self.speech_thread.join()

#             # Start a new speech thread
#             self.speech_thread = threading.Thread(target=speak_thread, daemon=True)
#             self.speech_thread.start()


import threading
import simpleaudio  # New library for playing the audio
from TTS.api import TTS

class TextToSpeech:
    def __init__(self):
        self.tts = TTS("tts_models/en/vctk/vits").to("cpu")  # Load VITS Model
        self.speech_thread = None  # Thread for speech
        self.lock = threading.Lock()  # Prevent overlapping speech
        self.default_speaker = "p231"  # Default speaker

    def set_voice(self, gender="female"):
        """VITS uses predefined speakers. Gender selection maps to specific speakers."""
        if gender.lower() == "female":
            self.default_speaker = "p273"  # Use different speaker for female
        else:
            self.default_speaker = "p231"  # Default male speaker

    def speak(self, content, gender="female"):
        with self.lock:  # Prevents multiple speech runs at the same time
            self.set_voice(gender)

            def speak_thread():
                self.tts.tts_to_file(text=content, file_path="output.wav", speaker=self.default_speaker)  # Generate speech

                # Play the audio file using simpleaudio
                wave_obj = simpleaudio.WaveObject.from_wave_file("output.wav")
                play_obj = wave_obj.play()
                play_obj.wait_done()  # Wait until playback is finished

            # If a thread is already running, wait for it to finish
            if self.speech_thread and self.speech_thread.is_alive():
                self.speech_thread.join()

            # Start a new speech thread
            self.speech_thread = threading.Thread(target=speak_thread, daemon=True)
            self.speech_thread.start()
