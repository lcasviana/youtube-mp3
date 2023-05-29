import os
import csv
import sys
from moviepy.editor import *
from pytube import YouTube
from pathlib import Path


def youtube2mp3(folder_name: str, file_name: str, video_url: str) -> None:
    if not os.path.isdir(folder_name):
      os.mkdir(folder_name)

    print(f'{file_name} ({video_url})')

    try:
        youtube = YouTube(video_url)
        highest_resolution_stream = youtube.streams.get_highest_resolution()

        highest_resolution_video = highest_resolution_stream.download(output_path='.')
        video_name, video_ext = os.path.splitext(highest_resolution_video)

        video_clip = VideoFileClip(highest_resolution_video)
        audio_clip = video_clip.audio

        audio_name = f'{video_name}.mp3'
        audio_clip.write_audiofile(
            audio_name, bitrate='320k', logger=None, verbose=False)

        final_audio_name = Path(f'./{folder_name}/{file_name}.mp3')
        os.rename(audio_name, final_audio_name)
        os.remove(f'{video_name}{video_ext}')

    except Exception as e:
        print(str(e))


def main():
    try:
        _, folder_name, csv_file = sys.argv

        if not folder_name or not csv_file:
            print('<folder_name> <csv_file>')
            sys.exit(0)

        with open(csv_file, mode ='r') as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            for file_name, video_url in reader:
                youtube2mp3(folder_name, file_name, video_url)
    except:
        print('<folder_name> <csv_file>')


if __name__ == '__main__':
    main()
