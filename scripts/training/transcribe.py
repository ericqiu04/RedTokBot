import whisper
import os
import json
import warnings

model = whisper.load_model("base")
warnings.filterwarnings("ignore", category=UserWarning, message="FP16 is not supported on CPU; using FP32 instead")


input_path = "../../input_audio/o_data/"
output_path = "../../input_audio/transcription/"
os.makedirs(output_path, exist_ok=True)

metadata = []

for file in os.listdir(input_path):
    if file.endswith(".wav"):
        audio_path = os.path.join(input_path, file)
        result = model.transcribe(audio_path)
        transcript = result['text']
        metadata.append([file, transcript])
        with open(os.path.join(output_path, file.replace(".wav", ".txt")), "w") as f:
            f.write(transcript)

with open('training_data.json', 'w') as f:
    json.dump(metadata, f)