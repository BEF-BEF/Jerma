import os
import csv
import yt_dlp
import urllib.error
import glob
import datetime
from faster_whisper import WhisperModel
import subprocess
import logging
from utils import clean_folder_name
    # Download Audio from URLs: The script utilizes the yt_dlp library to download the best audio version of content from specified URLs. These URLs are read from a file named "remainingURLS5.txt".

    # Check Processed URLs: Before downloading or processing a URL, the script checks a CSV file to see if the URL has already been processed. This is to avoid redundant work and save time.

    # Transcription: The script transcribes the downloaded audio using the Faster Whisper model. The transcription results, including timestamps, are saved to a text file.

    # Logging & Storage: Processed URLs, along with their transcription details and timing, are logged to a CSV file. The program supports a "testing" mode, where it uses different directory and file names to avoid overwriting production data.

    # Error Handling: If there are any issues with downloading or processing a URL (e.g., network errors), the error is logged in the CSV file against that URL.

# Constants and Configurations
CONFIG = {
    "url_file": "missingURLS.txt",
    "testing": False,
    "gpu_index": 0,
    "initial_prompt":"Hey guys, welcome to my stream. I'm friends with Ster."
}
CONFIG["audio_folder"] = "JermAudioTest" if CONFIG["testing"] else "JermAudio"
CONFIG["out_folder"] = "outDirTest" if CONFIG["testing"] else "outDirectories"
CONFIG["csv_name"] = "processed_streamsTest.csv" if CONFIG["testing"] else "processed_streams.csv"

# Logging setup
logging.basicConfig()
logging.getLogger("faster_whisper").setLevel(logging.DEBUG)

def trim_audio(input_file, output_file, trim_duration=300):
    """Trim the audio to the specified duration using ffmpeg."""
    command = ["ffmpeg", "-i", input_file, "-t", str(trim_duration), "-c:a", "copy", output_file]
    subprocess.call(command)

def is_url_processed(csv_file, url):
    """Check if a URL has been processed by checking the CSV file."""
    with open(csv_file, "r", encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader, None)  # Skip the header
        for row in reader:
            if row[1] == url:
                if row[0] != "ERROR":
                    return True
    return False


def transcribe_audio(file_path, output_dir):
    """Transcribe an audio file using the Faster Whisper model."""


    #model = WhisperModel("medium", device="cuda",device_index=CONFIG["gpu_index"], compute_type="float16", local_files_only=True)
    model = WhisperModel("large-v2", device="cuda",device_index=CONFIG["gpu_index"], compute_type="float16", local_files_only=True)

    segments, info = model.transcribe(file_path, beam_size=5, language="en", initial_prompt=CONFIG["initial_prompt"], vad_filter=True, vad_parameters=dict(min_silence_duration_ms=500, speech_pad_ms=200))
    print("PATH: " + str(os.path.join(output_dir, 'transcription.txt')))
    with open(os.path.join(output_dir, 'transcription.txt'), 'w') as f:
        for segment in segments:
            write_string = f"[{segment.start:.2f}s -> {segment.end:.2f}s] {segment.text}\n"
            print(write_string)
            f.write(write_string)

def check_and_create_directories():
    for dir_path in [CONFIG["audio_folder"], CONFIG["out_folder"]]:
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
def initialize_csv():
    with open(CONFIG["csv_name"], "a+", newline="", encoding='utf-8') as f:
        writer = csv.writer(f)
        f.seek(0)
        if f.readline() == '':
            writer.writerow(["Title", "URL", "Processed", "Error", "Whisper Transcription Time (MM:SS)", "Total Processing Time (MM:SS)", "Device"])

def write_to_csv(data):
    with open(CONFIG["csv_name"], "a+", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(data)

def process_urls():
    
    ydl_opts = {
        'format': 'bestaudio[ext=m4a]',
        'outtmpl': os.path.join(CONFIG["audio_folder"], '%(title)s.%(ext)s'),
        'restrictfilenames': True,
        'cookiefile': 'secrets/cookies.txt',
        "quiet": True,
    }


    with open(CONFIG["url_file"], "r", encoding='utf-8') as f:
        urls = f.read().splitlines()


    for url in urls:
        video_title = "ERROR"
        if is_url_processed(CONFIG["csv_name"], url):
            print(f"URL {url} has already been processed, skipping.")
            continue

        total_start_time = datetime.datetime.now()
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    try:
                        info_dict = ydl.extract_info(url, download=True)
                        video_title = info_dict.get('title', None)
                        print(video_title + " has been successfully downloaded.")

                        list_of_files = glob.glob(CONFIG["audio_folder"]+'/*')
                        latest_file = max(list_of_files, key=os.path.getctime)

                        whisper_output_dir = os.path.join(CONFIG["out_folder"], clean_folder_name(video_title))
                        if not os.path.exists(whisper_output_dir):
                            os.makedirs(whisper_output_dir)
                        if CONFIG["testing"]:
                            trimmedFile = os.path.join(CONFIG["audio_folder"], f"trimmed_{video_title}.m4a")
                            trim_audio(latest_file, trimmedFile)
                            latest_file=trimmedFile

                        # Start timing for Whisper transcription
                        whisper_start_time = datetime.datetime.now()
                        # Use the Faster Whisper model
                        transcribe_audio(latest_file, whisper_output_dir)
                        whisper_time = str(datetime.datetime.now() - whisper_start_time)[:-7]

                        os.remove(latest_file)

                        total_time = str(datetime.datetime.now() - total_start_time)[:-7]            
                        write_to_csv([video_title, url, "True", "", whisper_time, total_time, "3090"])
                    
                    except urllib.error.URLError as e:
                        print("Network Error: ", str(e))
                        write_to_csv([video_title, url, "False", str(e), "", str(datetime.datetime.now() - total_start_time)[:-7], "3090"])
                    except Exception as e:
                        print("Error: ", str(e))
                        write_to_csv([video_title, url, "False", str(e), "", str(datetime.datetime.now() - total_start_time)[:-7], "3090"])

def main():
    check_and_create_directories()
    initialize_csv()
    process_urls()

if __name__ == "__main__":
    main()
