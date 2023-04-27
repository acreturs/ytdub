from pydub import AudioSegment
from pydub.silence import detect_nonsilent
from pydub import AudioSegment

# adjust target amplitude





def split2(t1,t2,calls):
    t1 = t1 * 1000  # Works in milliseconds
    t2 = t2 * 1000
    newAudio = AudioSegment.from_wav("testaudio.wav")
    calls += 1
    newAudio = newAudio[t1:t2]
    newAudio.export("newSong"+ str(calls) +".wav", format="wav")  # Exports to a wav file in the current path.


def match_target_amplitude(sound, target_dBFS):
    change_in_dBFS = target_dBFS - sound.dBFS
    return sound.apply_gain(change_in_dBFS)


def split():
    # Convert wav to audio_segment
    audio_segment = AudioSegment.from_wav("testaudio.wav")

    # normalize audio_segment to -20dBFS
    normalized_sound = match_target_amplitude(audio_segment, -10.0)#umso niedriger die Zahl, umso weniger Geräusch wird als Geräusch erkannt TODO ich will, dass er länger aufnimmt, nach Pause länger wartet
    print("length of audio_segment={} seconds".format(len(normalized_sound) / 1000))

    # Print detected non-silent chunks, which in our case would be spoken words.
    nonsilent_data = detect_nonsilent(normalized_sound, min_silence_len=500, silence_thresh=-20, seek_step=1) #hier für silence thresh ist -20 normal aber variert glaube von Ding zu Ding
    #todo bei -26 wird Zeug zusammensortiert

    # convert ms to seconds
    print("start,Stop")
    call = 0
    for chunks in nonsilent_data:
        #print(type(chunks))
        t1 = chunks[0]/1000
        t2 = (chunks[1])/1000
        split2(t1,t2,call)
        call+=1
        print("lol", [chunk / 1000 for chunk in chunks])



if __name__ == '__main__':
    split()