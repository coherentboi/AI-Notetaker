import pyaudio
import wave
import os
import threading
from pydub import AudioSegment
import time

def convert_wav_to_mp3(wav_filename, mp3_filename, bitrate="192k"):
    # Load the WAV file
    audio = AudioSegment.from_file(wav_filename, format="wav")
    # Convert it to MP3
    audio.export(mp3_filename, format="mp3", bitrate=bitrate)
    print("Conversion complete: {} has been created.".format(mp3_filename))

def record_audio():
    chunk = 1024
    sample_format = pyaudio.paInt16  # 16 bits per sample
    channels = 1
    sample_rate = 16000  # 16 kHz
    wavFilename = os.path.join("speech","output.wav")

    # Ensure previous recordings are removed
    if os.path.exists(wavFilename):
        os.remove(wavFilename)
        print(f"Previous file {wavFilename} removed.")
    
    mp3Filename = os.path.join("speech", "output.mp3")

    if os.path.exists(mp3Filename):
        os.remove(mp3Filename)
        print("Previous file output.mp3 removed.")

    p = pyaudio.PyAudio()  # Create an interface to PortAudio

    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=sample_rate,
                    frames_per_buffer=chunk,
                    input=True)

    frames = []  # Initialize array to store frames
    stop_recording = threading.Event()

    def stop():
        input("Recording started. Press Enter to stop.")
        stop_recording.set()

    threading.Thread(target=stop).start()

    try:
        while not stop_recording.is_set():
            data = stream.read(chunk)
            frames.append(data)
    except KeyboardInterrupt:
        print('Recording stopped by user')

    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    # Terminate the PortAudio interface
    p.terminate()

    print('Finished recording')

    # Save the recorded data as a WAV file
    wf = wave.open(wavFilename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(sample_rate)
    wf.writeframes(b''.join(frames))
    wf.close()

    # Convert wav to mp3
    convert_wav_to_mp3(wavFilename, mp3Filename)
