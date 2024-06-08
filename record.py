import pyaudio
import wave
import keyboard
import os
import time
import imageio_ffmpeg as ffmpeg
from pydub import AudioSegment

def convert_wav_to_mp3(wav_filename, mp3_filename, bitrate="192k"):
    # Load your WAV file
    audio = AudioSegment.from_file(wav_filename, format="wav")
    
    # Convert it to MP3
    audio.export(mp3_filename, format="mp3", bitrate=bitrate)

def wait_for_file(filename, timeout=3600):
    """Wait for a file to exist within a timeout period."""
    start_time = time.time()
    while True:
        if os.path.exists(filename):
            print(f"File {filename} exists.")
            return True
        elif (time.time() - start_time) > timeout:
            print(f"Waiting for file {filename} timed out.")
            return False
        else:
            print(f"Waiting for file {filename}...")
            time.sleep(5)  # Check every 5 seconds

def record_audio():
    chunk = 1024
    sample_format = pyaudio.paInt16
    channels = 1
    sample_rate = 16000
    filename = "output.wav"

    if os.path.exists(filename):
        os.remove(filename)

    p = pyaudio.PyAudio()

    # Wait for 'q' to start recording
    print('Press "q" to start recording')
    keyboard.wait('q')
    print('Recording started. Press "q" again to stop.')

    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=sample_rate,
                    frames_per_buffer=chunk,
                    input=True)

    frames = []

    try:
        while True:
            data = stream.read(chunk)
            frames.append(data)
            if keyboard.is_pressed('q'):
                print('Ending recording')
                while keyboard.is_pressed('q'):
                    # Wait for key release to ensure it doesn't trigger multiple stops
                    pass
                break
    except KeyboardInterrupt:
        print('Recording stopped')
    except Exception as e:
        print(f'Error: {e}')

    stream.stop_stream()
    stream.close()
    p.terminate()

    print('Finished recording')

    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(sample_rate)
    wf.writeframes(b''.join(frames))
    wf.close()

    wait_for_file("output.wav")
    convert_wav_to_mp3("output.wav", "output.mp3")


record_audio()
