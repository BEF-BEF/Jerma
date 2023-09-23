from cleanYoutubeCode import load_secret_from_file, write_videos_to_csv, build
from utils import compare_directories_to_csv, generate_missing_urls_file
from cleanFasterWhisper import check_and_create_directories, initialize_csv , process_urls
from cleanIndex import index_content, search_indexed
from utils import fix_stacked_directories, clean_csvs
from generateSubtitles import convert_transcriptions_to_srt
from stupidGithubTooManyDirectories import combine_directories, split_directories

# The commented out lines are for advanced users looking to transcribe videos. It's a bit complex to set up.
def main():

    # # Advanced: download new videos for transcription
    # # Load the YouTube API key from a file. You'll need this and cookies.txt in a directory called secrets
    # API_KEY = load_secret_from_file("secrets/api_key.txt")
    # youtube = build('youtube', 'v3', developerKey=API_KEY)
    # # Write all info of all videos uploaded by JermaStreamArchive to a CSV file. Uses JermaStreamArchive's Channel ID
    # write_videos_to_csv(youtube, "UC2oWuUSd3t3t5O3Vxp4lgAA", "urlsAndDetails.csv")


    combine_directories()
    combine_directories("subtitleDirectories","subtitleDirectories")

    clean_csvs()
    # Compare directories to CSV and identify discrepancies
    compare_directories_to_csv()

    # Generate a txt containing new URLs that need to be transcribed
    generate_missing_urls_file()
    check_and_create_directories()
    initialize_csv()

    # # Advanced: Transcribe missing videos
    # process_urls()

    # # Converts new transcriptions.txt to srt for youtube subtitles
    # convert_transcriptions_to_srt()


    # Index content for fast searching. It'll take a while the first time you run it then it's fast.
    
    index_content()
    search_term = input("Please enter a search term: ")

    # Call the function with the user's input
    search_indexed(search_term)

    split_directories()

    # Search within the indexed content. Input gets cleaned and tokenized so you can use punctuation and vArIouS capitalization.
if __name__ == "__main__":
    main()

