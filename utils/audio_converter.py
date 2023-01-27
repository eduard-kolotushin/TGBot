import speech_recognition as sr
from pydub import AudioSegment
import os


# convert audio to text
def convert_audio_to_text(folder, file_name):
    # convert audio to text
    r = sr.Recognizer()
    file_name = convert_ogg_to_wav(folder, file_name)
    with sr.AudioFile(os.path.join(folder, file_name)) as source:
        audio = r.record(source)  # read the entire audio file
    try:
        text = r.recognize_google(audio, language="ru")
        print("Google Speech Recognition thinks you said " + text)
    except sr.UnknownValueError:
        # print("Google Speech Recognition could not understand audio")
        text = "Google Speech Recognition could not understand audio"
    except sr.RequestError as e:
        # print("Could not request results from Google Speech Recognition service; {0}".format(e))
        text = "Could not request results from Google Speech Recognition service; {0}".format(e)
    return text


# convert ogg to wav
def convert_ogg_to_wav(folder, file_name):
    orig_song = os.path.join(folder, file_name)
    dest_song = os.path.join(folder, file_name.split(".")[0] + ".wav")

    song = AudioSegment.from_ogg(orig_song)
    song.export(dest_song, format="wav")

    return file_name.split(".")[0] + ".wav"
