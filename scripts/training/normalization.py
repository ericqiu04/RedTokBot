import librosa
import soundfile as sf
import os

#improves quality of the audio files
def preprocess_audio(file_path, output_path):
    try:
        y, sr = sf.read(file_path)
        y = librosa.effects.preemphasis(y)
        y = librosa.util.normalize(y)
        sf.write(output_path, y, int(sr))
    except Exception as e:
        print(f"Error processing {file_path}: {e}")


#will process only .wav files
input_path = "../../input_audio/data/"
output_path = "../../input_audio/o_data"
os.makedirs(output_path, exist_ok=True)
for file in os.listdir(input_path):
    if file.endswith(".wav"):
        preprocess_audio(os.path.join(input_path, file), os.path.join(output_path, file))
    else:
        print(f"Skipping non-audio file: {file}")
