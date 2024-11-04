import os
import sys
from itertools import combinations
from scipy.io import wavfile
import numpy as np

def make_mono(wav_path):
    """Convert a wav file to mono by averaging its channels and normalize it."""
    try:
        sample_rate, data = wavfile.read(wav_path)
    except ValueError as e:
        print(f"Error reading {wav_path}: {e}")
        return None, None  # Return None for invalid files

    # Check if the file is already mono
    if len(data.shape) == 1:
        mono_data = data
    else:
        # If stereo, average the channels to make mono
        mono_data = data.mean(axis=1).astype(data.dtype)
    
    return mono_data, sample_rate

def normalize_audio(audio_data):
    """Normalize the audio data to make the peak amplitude reach the maximum possible value."""
    max_val = np.max(np.abs(audio_data))
    if max_val == 0:
        return audio_data  # Avoid division by zero if the data is silent
    return (audio_data / max_val * np.iinfo(audio_data.dtype).max).astype(audio_data.dtype)

def pad_to_match_length(wav1_mono, wav2_mono):
    """Pad the shorter array with zeros to match the length of the longer array."""
