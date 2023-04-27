# importing libraries
import requests
import speech_recognition as sr
import os
from pydub import AudioSegment
from pydub.silence import split_on_silence
import deepl
from googletrans import Translator, constants
from pprint import pprint

# create a speech recognition object
r = sr.Recognizer()


# a function that splits the audio file into chunks
# and applies speech recognition
def get_large_audio_transcription():
    """
    Splitting the large audio file into chunks
    and apply speech recognition on each of these chunks # Splits and speech to text
    """
    # open the audio file using pydub
    sound = AudioSegment.from_wav("simpli2.wav")
    # split audio sound where silence is 700 miliseconds or more and get chunks
    chunks = split_on_silence(sound,
                              # experiment with this value for your target audio file
                              min_silence_len=500,
                              # adjust this per requirement
                              silence_thresh=sound.dBFS - 15,
                              # keep the silence for 1 second, adjustable as well
                              keep_silence=500,
                              )
    folder_name = "audio-chunks"
    print(len(chunks))
    # create a directory to store the audio chunks
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
    whole_text = ""
    # process each chunk
    for i, audio_chunk in enumerate(chunks, start=1):
        # export audio chunk and save it in
        # the `folder_name` directory.
        chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
        audio_chunk.export(chunk_filename, format="wav")
        # recognize the chunk
        with sr.AudioFile(chunk_filename) as source:
            audio_listened = r.record(source)
            # try converting it to text
            try:
                text = r.recognize_google(audio_listened)
                translated = translate(text)
                print("mit diesem übersetzten text wird aufgerufen",translated)
                headers = {"xi-api-key": "7ede5162d024a392e4e50120d188ee33"}

                url = "https://api.elevenlabs.io/v1/text-to-speech/21m00Tcm4TlvDq8ikWAM"

                data = {

                    "text": translated,
                    "voice_settings": {
                        "stability": 0,
                        "similarity_boost": 0
                    }
                }

                print("response gesendet")
                response = requests.post(url, headers=headers, json=data)

                # Open file in binary write mode
                binary_file = open("my_file"+str(i)+".wav", "wb")

                # Write bytes to file
                binary_file.write(response.content)

                # Close file
                binary_file.close()
            except sr.UnknownValueError as e:
                print("Error:", str(e))
            else:
                text = f"{text.capitalize()}. "
                print(chunk_filename, ":", text)
                whole_text += text
    # return the text for all chunks detected
    return whole_text


translator = Translator()


def translate(text)->str:
    translation = translator.translate(text,dest="en",src="de")
    print(f"{translation.origin} ({translation.src}) --> {translation.text} ({translation.dest})")
    return translation.text

if __name__ == '__main__':
    get_large_audio_transcription()
