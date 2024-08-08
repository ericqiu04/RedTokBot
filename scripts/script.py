import warnings

# Suppress specific future warnings
warnings.filterwarnings("ignore", message=".*weights_only=False.*", category=FutureWarning)
warnings.filterwarnings("ignore", message=".*Some weights of the model.*", category=UserWarning)
warnings.filterwarnings("ignore", message=".*torch.nn.utils.weight_norm is deprecated.*", category=FutureWarning)

import textwrap
import praw
import os

import torchaudio
import torch

from pydub import AudioSegment

from tortoise.api import TextToSpeech
from tortoise.utils.audio import load_audio, load_voice

import warnings


warnings.filterwarnings("ignore", category=DeprecationWarning)

warnings.filterwarnings("ignore", category=FutureWarning)

tts = TextToSpeech()

samples, latents = load_voice("obama")

from datetime import datetime

reddit = praw.Reddit(client_id = 'KzX-qywS2yAz0GJb5Xr41g',

                     client_secret = 'dTtnJHi-YdNO-MS3hsJyj82VJFmFwQ',

                     user_agent = 'tiktok by u/IAmFatChoy')

abbreviations = {
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

def replace_abbreviations(text, abbreviations):

    words = text.split()
    
    new_words = [abbreviations[word.lower()] if word.lower() in abbreviations else word for word in words]
    
    return ' '.join(new_words)


def fetch_reddit_post(subreddit_name, limit):
    
    subreddit = reddit.subreddit(subreddit_name)
    
    return [post for post in subreddit.new(limit=limit)]


def load_processed_ids(file_path):
    
    if not os.path.exists(file_path):
    
        return set()
    
    with open(file_path, 'r') as file:
    
        return set(line.strip() for line in file)


def save_proceessed_ids(file_path, ids):
    
    with open(file_path, 'a') as file:
    
        for post_id in ids:
    
            file.write(post_id + '\n')


def save_post_content(post, directory):
    
    file_path = os.path.join(directory, f"{post.id}.txt")
    
    with open(file_path, 'w') as file:
    
        file.write(post.selftext)

    return file_path


def text_to_speech(text, output_path):
    
    TEXT = replace_abbreviations(text, abbreviations)
    
    parts = textwrap.wrap(text, width=300, break_long_words=False, replace_whitespace=False)

    audio_files = []

    for i, part in enumerate(parts):

        audio_file_path = f"{i}{output_path}"

        gen = tts.tts_with_preset(

        text = part,

        voice_samples = samples,

        conditioning_latents = latents,

        preset = "high_quality",

        )
        gen = gen.cuda()
        
        processed_gen = gen.squeeze(0).cpu()
    
        torchaudio.save(output_path, processed_gen, 24000)
        
        audio_files.append(audio_file_path)

    combined = AudioSegment.empty()

    for file in audio_files:
        segment = AudioSegment.from_mp3(file)
        combined += segment
    
    combined.export(output_path, format = "mp3")
    



def main():
    
    subreddit_name = 'amitheasshole'
    
    limit = 5
    
    processed_ids_file = 'processed_ids.txt'

    date_str = datetime.now().strftime("%Y-%m-%d")

    os.makedirs(date_str, exist_ok = True)

    processed_ids = load_processed_ids(processed_ids_file)

    new_posts = []

    posts = fetch_reddit_post(subreddit_name, limit = limit * 2)


    for p in posts:

        if p.id not in processed_ids:

            new_posts.append(p)

        if len(new_posts) == limit:

            break

    new_ids = set()

    for post in new_posts:

        post_file_path = save_post_content(post, date_str)

        print(f"Saved post {post_file_path}")

        audio_file_path = os.path.join(date_str, f"{post.id}.mp3")

        print(f"Saved Audio {audio_file_path}")

        text_to_speech(post.selftext, audio_file_path)

        new_ids.add(post.id)

    save_proceessed_ids(processed_ids_file, new_ids)

    print(f"Processed Post IDS saved to {processed_ids_file}")

if __name__ == "__main__":

    main()