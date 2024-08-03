
import textwrap
import praw
import os
import torchaudio
import torch
import torchaudio.transforms as transforms
from pydub import AudioSegment
from tortoise.api import TextToSpeech
from tortoise.utils.audio import load_audio
from datetime import datetime


reddit = praw.Reddit(client_id = 'KzX-qywS2yAz0GJb5Xr41g',
                     client_secret = 'dTtnJHi-YdNO-MS3hsJyj82VJFmFwQ',
                     user_agent = 'tiktok by u/IAmFatChoy')


tts = TextToSpeech()
voice_sample_dir = 'voice_samples'
clips_path = [os.path.join(voice_sample_dir, filename) for filename in os.listdir(voice_sample_dir) if filename.endswith(".wav")]
ref_clips = [load_audio(p, 22050) for p in clips_path]
pcm_audio = tts.tts_with_preset("hello world", voice_samples=ref_clips, preset='standard')
