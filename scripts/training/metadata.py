import os
import json

wav_path = "../../input_audio/o_data"
trans_path = "../../input_audio/transcription"
metadata = []

for file in os.listdir(trans_path):
    if file.endswith(".txt"):
        audio_file = file.replace(".txt", ".wav")
        audio_path = os.path.join(wav_path, audio_file)
        with open(os.path.join(trans_path, file), 'r') as f:
            transcript = f.read().strip()

        if os.path.exists(audio_path):
            metadata.append([audio_path, transcript])

with open('training_data.json', 'w') as f:
    json.dump(metadata, f)
