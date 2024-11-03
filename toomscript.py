import os
import sys
from itertools import combinations
import wave

def make_mono(wav_path):
    """Convert a wav file to mono by averaging its channels."""
    with wave.open(wav_path, 'rb') as wav_file:
        params = wav_file.getparams()
        sample_width = wav_file.getsampwidth()
        frame_rate = wav_file.getframerate()
        n_frames = wav_file.getnframes()
        n_channels = wav_file.getnchannels()
        frames = wav_file.readframes(n_frames)
    
    # If already mono, return the frames as-is
    if n_channels == 1:
        return frames, sample_width, frame_rate
    
    # Convert to mono by averaging channels
    mono_frames = bytearray()
    for i in range(0, len(frames), sample_width * n_channels):
        samples = [
            int.from_bytes(frames[i + j * sample_width: i + (j + 1) * sample_width], byteorder='little', signed=True)
            for j in range(n_channels)
        ]
        mono_sample = sum(samples) // n_channels
        mono_frames.extend(mono_sample.to_bytes(sample_width, byteorder='little', signed=True))
    
    return bytes(mono_frames), sample_width, frame_rate

def merge_to_stereo(wav1_mono, wav2_mono, sample_width):
    """Interleave two mono audio frames to create stereo audio."""
    stereo_frames = bytearray()
    for i in range(0, len(wav1_mono), sample_width):
        stereo_frames.extend(wav1_mono[i:i + sample_width])  # Left channel
        stereo_frames.extend(wav2_mono[i:i + sample_width])  # Right channel
    return bytes(stereo_frames)

def make_mono_and_merge(wav1_path, wav2_path, output_folder):
    # Convert both audio files to mono
    wav1_mono, sample_width1, frame_rate1 = make_mono(wav1_path)
    wav2_mono, sample_width2, frame_rate2 = make_mono(wav2_path)

    # Ensure compatibility
    if sample_width1 != sample_width2 or frame_rate1 != frame_rate2:
        print(f"Incompatible files: {wav1_path} and {wav2_path}. Skipping.")
        return

    # Interleave the two mono files into a stereo file
    stereo_frames = merge_to_stereo(wav1_mono, wav2_mono, sample_width1)

    # Create output filename based on input filenames
    base1 = os.path.splitext(os.path.basename(wav1_path))[0]
    base2 = os.path.splitext(os.path.basename(wav2_path))[0]
    output_filename = f"{base1}_{base2}_merged.wav"
    output_path = os.path.join(output_folder, output_filename)

    # Write the output file
    with wave.open(output_path, 'wb') as output:
        output.setnchannels(2)  # Stereo
        output.setsampwidth(sample_width1)
        output.setframerate(frame_rate1)
        output.writeframes(stereo_frames)
    
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

