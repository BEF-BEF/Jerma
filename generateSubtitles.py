import os

def transcript_to_srt(transcript_text):
    entries = transcript_text.split('\n')
    srt_format = []

    counter = 1
    for entry in entries:
        if not entry.strip():
            continue
        if ']  ' not in entry:
            print(f"Warning: Skipping malformed entry - {entry}")
            continue

        times, text = entry.split(']  ', 1)
        if ' -> ' not in times:
            print(f"Warning: Skipping malformed time entry - {times}")
            continue
        start_time, end_time = times[1:].split(' -> ')
        
        start_time = format_time(float(start_time[:-1]))
        end_time = format_time(float(end_time[:-1]))
        
        srt_format.append(f"{counter}\n{start_time} --> {end_time}\n{text}\n")
        counter += 1

    return "\n".join(srt_format)


def format_time(seconds):
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02},{int((seconds % 1) * 1000):03}"

def convert_transcriptions_to_srt():
    base_path = "outDirectories"
    dest_base_path = "subtitleDirectories"

    # Ensure the subtitleDirectories exists
    if not os.path.exists(dest_base_path):
        os.makedirs(dest_base_path)

    for dir_name in os.listdir(base_path):
        dir_path = os.path.join(base_path, dir_name)

        # Check if the directory has a transcription.txt
        if os.path.isdir(dir_path) and 'transcription.txt' in os.listdir(dir_path):
            with open(os.path.join(dir_path, 'transcription.txt'), 'r') as f:
                transcript = f.read()
            print(dir_path)
            # Convert the transcript to SRT format
            srt_content = transcript_to_srt(transcript)

            # Ensure the directory exists in subtitleDirectories
            dest_dir = os.path.join(dest_base_path, dir_name)
            if not os.path.exists(dest_dir):
                os.makedirs(dest_dir)

            # Write to the new subtitle.srt file
            with open(os.path.join(dest_dir, 'subtitle.srt'), 'w') as f:
                f.write(srt_content)
