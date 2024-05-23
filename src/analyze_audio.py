import argparse
import os
from pydub import AudioSegment
import numpy as np
import librosa
from scipy.ndimage import uniform_filter1d

def analyze_audio(file_path):
    # Convert mp3 to wav
    print("Converting MP3 to WAV...")
    audio = AudioSegment.from_mp3(file_path)
    wav_file_path = 'output.wav'
    audio.export(wav_file_path, format='wav')    

    # Load the audio file with librosa
    print("Loading audio file...")
    y, sr = librosa.load(wav_file_path)

    # Use HPSS to separate harmonic content
    print("Separating harmonic content...")
    y_harmonic, y_percussive = librosa.effects.hpss(y)

    # Extract chroma feature with longer window and smoothing
    print("Extracting chroma features...")
    chroma = librosa.feature.chroma_stft(y=y_harmonic, sr=sr, hop_length=512, n_fft=4096)
    chroma_mean = np.mean(chroma, axis=1)
    chroma_smoothed = uniform_filter1d(chroma_mean, size=3)

    # Extract HPCP (Harmonic Pitch Class Profile)
    print("Extracting HPCP features...")
    hpcp = librosa.feature.chroma_cqt(y=y_harmonic, sr=sr)
    hpcp_mean = np.mean(hpcp, axis=1)
    hpcp_smoothed = uniform_filter1d(hpcp_mean, size=3)

    # Extract Tonnetz features
    print("Extracting Tonnetz features...")
    tonnetz = librosa.feature.tonnetz(y=y_harmonic, sr=sr)
    tonnetz_mean = np.mean(tonnetz, axis=1)

    # Define major and minor scale patterns
    major_pattern = np.array([1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1])
    minor_pattern = np.array([1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0])

    # Function to determine the best matching key
    def get_best_key(chroma_smoothed, hpcp_smoothed, tonnetz_mean, major_pattern, minor_pattern):
        max_correlation = -1
        best_key = None
        best_scale = None
        notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        
        for i in range(12):
            rotated_major = np.roll(major_pattern, i)
            rotated_minor = np.roll(minor_pattern, i)
            
            # Calculate correlations
            chroma_major_correlation = np.corrcoef(chroma_smoothed, rotated_major)[0, 1]
            chroma_minor_correlation = np.corrcoef(chroma_smoothed, rotated_minor)[0, 1]
            hpcp_major_correlation = np.corrcoef(hpcp_smoothed, rotated_major)[0, 1]
            hpcp_minor_correlation = np.corrcoef(hpcp_smoothed, rotated_minor)[0, 1]
            tonnetz_major_correlation = np.corrcoef(tonnetz_mean, rotated_major[:len(tonnetz_mean)])[0, 1]
            tonnetz_minor_correlation = np.corrcoef(tonnetz_mean, rotated_minor[:len(tonnetz_mean)])[0, 1]
            
            # Average correlations
            major_correlation = np.mean([chroma_major_correlation, hpcp_major_correlation, tonnetz_major_correlation])
            minor_correlation = np.mean([chroma_minor_correlation, hpcp_minor_correlation, tonnetz_minor_correlation])
            
            if major_correlation > max_correlation:
                max_correlation = major_correlation
                best_key = notes[i]
                best_scale = "major"
            
            if minor_correlation > max_correlation:
                max_correlation = minor_correlation
                best_key = notes[i]
                best_scale = "minor"
        
        return best_key, best_scale

    # Determine the best key
    best_key, best_scale = get_best_key(chroma_smoothed, hpcp_smoothed, tonnetz_mean, major_pattern, minor_pattern)

    # Delete the temporary wav file
    if os.path.exists(wav_file_path):
        os.remove(wav_file_path)
        print(f"Deleted temporary file: {wav_file_path}")

    print(f"The best matching key is: {best_key} {best_scale}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Analyze the key of an audio file.')
    parser.add_argument('file_path', type=str, help='Path to the audio file')
    args = parser.parse_args()
    
    analyze_audio(args.file_path)
