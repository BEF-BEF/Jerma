# Jerma
do pip installs

run main.py

comment out things until you stop getting errors


look at faster-whisper installation documentation if you want to transcribe new videos.

You will need to get a youtube api key and cookies.txt in secrets.

    # Index content for fast searching. It'll take a while the first time you run it then it's fast.
    index_content()

    # Search within the indexed content. Input gets cleaned and tokenized so you can use punctuation and vArIouS capitalization.
    search_indexed("Crack time!")

these are the two lines that you need if you just want to search through the text
