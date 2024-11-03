import os
import sys
from itertools import combinations
from scipy.io import wavfile
import numpy as np

def make_mono(wav_path):
    """Convert a wav file to mono by averaging its channels."""
    try:
        sample_rate, data = wavfile.read(wav_path)
    except ValueError as e:
        print(f"Error reading {wav_path}: {e}")
        return None, None  # Return None for invalid files

    # Check if the file is already mono
    if len(data.shape) == 1:
        return data, sample_rate

    # If stereo, average the channels to make mono
    mono_data = data.mean(axis=1).astype(data.dtype)
    return mono_data, sample_rate

def pad_to_match_length(wav1_mono, wav2_mono):
    """Pad the shorter array with zeros to match the length of the longer array."""
    max_len = max(len(wav1_mono), len(wav2_mono))
    
    if len(wav1_mono) < max_len:
        wav1_mono = np.pad(wav1_mono, (0, max_len - len(wav1_mono)), 'constant')
    if len(wav2_mono) < max_len:
        wav2_mono = np.pad(wav2_mono, (0, max_len - len(wav2_mono)), 'constant')
    
    return wav1_mono, wav2_mono

def merge_to_stereo(wav1_mono, wav2_mono):
    """Merge two mono audio arrays into a stereo array."""
    wav1_mono, wav2_mono = pad_to_match_length(wav1_mono, wav2_mono)
    return np.column_stack((wav1_mono, wav2_mono))

def make_mono_and_merge(wav1_path, wav2_path, output_folder):
    # Convert both audio files to mono
    wav1_mono, sample_rate1 = make_mono(wav1_path)
    wav2_mono, sample_rate2 = make_mono(wav2_path)

    if wav1_mono is None or wav2_mono is None:
        print(f"Skipping merge due to invalid files: {wav1_path}, {wav2_path}")
        return

    # Interleave the two mono files into a stereo file
    stereo_data = merge_to_stereo(wav1_mono, wav2_mono)

    # Create output filename based on input filenames
    base1 = os.path.splitext(os.path.basename(wav1_path))[0]
    base2 = os.path.splitext(os.path.basename(wav2_path))[0]
    output_filename = f"{base1}_{base2}_merged.wav"
    output_path = os.path.join(output_folder, output_filename)

    # Write the output file
    wavfile.write(output_path, sample_rate1, stereo_data)
    print(f"Created {output_path}")

def main(source_folder, target_folder):
    # Check if source and target folders exist
    if not os.path.isdir(source_folder):
        print(f"Source folder '{source_folder}' does not exist.")
        return
    if not os.path.isdir(target_folder):
        os.makedirs(target_folder)
    
    # Get all wav files in the source folder
    wav_files = [f for f in os.listdir(source_folder) if f.endswith('.wav')]
    
    # Process each combination of 2 files
    for wav1, wav2 in combinations(wav_files, 2):
        wav1_path = os.path.join(source_folder, wav1)
        wav2_path = os.path.join(source_folder, wav2)
        make_mono_and_merge(wav1_path, wav2_path, target_folder)

if __name__ == "__main__":
    # Check if the correct number of arguments are provided
    if len(sys.argv) != 3:
        print("Usage: python script.py <source_folder> <target_folder>")
    else:
        source_folder = sys.argv[1]
        target_folder = sys.argv[2]
        main(source_folder, target_folder)
