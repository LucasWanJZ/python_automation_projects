from pytube import YouTube
import tkinter as tk
from tkinter import filedialog
from pydub import AudioSegment
import os

def convert_webm_to_mp3(webm_file,output_file_path):
    try:
        webm_file.export(output_file_path, format="mp3")
    except Exception as e:
        print(f"Error during conversion: {e}")

def download_youtube(url, save_path,format):
    try:
        yt = YouTube(url)
        if (format == 'mp4'):
            streams = yt.streams.filter(progressive=True, file_extension=format)
            highest_res_stream = streams.get_highest_resolution();  
            highest_res_stream.download(output_path=save_path)
            print("Download successful")
        elif (format == 'mp3'):
            audio_streams = yt.streams.filter(only_audio=True).order_by('abr').desc().first()
            audio_file_path = audio_streams.download(output_path=save_path)

            mp4_audio = AudioSegment.from_file(audio_file_path, format="mp4")
            mp3_file_path = os.path.splitext(audio_file_path)[0] + ".mp3"
            convert_webm_to_mp3(mp4_audio, mp3_file_path)

            os.remove(audio_file_path)

            print("Download MP3 successful")
    except Exception as e:
        print(e)
        print("Download failed")

def open_file_dialog():
    folder = filedialog.askdirectory()
    if folder:
        print("Selected folder: ", folder)
    return folder

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()

    url = input("Enter the YouTube URL: ")
    save_path = open_file_dialog()

    if not save_path:
        print("No folder selected...")
    else:
        format = input("Enter the format (mp4 or mp3): ")
        print("Downloading...")
        download_youtube(url, save_path, format)

