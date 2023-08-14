import os
import csv
import shutil
# Constants
INDEX_DIR = "index_dirWithTimestamps_final"
URLS_DETAILS_CSV = "urlsAndDetails.csv"
COMPARISONS_CSV = "downloadComparisons.csv"
TXT_DIRECTORY= "outDirectories"

# Constants
INDEX_DIR = "index_dirWithTimestamps_final"
URLS_DETAILS_CSV = "urlsAndDetails.csv"
COMPARISONS_CSV = "downloadComparisons.csv"
TXT_DIRECTORY = "outDirectories"

def recursive_clean(s):
    """Recursively clean the string."""
    new_s = s.replace("/", " ").replace(",", " ").replace("  ", " ")
    if new_s == s:
        return s
    return recursive_clean(new_s)

def clean_and_rename_directory(dir_path):
    """Clean the directory name and rename if necessary."""
    original_name = os.path.basename(dir_path)
    cleaned_name = recursive_clean(original_name)

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
        print("Printing Discrepancies: ")
        for dir_tuple in missing_in_csv:
            print("in dir: " + dir_tuple[1])
            writer.writerow(["In Dir:", dir_tuple[1]])  # dir_tuple[1] contains the full path
            
        for title in missing_in_dir:
            writer.writerow(["In CSV:", title])
            print(title + "  in csv")

def recursive_traverse(dir_path, full_name, processed_directories):
    """Recursively traverse directories to find the transcription.txt file and the accumulated full name."""
    if 'transcription.txt' in os.listdir(dir_path):
        return dir_path, full_name

    for sub_dir_name in os.listdir(dir_path):
        sub_dir_path = os.path.join(dir_path, sub_dir_name)
        if os.path.isdir(sub_dir_path):
            new_full_name = full_name + " " + sub_dir_name.replace('/', ' ')
            result_path, result_name = recursive_traverse(sub_dir_path, new_full_name, processed_directories)
            if result_path:
                processed_directories.add(sub_dir_path)
                return result_path, result_name

    return None, None

def fix_stacked_directories():
    base_path = TXT_DIRECTORY
    processed_directories = set()

    for dir_name in os.listdir(base_path):
        dir_path = os.path.join(base_path, dir_name)
        if os.path.isdir(dir_path):
            transcription_path, full_name = recursive_traverse(dir_path, dir_name, processed_directories)
            full_name = recursive_clean(full_name)
            if transcription_path:
                full_path = os.path.join(base_path, full_name)
                if not os.path.exists(full_path):
                    os.makedirs(full_path)

                shutil.move(os.path.join(transcription_path, 'transcription.txt'), os.path.join(full_path, 'transcription.txt'))

    # Only delete empty directories from the list of processed directories
    safe_delete(processed_directories, base_path)

def safe_delete(processed_directories, base_path):
    """Safely delete only empty directories from the processed_directories list."""
    for dir_path in processed_directories:
        while dir_path.startswith(base_path):
            if os.path.exists(dir_path) and not os.listdir(dir_path):
                os.rmdir(dir_path)
                dir_path = os.path.dirname(dir_path)
            else:
                break

def copy_nested_directories(source_base=TXT_DIRECTORY, dest_base='outDirTest'):
    """Copy nested directories from source_base to dest_base."""
    for dir_name in os.listdir(source_base):
        dir_path = os.path.join(source_base, dir_name)
        dest_path = os.path.join(dest_base, dir_name)

        if os.path.isdir(dir_path) and any(os.path.isdir(os.path.join(dir_path, sub_name)) for sub_name in os.listdir(dir_path)):
            shutil.copytree(dir_path, dest_path)

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
        print("Printing Discrepancies: ")
        for dir_tuple in missing_in_csv:
            print("in dir: " + dir_tuple[1])
            writer.writerow(["In Dir:", dir_tuple[1]])  # dir_tuple[1] contains the full path
            
        for title in missing_in_dir:
            writer.writerow(["In CSV:", title])
            print(title + "  in csv")
if __name__ == "__main__":
    compare_directories_to_csv()
    generate_missing_urls_file()
