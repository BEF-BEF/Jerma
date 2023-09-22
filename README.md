# Quick start tutorial
install python3: https://www.python.org/downloads/release/python-3114/
make sure git is installed (https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
open a terminal and run: ```pip3 install nltk whoosh```
```git clone https://github.com/BEF-BEF/Jerma.git
cd Jerma
python3 main.py```

This will index all of the pre-transcribed files which might take a few minutes the first time and then prompt you to input a search term. After the first time it's much faster.

# Jerma
This uses Python3 to automatically transcribe all of the youtube videos posted by the Jerma Stream Archive youtube channel.
You can see the transcribed videos with timestamps inside of outDirectories.
You can search them by doing the following:

install python3: https://www.python.org/downloads/release/python-3114/. Install it for your system. Make sure to select add to path while installing it.

open terminal and run: ```pip3 install nltk whoosh```

download this project, navigate to it in terminal,and run ```python3 main.py```





in main.py, these lines should be the only ones uncommented to start. Further lines function but require more complicated installs.
```
   # Index content for fast searching. It'll take a while the first time you run it then it's fast.
   index_content()


   # Search within the indexed content. Input gets cleaned and tokenized so you can use punctuation and vArIouS capitalization.
   search_indexed("Crack time!")
```

these are the two lines that you need if you just want to search through the text. Index takes about 0.7 GB of storage space.

You can edit "Crack time!" to anything else. My transcriptions are not perfectly in sync with the videos and I don't know why yet, but it'll be around the timestamp that is provided by the search function. For example, here's every time he has said cigarette:

in main.py
    search_indexed("cigarette")

```
Found in: outDirectories/Jerma Streams - 700 000 Games Version 2.0 (Part 2 Finale)/transcription.txt during 16544.84s -> 16546.84s
URL: https://www.youtube.com/watch?v=szJ4LIKVmsc&t=16544s
Found in: outDirectories/Jerma Streams - Nancy Drew: Secrets Can Kill/transcription.txt during 3958.84s -> 3960.84s
URL: https://www.youtube.com/watch?v=2VzJkfzZaOU&t=3958s
Found in: outDirectories/Jerma Streams - Flash Games (Part 3)/transcription.txt during 18420.89s -> 18421.37s
URL: https://www.youtube.com/watch?v=5RL0ZY2xpZs&t=18420s
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
Found in: outDirectories/Jerma Streams - Travellers Rest/transcription.txt during 8344.65s -> 8345.29s
URL: https://www.youtube.com/watch?v=wODQR5JIElU&t=8344s
Found in: outDirectories/Jerma Streams - Stream Awards 2021 and WWE 2K20/transcription.txt during 11141.38s -> 11143.81s
URL: https://www.youtube.com/watch?v=6MEYUy91Y90&t=11141s
```

## complete faster-whisper installation documentation if you want to transcribe new videos


You will need to get a youtube api key and cookies.txt in secrets.

Get a youtube API key: https://developers.google.com/youtube/v3/getting-started

Get cookies.txt: I used cookies.txt extension in firefox

Do more pip installs
```
pip3 install --upgrade google-api-python-client

pip3 install yt_dlp

pip3 install faster-whisper

```

