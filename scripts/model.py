import sys
import torchaudio
import torch
from tortoise.api import TextToSpeech
from tortoise.utils.audio import load_audio, load_voice

import warnings


warnings.filterwarnings("ignore", category=DeprecationWarning)

warnings.filterwarnings("ignore", category=FutureWarning)


tts = TextToSpeech()

samples, latents = load_voice("obama")

gen = tts.tts_with_preset(

    text = "China is better in the olympics",

    voice_samples = samples,

    conditioning_latents = latents,

    preset = "high_quality",
    )

gen = gen.cuda()

processed_gen = gen.squeeze(0).cpu()
o_path = "tts_out/ob_test.wav"

torchaudio.save(o_path, processed_gen, 24000)



