from cleanYoutubeCode import load_secret_from_file, write_videos_to_csv, build
from utils import compare_directories_to_csv, generate_missing_urls_file
from cleanFasterWhisper import check_and_create_directories, initialize_csv, process_urls
from cleanIndex import index_content, search_indexed

def main():
    # Load the YouTube API key from a file. You'll need this and cookies.txt in a directory called secrets
    API_KEY = load_secret_from_file("secrets/api_key.txt")
    youtube = build('youtube', 'v3', developerKey=API_KEY)
    
    # Write all info of all videos uploaded by JermaStreamArchive to a CSV file. Uses JermaStreamArchive's Channel ID
    #write_videos_to_csv(youtube, "UC2oWuUSd3t3t5O3Vxp4lgAA", "urlsAndDetails.csv")

    # Compare directories to CSV and identify discrepancies
    #compare_directories_to_csv()

    # Generate a txt containing missing URLs
    #generate_missing_urls_file()
    #check_and_create_directories()
    #initialize_csv()

    # Transcribe missing videos
    #process_urls()

    # Index content for fast searching. It'll take a while the first time you run it then it's fast.
    index_content()

    # Search within the indexed content. Input gets cleaned and tokenized so you can use punctuation and vArIouS capitalization.
    search_indexed("Crack time!")

if __name__ == "__main__":
    main()
