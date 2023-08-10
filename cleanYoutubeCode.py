import csv
import re
from googleapiclient.discovery import build

def load_secret_from_file(filename):
    with open(filename, "r") as file:
        return file.read().strip()

def extract_video_id(url):
    """Extract video ID from YouTube URL."""
    match = re.match(r'https?://(?:www\.)?youtube\.com/watch\?v=([\w-]+)', url)
    return match.group(1) if match else None

def get_video_details(youtube, video_id):
    """Fetch title, duration, upload date, and description."""
    request = youtube.videos().list(part="snippet,contentDetails", id=video_id)
    response = request.execute()

    items = response.get("items", [])
    if items:
        title = items[0]["snippet"]["title"]
        duration = items[0]["contentDetails"]["duration"]
        upload_date = items[0]["snippet"]["publishedAt"]
        return title, duration, upload_date
    return None, None, None

def get_channel_videos(youtube, channel_id):
    res = youtube.channels().list(id=channel_id, part="contentDetails").execute()
    playlist_id = res["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

    videos = []
    next_page_token = None

    while True:
        res = (
            youtube.playlistItems()
            .list(
                playlistId=playlist_id,
                part="snippet",
                maxResults=50,
                pageToken=next_page_token,
            )
            .execute()
        )
        videos += res["items"]
        next_page_token = res.get("nextPageToken")

        if next_page_token is None:
            break

    return videos

def recursive_clean(s):
    """Recursively clean the string."""
    new_s = s.replace("/", " ").replace(",", " ").replace("  ", " ")
    if new_s == s:
        return s
    return recursive_clean(new_s)

def write_videos_to_csv(youtube, channel_id, output_filename):
    videos = get_channel_videos(youtube, channel_id)
    with open(output_filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Title", "URL","Duration", "Upload Date", "VideoID"])  # Headers

        for video in videos:
            video_url = f"https://www.youtube.com/watch?v={video['snippet']['resourceId']['videoId']}"
            video_id = extract_video_id(video_url)
            if video_id:
                title, duration, upload_date = get_video_details(youtube, video_id)
                title = recursive_clean(title)
                
                writer.writerow([title, video_url, upload_date, duration, video_id])
                print("wrote: " + title + " to csv")

if __name__ == "__main__":
    API_KEY = load_secret_from_file("secrets/api_key.txt")
    youtube = build('youtube', 'v3', developerKey=API_KEY)
    write_videos_to_csv(youtube, "UC2oWuUSd3t3t5O3Vxp4lgAA", "urlsAndDetails.csv")
