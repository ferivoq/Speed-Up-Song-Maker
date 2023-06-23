from pydub import AudioSegment

def modify_audio(file_path):
    audio = AudioSegment.from_file(file_path, format="wav")

    octaves = 0.3
    new_sample_rate = int(audio.frame_rate * (2.0 ** octaves))
    audio = audio._spawn(audio.raw_data, overrides={'frame_rate': new_sample_rate})
    audio = audio.set_frame_rate(44100)

    modified_file_path = file_path.replace(".wav", "_modified.wav")
    audio.export(modified_file_path, format="wav")

    print("Modified audio exported successfully.")

file_path = input("Enter the name of the WAV file (with .wav): ")

modify_audio(file_path)