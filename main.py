import os
from pydub import AudioSegment
from pytube import YouTube

def download_music(url):
    print("Downloading music from YouTube...")
    yt = YouTube(url)
    video = yt.streams.filter(only_audio=True).first()
    download_path = video.download()
    
    # Attempt to convert to MP3 using pydub
    try:
        audio = AudioSegment.from_file(download_path)
        mp3_path = download_path.rsplit('.', 1)[0] + '.mp3'
        audio.export(mp3_path, format='mp3')
        os.remove(download_path)  # Remove the original download
        print(f"Downloaded and converted to MP3 as {mp3_path}")
        return mp3_path
    except Exception as e:
        print(f"Failed to convert to MP3: {e}")
        print(f"Downloaded without conversion as {download_path}")
        return download_path

def modify_audio(file_path):
    file_format = 'mp3'  # Assume MP3 format after conversion
    audio = AudioSegment.from_file(file_path, format=file_format)
    octaves = 0.3
    new_sample_rate = int(audio.frame_rate * (2.0 ** octaves))
    audio = audio._spawn(audio.raw_data, overrides={'frame_rate': new_sample_rate})
    audio = audio.set_frame_rate(45100)
    modified_file_path = file_path.replace(".mp3", "_modified.mp3")
    audio.export(modified_file_path, format="mp3")
    print("Modified audio exported successfully.")

def list_audio_files(directory):
    audio_extensions = ['.mp3', '.wav', '.m4a', '.aac', '.flac']
    audio_files = [f for f in os.listdir(directory) if any(f.endswith(ext) for ext in audio_extensions)]
    return audio_files

def clear_directory(directory):
    audio_files = list_audio_files(directory)
    for file in audio_files:
        file_path = os.path.join(directory, file)
        os.remove(file_path)
        print(f"Deleted {file_path}")
    print("All music files have been cleared from the directory.")

def main_menu():
    ascii_art = """

 _____                     _ _   _       _____                  ___  ___      _             
/  ___|                   | | | | |     /  ___|                 |  \/  |     | |            
\ `--. _ __   ___  ___  __| | | | |_ __ \ `--.  ___  _ __   __ _| .  . | __ _| | _____ _ __ 
 `--. \ '_ \ / _ \/ _ \/ _` | | | | '_ \ `--. \/ _ \| '_ \ / _` | |\/| |/ _` | |/ / _ \ '__|
/\__/ / |_) |  __/  __/ (_| | |_| | |_) /\__/ / (_) | | | | (_| | |  | | (_| |   <  __/ |   
\____/| .__/ \___|\___|\__,_|\___/| .__/\____/ \___/|_| |_|\__, \_|  |_/\__,_|_|\_\___|_|   
      | |                         | |                       __/ |                           
      |_|                         |_|                      |___/                            

                                                                                   
"""
    print(ascii_art)
    choice = input("Choose an option:\n1. Download music from YouTube\n2. Speed up music\n3. Clear directory\n4. Exit\nEnter your choice (1, 2, 3, or 4): ")
    return choice


def choose_file_to_modify(directory):
    audio_files = list_audio_files(directory)
    if not audio_files:
        print("No audio files found in the directory.")
        return None
    print("Audio files found:")
    for i, file in enumerate(audio_files, start=1):
        print(f"{i}. {file}")
    print(f"{len(audio_files) + 1}. Back to menu")
    choice = int(input("Enter the number of the audio file you want to modify, or go back to menu: ")) - 1
    if 0 <= choice < len(audio_files):
        return os.path.join(directory, audio_files[choice])
    return None

def main():
    while True:
        user_choice = main_menu()
        if user_choice == '1':
            youtube_url = input("Enter the YouTube URL: ")
            downloaded_file = download_music(youtube_url)
            speed_up = input("Do you want to speed up the downloaded music? (yes/no): ")
            if speed_up.lower() == 'yes':
                modify_audio(downloaded_file)
        elif user_choice == '2':
            directory = os.path.dirname(os.path.abspath(__file__))
            file_path = choose_file_to_modify(directory)
            if file_path:
                modify_audio(file_path)
        elif user_choice == '3':
            clear_directory(directory)
        elif user_choice == '4':
            print("Exiting...")
            break
        else:
            print("Invalid option. Please choose 1, 2, 3, or 4.")

if __name__ == "__main__":
    main()
