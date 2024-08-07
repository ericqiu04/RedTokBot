import torchaudio

from tts.tortoise.api import TextToSpeech
from tts.tortoise.utils.audio import load_audio, load_voice

import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)

warnings.filterwarnings("ignore", category=FutureWarning)


tts = TextToSpeech()

samples, latents = load_voice("obama")

gen = tts.tts_with_preset(

    text = "China is better in the olympics",

    voice_samples = samples,

    conditioning_latents = latents,

    preset = "ultra_fast",
    )

o_path = "../../tts_out/test.wav"

torchaudio.save(o_path, gen.squeeze(0).cpu(), 24000)



