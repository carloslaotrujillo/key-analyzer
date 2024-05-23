# key-analyzer

### This script analyzes the key of an audio file. It accepts an MP3 file as input, converts it to WAV format, and determines the key using various audio features.

* Requires ffmpeg to be installed.

## Script Details

The script performs the following steps:

- Converts the input MP3 file to WAV format.
- Loads the audio file and separates harmonic content using Harmonic Percussive Source Separation (HPSS).
- Extracts various audio features including Chroma, Harmonic Pitch Class Profile (HPCP), and Tonnetz.
- Determines the key by comparing extracted features with predefined major and minor scale patterns.
- Deletes the temporary WAV file after analysis.

## Usage 

```python
  ./analyze_audio path/to/audio.mp3
```

## Download the Executable

You can download the pre-built executable from the releases page.
