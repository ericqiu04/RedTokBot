from pydub import AudioSegment

sound = AudioSegment.from_wav('tts_out/test.wav')

sound.export('tts_out/test.mp3', format="mp3")
