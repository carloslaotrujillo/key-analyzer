# key-analyzer

#### This script analyzes the key of an audio file. It accepts an MP3 file as input, converts it to WAV format, and determines the key using various audio features.

Requires ffmpeg to be installed on your system. You can install it using the following command:

Linux:
```bash
sudo apt install ffmpeg 
```

MacOS:
```bash
brew install ffmpeg
```

## Usage
```python
./dist/analyze_audio path/to/audio.mp3
```

## Script Details
The script performs the following steps:

- Converts the input MP3 file to WAV format.
- Loads the audio file and separates harmonic content using Harmonic Percussive Source Separation (HPSS).
- Extracts various audio features including Chroma, Harmonic Pitch Class Profile (HPCP), and Tonnetz.
- Determines the key by comparing extracted features with predefined major and minor scale patterns.
- Deletes the temporary WAV file after analysis.

## Set Up a Virtual Environment:
```python
python3 -m venv env
source env/bin/activate
```

## Install Dependencies:
```python
pip install -r requirements.txt
```
## Build the Executable:
```python
pyinstaller --onefile analyze_audio.py
```

## Run the Executable:
```python
./dist/analyze_audio path/to/audio.mp3
```
