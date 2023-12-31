# Quick Start Tutorial

Advanced commands are commented out on main.py. This quick start tutorial will enable you to search the transcriptions. See the bottom of page if you want to transcribe videos yourself.

- Install Python3 from [this link](https://www.python.org/downloads/release/python-3114/). Ensure to check the box to add Python to your system path during installation as it will save you a lot of typing.

- Ensure [git](https://git-scm.com/downloads) is installed on your system.

- Open a terminal and run the following commands:

```
pip3 install nltk whoosh google-api-python-client yt_dlp faster_whisper
git clone https://github.com/BEF-BEF/Jerma.git
cd Jerma
python3 main.py
```
You may need to replace `python3` with `python` or `pip3` with `pip` depending on how your Python was installed. 

This will index all of the pre-transcribed files which will take a few minutes the first time and then prompts you to input a search term. After the first run, the files have already been indexed so it's much faster.


# Jerma
This uses Python3 to automatically transcribe all of the youtube videos posted by the Jerma Stream Archive youtube channel.
You can see the transcribed videos with timestamps inside of outDirectories, and subtitles inside of subtitleDirectories


```
    # Index content for fast searching. It'll take a while the first time you run it then it's fast.
    
    index_content()
    search_term = input("Please enter a search term: ")

    # Call the function with the user's input
    search_indexed(search_term)
```

these are the two lines that you need if you just want to search through the text. Index takes about 0.7 GB of storage space.

Transcriptions generated by whisper are not perfectly in sync with the videos' timestamp, but it'll be around the timestamp that is returned by the search function. For example, here's every time he has said cigarette:


```
Please enter a search term: cigarette
Found in: outDirectories/Jerma Streams - 700 000 Games Version 2.0 (Part 2 Finale)/transcription.txt during 16544.84s -> 16546.84s
URL: https://www.youtube.com/watch?v=szJ4LIKVmsc&t=16544s
Found in: outDirectories/Jerma Streams - Nancy Drew Secrets Can Kill/transcription.txt during 3958.84s -> 3960.84s
URL: https://www.youtube.com/watch?v=2VzJkfzZaOU&t=3958s
Found in: outDirectories/Jerma Streams - 3DO Games (Part 3)/transcription.txt during 2148.16s -> 2148.66s
URL: https://www.youtube.com/watch?v=ZCVi3SYsp7w&t=2148s
Found in: outDirectories/Jerma Streams - 3DO Games (Part 3)/transcription.txt during 4691.02s -> 4696.12s
URL: https://www.youtube.com/watch?v=ZCVi3SYsp7w&t=4691s
Found in: outDirectories/Jerma Streams - 3DO Games (Part 3)/transcription.txt during 4712.32s -> 4714.72s
URL: https://www.youtube.com/watch?v=ZCVi3SYsp7w&t=4712s
Found in: outDirectories/Jerma Streams - 3DO Games (Part 3)/transcription.txt during 4716.09s -> 4716.59s
URL: https://www.youtube.com/watch?v=ZCVi3SYsp7w&t=4716s
Found in: outDirectories/Jerma Streams - 3DO Games (Part 3)/transcription.txt during 4719.04s -> 4719.54s
URL: https://www.youtube.com/watch?v=ZCVi3SYsp7w&t=4719s
Found in: outDirectories/Jerma Streams - Flash Games (Part 3)/transcription.txt during 18420.89s -> 18421.37s
URL: https://www.youtube.com/watch?v=5RL0ZY2xpZs&t=18420s
Found in: outDirectories/Jerma Streams - Stream Awards 2021 and WWE 2K20/transcription.txt during 11141.38s -> 11143.81s
URL: https://www.youtube.com/watch?v=6MEYUy91Y90&t=11141s
Found in: outDirectories/Jerma Streams - Travellers Rest/transcription.txt during 8344.65s -> 8345.29s
URL: https://www.youtube.com/watch?v=wODQR5JIElU&t=8344s
```

## complete faster-whisper installation documentation if you want to transcribe new videos

Commented lines function on my Ubuntu pc but require more complicated installs and are not planned to be tested on Windows. I don't have those installs fully documented. Here's a start though:

Using Ubuntu or another Linux distro is highly recommended. NVIDIA GPU required.

You will need to get a youtube api key and cookies.txt in secrets.

Get a youtube API key: https://developers.google.com/youtube/v3/getting-started

Get cookies.txt: I used cookies.txt extension in firefox

Look at [faster whisper's github](https://github.com/guillaumekln/faster-whisper) for installation requirements. It's a bit intensive.

