import os
import csv

# Constants
INDEX_DIR = "index_dirWithTimestamps_final"
URLS_DETAILS_CSV = "urlsAndDetails.csv"
COMPARISONS_CSV = "downloadComparisons.csv"
TXT_DIRECTORY= "outDirectories"
def clean_and_rename_directory(dir_path):
    """Clean the directory name and rename if necessary."""
    original_name = os.path.basename(dir_path)
    cleaned_name = original_name.replace(",", " ").replace("  ", " ")

    if original_name != cleaned_name:
        new_path = os.path.join(os.path.dirname(dir_path), cleaned_name)
        os.rename(dir_path, new_path)
        print("Renaming " + str(new_path) )
        return cleaned_name, new_path
    return original_name, dir_path

def collect_transcription_directories(directory=TXT_DIRECTORY):
    """Collect names of all folders containing transcription.txt and rename if necessary."""
    transcription_directories = []

    for root, _, files in os.walk(directory):
        for file in files:
            if file == 'transcription.txt':
                cleaned_name, cleaned_path = clean_and_rename_directory(root)
                transcription_directories.append((cleaned_name, cleaned_path))
                
    return transcription_directories

def extract_titles_from_csv(csv_path=URLS_DETAILS_CSV):
    """Extract video titles from the provided CSV."""
    titles = []

    with open(csv_path, 'r', encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)  # Skip the header
        for row in reader:
            titles.append(row[0])
    
    return titles

def compare_directories_to_csv():
    """Compare directory names to CSV titles and write discrepancies to downloadComparisons.csv."""
    
    transcription_directories = collect_transcription_directories()
    csv_titles = extract_titles_from_csv()

    # Extract directory names only (without full path)
    dir_names = [dir_tuple[0] for dir_tuple in transcription_directories]

    # Compare
    missing_in_csv = [dir_tuple for dir_tuple in transcription_directories if dir_tuple[0] not in csv_titles]
    missing_in_dir = [title for title in csv_titles if title not in dir_names]

    # Write to CSV
    with open(COMPARISONS_CSV, 'w', encoding="utf-8", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Discrepancy", "Details"])
        
        for dir_tuple in missing_in_csv:
            print(dir_tuple[1])
            writer.writerow(["In Dir:", dir_tuple[1]])  # dir_tuple[1] contains the full path
        for title in missing_in_dir:
            writer.writerow(["In CSV:", title])
            print(title + "  title")

def extract_missing_titles_from_comparisons(file_name="downloadComparisons.csv"):
    """Extract titles with 'In CSV:' discrepancy from the comparisons CSV."""
    missing_titles = []
    
    with open(file_name, 'r', newline='') as csv_file:
        reader = csv.reader(csv_file)
        next(reader)  # Skip header
        for row in reader:
            if row[0] == "In CSV:":
                missing_titles.append(row[1])
                
    return missing_titles
def timestamp_to_seconds(timestamp):
    """Convert a timestamp in the format X.Xs to seconds."""
    return int(float(timestamp[:-1]))

def extract_title_to_url_mapping(file_name="urlsAndDetails.csv"):
    """Create a dictionary with titles as keys and URLs as values."""
    title_to_url = {}
    
    with open(file_name, 'r', newline='') as csv_file:
        reader = csv.reader(csv_file)
        next(reader)  # Skip header
        for row in reader:
            title_to_url[row[0]] = row[1]  # Assuming Title is in the first column and URL in the fifth
            
    return title_to_url

def generate_missing_urls_file():
    missing_titles = extract_missing_titles_from_comparisons()
    title_to_url = extract_title_to_url_mapping()
    
    missing_urls = [title_to_url[title] for title in missing_titles if title in title_to_url]
    
    with open('missingURLS.txt', 'w') as f:
        for url in missing_urls:
            f.write(url + '\n')
    
    print(f"{len(missing_urls)} missing URLs have been written to missingURLS.txt")

if __name__ == "__main__":
    compare_directories_to_csv()
    generate_missing_urls_file()
