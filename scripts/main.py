import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)

warnings.filterwarnings("ignore", category=FutureWarning)


import textwrap
import praw
import os

import multiprocessing

import torchaudio
from tortoise.api import TextToSpeech
from tortoise.utils.audio import load_voice



#constants
REDDIT = praw.Reddit(client_id = 'KzX-qywS2yAz0GJb5Xr41g',

                     client_secret = 'dTtnJHi-YdNO-MS3hsJyj82VJFmFwQ',

                     user_agent = 'tiktok by u/IAmFatChoy')

SUBREDDIT_NAME = "amitheasshole"

ABBREVIATIONS = {
    'bf': 'boyfriend',
    'gf': 'girlfriend',
    'btw': 'by the way',
    'omg': 'oh my god',
    'idk': 'I don’t know',
    'lol': 'laugh out loud',
    'brb': 'be right back',
    'gtg': 'got to go',
    'tbh': 'to be honest',
    'smh': 'shaking my head',
    'ttyl': 'talk to you later',
    'imo': 'in my opinion',
    'imho': 'in my humble opinion',
    'fyi': 'for your information',
    'asap': 'as soon as possible',
    'bff': 'best friends forever',
    'nvm': 'never mind',
    'thx': 'thanks',
    'u': 'you',
    'ur': 'your/you’re',
    'pls': 'please',
    'ppl': 'people',
    'msg': 'message',
    'wtf': 'what the f**k',
    'lmao': 'laughing my a** off',
    'rofl': 'rolling on the floor laughing',
    'np': 'no problem',
    'omw': 'on my way',
    'jk': 'just kidding',
    'tmi': 'too much information',
    'cya': 'see you',
    'wbu': 'what about you',
    'yolo': 'you only live once',
    'b4': 'before',
    '2moro': 'tomorrow',
    '4u': 'for you',
    '4ever': 'forever',
    'hbu': 'how about you',
    'idc': 'I don’t care',
    'icymi': 'in case you missed it',
    'ily': 'I love you',
    'iirc': 'if I recall correctly',
    'irl': 'in real life',
    'lmk': 'let me know',
    'rn': 'right now',
    'smh': 'shaking my head',
    'stfu': 'shut the f**k up',
    'tbh': 'to be honest',
    'thx': 'thanks',
    'tl;dr': 'too long; didn’t read',
    'ur': 'your/you’re',
    'w/': 'with',
    'w/o': 'without',
    'y': 'why',
    'yw': 'you’re welcome',
}

TTS = TextToSpeech()

TTS_VOICE = 'obama'

SAMPLES, LATENTS = load_voice(TTS_VOICE)


def fetch_reddit_posts(subreddit_name, limit = 5):

    subreddit = REDDIT.subreddit(subreddit_name)
    
    posts = [post for post in subreddit.hot(limit = limit)]

    return posts


def save_posts_to_file(post, directory):

    filename = f"{post.id}.txt"

    filepath = os.path.join(directory, filename)
    
    with open(filepath, 'w', encoding='utf-8') as file:

        file.write(f"Title: {post.title}\nText: {replace_abbreviations(post.selftext, ABBREVIATIONS)}")


def replace_abbreviations(text, abbreviations):

    words = text.split()
    
    new_words = [abbreviations[word.lower()] if word.lower() in abbreviations else word for word in words]
    
    return ' '.join(new_words)


def text_to_speech(file_path, output_path):
    
    tts = TTS.to('cuda')

    samples = samples.to('cuda')

    latents = latents.to('cuda')


    with open(file_path, 'r', encoding = 'utf-8') as file:
        text = file.read()


    audio = tts.tts_with_preset(

        text = text,

        voice_samples = samples,

        conditioning_latents = latents,

        preset = "high_quality",

        )
    
    audio = audio.cuda()

    audio = audio.squeeze.cpu()

    torchaudio.save(output_path, audio, 24000)


def main():

    posts = fetch_reddit_posts(SUBREDDIT_NAME, 5)
    
    directory = 'reddit_posts'

    if not os.path.exists(directory):
        
        os.makedirs(directory)

    for post in posts:

        save_posts_to_file(post, directory)
    


    text_files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.txt')]

    processes = []

    for i, file_path in enumerate(text_files):

        output_path = f'audio_output_{i}.wav'
        
        p = multiprocessing.Process(target = text_to_speech, args = (file_path, output_path))
        
        processes.append(p)

        p.start()

    for p in processes:

        p.join()


if __name__ == "__main__":
    
    main()