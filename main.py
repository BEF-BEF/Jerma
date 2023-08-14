from cleanYoutubeCode import load_secret_from_file, write_videos_to_csv, build
from utils import compare_directories_to_csv, generate_missing_urls_file
from cleanFasterWhisper import check_and_create_directories, initialize_csv, process_urls
from cleanIndex import index_content, search_indexed
from utils import fix_stacked_directories
from generateSubtitles import convert_transcriptions_to_srt
from stupidGithubTooManyDirectories import combine_directories, split_directories

def main():
    # Load the YouTube API key from a file. You'll need this and cookies.txt in a directory called secrets
    API_KEY = load_secret_from_file("secrets/api_key.txt")
    youtube = build('youtube', 'v3', developerKey=API_KEY)

    combine_directories()
    #UCK3kaNXbB57CLcyhtccV_yw
    # Write all info of all videos uploaded by JermaStreamArchive to a CSV file. Uses JermaStreamArchive's Channel ID
    write_videos_to_csv(youtube, "UCK3kaNXbB57CLcyhtccV_yw", "urlsAndDetails.csv")
    #write_videos_to_csv(youtube, "UC2oWuUSd3t3t5O3Vxp4lgAA", "urlsAndDetails.csv")
    # Compare directories to CSV and identify discrepancies
    compare_directories_to_csv()

    # Generate a txt containing missing URLs
    generate_missing_urls_file()
    check_and_create_directories()
    initialize_csv()

    # Transcribe missing videos
    process_urls()

    # # generate youtube subtitles
    # convert_transcriptions_to_srt()


    # # bandaid for when I transcribe video names that contain a /. fixes the multiple directories that creates
    # fix_stacked_directories()  - currently broken because github forces directories to have <= 1000 subdirectories
    # Index content for fast searching. It'll take a while the first time you run it then it's fast.
    index_content()
    search_indexed("he doesnt know")
    split_directories()

    # Search within the indexed content. Input gets cleaned and tokenized so you can use punctuation and vArIouS capitalization.
if __name__ == "__main__":
    main()

