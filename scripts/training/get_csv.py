import os
import csv

wav_path = "../../input_audio/o_data/"
trans_path = "../../input_audio/transcription/"

csv_file = "../../input_audio/dataset.csv"

with open(csv_file, mode = "w", newline= '') as f:
    writer = csv.writer(f)
    writer.writerow(["path", "text"])
    for t in os.listdir(trans_path):
        if t.endswith(".txt"):
            audio_file = t.replace(".txt", ".wav")
            a_path = os.path.join(wav_path, audio_file)
            t_path = os.path.join(trans_path, t)
            if not os.path.exists(t_path):
                continue
            print(f"1: {t_path}")  # Debug print
            with open(t_path, 'r') as file:
                transcript = file.read().strip()
            if os.path.exists(a_path):
                writer.writerow([a_path, transcript])
