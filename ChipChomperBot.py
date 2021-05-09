import glob, os
import pathlib
import time
import random
import discord
from dotenv import load_dotenv



AUDIO_PATH = str(pathlib.Path(__file__).parent.absolute())
AUDIO_PATH = AUDIO_PATH.replace("\\", "/") + "/audio_files/"
FFMPEG_PATH = "C:/ffmpeg/bin/ffmpeg.exe"
load_dotenv()
CLIENT = discord.Client()
TOKEN = os.getenv("DISCORD_TOKEN")

def get_audio_files():
    """
    Get a list of audio files under the audio_files directory
    :return: dict, contains file names as well as track length
    """
    os.chdir(AUDIO_PATH)
    audio_tracks = {}
    return [file for file in glob.glob("*.mp3")]


async def play_audio(context):
    """
    Play an audio file from the audio_files directory
    :param context: Discord Context
    """
    user = context.author
    voice_channel = user.voice.channel  # get users curr voice channel
    vc = await context.author.voice.channel.connect()  # join channel
    if vc is None:
        print("Not a valid voice channel, user may not be in a channel")

    vc.play(discord.FFmpegPCMAudio(executable=FFMPEG_PATH,
                                   source=AUDIO_PATH + random.choice(get_audio_files())))

    time.sleep(1)
    while vc.is_playing():
        time.sleep(.5)
    await vc.disconnect()


@CLIENT.event
async def on_message(context):
    if context.author == CLIENT.user:  # if msg is from the bot
        return
    elif context.content.lower() == "!chip":
        await play_audio(context)
    else:
        print(context)



CLIENT.run(TOKEN)