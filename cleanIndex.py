import os
import string
import re
from nltk.tokenize import word_tokenize
import nltk
from whoosh.fields import Schema, TEXT, ID
from whoosh.index import create_in, open_dir
from whoosh.qparser import QueryParser
from whoosh.writing import AsyncWriter

from utils import extract_title_to_url_mapping, timestamp_to_seconds
# Configuration dictionary
CONFIG = {
    "index_dir": "index_dirWithTimestamps_final",
    "txt_directory": "outDirectories",
    "schema": Schema(file_path=ID(stored=True), content=TEXT, timestamp=TEXT(stored=True)),
    "INDEXED_FILES_LIST":"indexed_files.txt",
}

def search_indexed(query_str):
    query_str = clean_and_tokenize_text(query_str)
    ix = open_dir(CONFIG["index_dir"])
    
    with ix.searcher() as searcher:
        query = QueryParser("content", CONFIG["schema"]).parse(query_str)
        results = searcher.search(query, limit=100)
        
        title_to_urls = extract_title_to_url_mapping()
        
        for hit in results:
            # Using os.path to handle file paths in a platform-independent way
            relative_path = os.path.relpath(hit['file_path'], CONFIG["txt_directory"])
            
            # Trim the "transcription.txt" part
            title_key = os.path.join(*relative_path.split(os.path.sep)[:-1])
            
            
            url = title_to_urls.get(title_key, "URL not found")
            
            # Extract the start time from the timestamp
            start_time = hit['timestamp'].split(' -> ')[0]
            start_seconds = timestamp_to_seconds(start_time)

            # Append the start time to the URL
            timestamped_url = f"{url}&t={start_seconds}s"
            print(f"Found in: {hit['file_path']} during {hit['timestamp']}")
            
            print(f"URL: {timestamped_url}")


def create_or_open_index(index_dir):
    if not os.path.exists(index_dir):
        os.makedirs(index_dir)
        print(f"Created new index directory: {index_dir}")
        # Ensure indexed_files.txt is empty
        with open(CONFIG["INDEXED_FILES_LIST"], 'w',encoding="utf-8") as f:
            pass  # This will create or truncate the file to be empty
        return create_in(index_dir, CONFIG["schema"])
    else:
        print(f"Opening existing index directory: {index_dir}")
        return open_dir(index_dir)

def add_file_to_index(file_path, writer, searcher):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    timestamped_content = extract_timestamps_and_content(content)
    for timestamp, normalized_content in timestamped_content:
        if not document_exists(file_path, timestamp, searcher):
            writer.add_document(file_path=file_path, content=normalized_content, timestamp=timestamp)
            print(f"Indexed segment with timestamp {timestamp} from file: {file_path}")

def document_exists(file_path, timestamp, searcher):
    return searcher.document(file_path=file_path, timestamp=timestamp) is not None

def extract_timestamps_and_content(text):
    segments = re.findall(r'\[(\d+\.\d+s -> \d+\.\d+s)\]  (.+?)\n', text)
    timestamped_content = [(t, clean_and_tokenize_text(c)) for t, c in segments]
    return timestamped_content

def clean_and_tokenize_text(text):
    text = text.lower().translate(str.maketrans('', '', string.punctuation))
    tokens = word_tokenize(text)
    return ' '.join(tokens)


def get_indexed_files():
    """
    Fetch the list of indexed files.
    """
    if os.path.exists(CONFIG["INDEXED_FILES_LIST"]):
        with open(CONFIG["INDEXED_FILES_LIST"], 'r', encoding='utf-8') as f:
            return f.read().splitlines()
    return []


def mark_as_indexed(file_path):
    """
    Mark a file as indexed by appending its path to the indexed files list.
    """
    with open(CONFIG["INDEXED_FILES_LIST"], 'a',encoding="utf-8") as f:
        f.write(file_path + "\n")

def index_file(file_path, writer, searcher):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    timestamped_content = extract_timestamps_and_content(content)
    for timestamp, normalized_content in timestamped_content:
        if not document_exists(file_path, timestamp, searcher):
            writer.add_document(file_path=file_path, content=normalized_content, timestamp=timestamp)
            print(f"Indexed segment with timestamp {timestamp} from file: {file_path}")
    mark_as_indexed(file_path)
def do_installs():
    nltk.download('punkt')
def index_content():
    do_installs()
    print(f"Indexing content from directory: {CONFIG['txt_directory']}")
    ix = create_or_open_index(CONFIG["index_dir"])
    writer = AsyncWriter(ix)

    indexed_files = get_indexed_files()

    with ix.searcher() as searcher:
        for root, _, files in os.walk(CONFIG["txt_directory"]):
            for file in files:
                full_path = os.path.join(root, file)
                if file == 'transcription.txt' and full_path not in indexed_files:
                    index_file(full_path, writer, searcher)
    print("Indexing complete. Committing...")
    writer.commit()
    print("Done")

if __name__ == "__main__":
    # Uncomment the next line if you're indexing for the first time or adding new files
    # index_content()
    search_indexed("crack time")
