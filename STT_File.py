import io
import os
import wave

from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
from pydub import AudioSegment
from pydub.silence import split_on_silence

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="Speech-To-Text.json"

def STT_File(file_name):

    client = speech.SpeechClient()
    if file_name[-4:] == ".mp3":
        sound = AudioSegment.from_file(file_name, format='mp3')
        file_name = file_name[0:-4]+'.wav'
        sound.export(file_name, format='wav')
        song = AudioSegment.from_wav(file_name)
    elif file_name[-4:] == ".wav":
        song = AudioSegment.from_wav(file_name)
    else:
        print("The Format of file should be either .mp3 or wav")
        return

    file_waveObj = wave.open(file_name)
    no_of_channels = file_waveObj.getnchannels()
    sampling_rate = file_waveObj.getframerate()
    if no_of_channels>1:
        recognition_per_channel = True
    else:
        recognition_per_channel = False
    file_waveObj.close()

    chunks = split_on_silence(song, min_silence_len=500, silence_thresh=-25)


    for chunk in chunks:
        chunk_silent = AudioSegment.silent(duration=100)

        audio_chunk = chunk_silent + chunk + chunk_silent

        print("saving chunk.wav")

        audio_chunk.export("chunk.wav", bitrate='192k', format="wav")

        with io.open('chunk.wav', 'rb') as audio_file:
            content = audio_file.read()
            audio = types.RecognitionAudio(content=content)

        config = types.RecognitionConfig(
            encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
            language_code='en-US',
            sample_rate_hertz=sampling_rate,
            audio_channel_count=no_of_channels,
            enable_separate_recognition_per_channel=recognition_per_channel)

        response = client.recognize(config, audio)

        for result in response.results:
            print(result.alternatives[0].transcript)

        os.remove("chunk.wav")


