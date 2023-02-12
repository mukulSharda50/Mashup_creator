from googleapiclient.discovery import build
import youtube_dl
from pydub import AudioSegment
import os
import sys


def search_videos(query, n):
    try:
        print("=====================Searching Videos=====================")

        api_key = "AIzaSyDAMVgYAPsz4lDZ18kUuZtEG0NJK9iM5A8"
        youtube = build("youtube", "v3", developerKey=api_key)
        request = youtube.search().list(
            part="id",
            type='video',
            q=query,
            maxResults=n
        )
        response = request.execute()
        videos = []
        for result in response.get("items", []):
            videos.append("https://www.youtube.com/watch?v=" + result["id"]["videoId"])
        return videos
    except Exception as e:
        raise Exception("Problem in searching Videos: ", e)


def download_videos(url):
    try:
        print("=====================Downloading Videos=====================")

        download_path = os.path.join(os.getcwd(), "downloads/")
        ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': download_path + '%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except Exception as e:
        raise Exception("Problem in downloading Videos: ", e)


def cut(output_path, sec):
    try:
        print("=====================Creating Mashup=====================")

        # os.chdir(os.path.join(os.getcwd(), "downloads"))
        # print(os.getcwd())
        for file in os.listdir('downloads'):
            print(file)
            if file.endswith(".mp3"):
                new_filename = file.split(sep='.')[0] + '-cut.mp3'
                cut_audio(file, os.path.join(output_path, new_filename), sec)
    except Exception as e:
        raise Exception("Problem in cutting audio: ", e)

def cut_audio(input_file, output_file, Y):    
    try:
        StrtMin = 0
        StrtSec = 1
        EndMin = 0
        EndSec = int(Y) + 2
        StrtTime = StrtMin*60*1000+StrtSec*1000
        EndTime = EndMin*60*1000+EndSec*1000
        sound = AudioSegment.from_mp3(os.path.join(os.getcwd(), "downloads", input_file))
        sound[StrtTime:EndTime].export(output_file, format=output_file.split(".")[-1])
    except Exception as e:
        raise Exception("Problem in cutting_audio: ", e)

def merge_audio(file_path, output_file):
    try:
        combined = AudioSegment.empty()
        for file in os.listdir(file_path):
            combined += AudioSegment.from_file(os.path.join(os.getcwd(), "segments", file))
        combined.export(output_file, format=output_file.split(".")[-1])
    except Exception as e:
        raise Exception("Problem in merging audios: ", e)


def setup_dirs():
    try:
        download_dir = os.path.join(os.getcwd(), "downloads")
        if not os.path.exists(download_dir):
            os.mkdir(download_dir)

        segments_dir = os.path.join(os.getcwd(), "segments")
        if not os.path.exists(segments_dir):
            os.mkdir(segments_dir)

        result_dir = os.path.join(os.getcwd(), "results")
        if not os.path.exists(result_dir):
            os.mkdir(result_dir)
        
        return download_dir, segments_dir, result_dir
        
    except Exception as e:
        raise Exception("Problem in setting up download directory. ", e)


def search_and_download(singer, n):
    urls = search_videos(singer, n)
    for url in urls:
        download_videos(url)


def main(n, sec, singer, output_name):
    try:
        download_dir, segments_dir, result_dir = setup_dirs()
        # search_and_download(singer, n)
        cut(segments_dir, sec)    
        merge_audio(segments_dir, os.path.join(result_dir, output_name))

    except Exception as e:
        print("Error Occured: ",e)

if __name__ == '__main__':
    if len(sys.argv) < 4:
        raise Exception("Not enough parameters: specify singer name, number of videos, audio duration, output file name.")

    singer = sys.argv[1]
    n = sys.argv[2]
    sec = sys.argv[3]
    output_name = sys.argv[4]

    if output_name.split(sep='.')[-1] != 'mp3':
        raise Exception("Please enter a valid mp3 file to save output.")
    main(n, sec, singer, output_name)
    
        

    