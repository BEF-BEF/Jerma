# Jerma
do pip installs


`pip3 install nltk whoosh`


run main.py


`python3 main.py`






   # Index content for fast searching. It'll take a while the first time you run it then it's fast.
   index_content()


   # Search within the indexed content. Input gets cleaned and tokenized so you can use punctuation and vArIouS capitalization.
   search_indexed("Crack time!")


these are the two lines that you need if you just want to search through the text. Index takes about 0.7 GB of storage space.








### look at faster-whisper installation documentation if you want to transcribe new videos.


You will need to get a youtube api key and cookies.txt in secrets.


```
pip3 install --upgrade google-api-python-client

pip3 install yt_dlp

pip3 install faster-whisper

```

