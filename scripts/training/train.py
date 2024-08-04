import pandas as pd
import librosa
import soundfile as sf
import os


csv_path = "../../input_audio/dataset.csv"
audio_path = "../../input_audio/o_data"
process_path = "../../input_audio/p_audio"

data = pd.read_csv(csv_path)


def process_audio(path):
    audio, sr = librosa.load(path, sr=22050)
    processed_path = os.path.join(process_path, os.path.basename(path))
    sf.write(processed_path, audio, sr)
    return processed_path


if not os.path.exists(process_path):
    os.makedirs(process_path)

data['processed_path'] = data['path'].apply(lambda x: process_audio(os.path.join(audio_path, x)))
new_csv_path = os.path.join(process_path, 'processed_data.csv')
data.to_csv(new_csv_path, index=False)
