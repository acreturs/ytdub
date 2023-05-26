from pydub import AudioSegment
from pydub.silence import detect_nonsilent
from pydub import AudioSegment
import requests
import whisper
import json

def SpeechToTextAndTranslate():
    model = whisper.load_model("base")
    result = model.transcribe("simple3.mp3")
    print(result["text"])

    print("erste Request")

    url = "https://api-free.deepl.com/v2/translate"
    headers = {
        "Authorization": "DeepL-Auth-Key 61abe4b3-4e02-5c66-981f-cbcd3f336e76:fx",
        "User-Agent": "YourApp/1.2.3",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    payload = {
        "text": result["text"],
        "target_lang": "EN"
    }

    response = requests.post(url, headers=headers, data=payload)

    # Print the response
    data = response.json()

    # Extract the translated text
    translations = data["translations"]
    translated_text = translations[0]["text"]
    print(translated_text)
    textToSpeechAPIRequest(translated_text)




# Receives two timestamps and splits the current file at these timestamps. Still needs to be handed the correct file
def splitFileAtTimeStamps(t1, t2, calls):
    t1 = t1 * 1000  # Works in milliseconds
    t2 = t2 * 1000
    newAudio = AudioSegment.from_wav("testaudio.wav")
    calls += 1
    newAudio = newAudio[t1:t2]
    newAudio.export("newSong" + str(calls) + ".wav", format="wav")



#Currently calls elevenlabs to get the written text in audio form
def textToSpeechAPIRequest(text):
    print("in text TO speech")
    headers = {"xi-api-key": "7ede5162d024a392e4e50120d188ee33"}

    url = "https://api.elevenlabs.io/v1/text-to-speech/21m00Tcm4TlvDq8ikWAM"

    data = {

        "text": text,
        "voice_settings": {
            "stability": 0,
            "similarity_boost": 0
        }
    }

    print("response gesendet")
    response = requests.post(url, headers=headers, json=data)

    # Open file in binary write mode
    binary_file = open("my_fileTest.wav", "wb")

    # Write bytes to file
    binary_file.write(response.content)

    # Close file
    binary_file.close()


#To split the audio file correctly
def match_target_amplitude(sound, target_dBFS):
    change_in_dBFS = target_dBFS - sound.dBFS
    return sound.apply_gain(change_in_dBFS)


def split():
    audio_segment = AudioSegment.from_wav("testaudio.wav")

    # normalize audio_segment to -20dBFS
    normalized_sound = match_target_amplitude(audio_segment,
                                              -10.0)  # umso niedriger die Zahl, umso weniger Geräusch wird als Geräusch erkannt TODO ich will, dass er länger aufnimmt, nach Pause länger wartet
    print("length of audio_segment={} seconds".format(len(normalized_sound) / 1000))

    nonsilent_data = detect_nonsilent(normalized_sound, min_silence_len=500, silence_thresh=-20,
                                      seek_step=1)  # hier für silence thresh ist -20 normal aber variert glaube von Ding zu Ding
    # todo bei -26 wird Zeug zusammensortiert

    # convert ms to seconds
    print("start,Stop")
    call = 0
    for chunks in nonsilent_data:
        # print(type(chunks))
        t1 = chunks[0] / 1000
        t2 = (chunks[1]) / 1000
        splitFileAtTimeStamps(t1, t2, call)
        call += 1
        print("lol", [chunk / 1000 for chunk in chunks])


if __name__ == '__main__':
    SpeechToTextAndTranslate()
