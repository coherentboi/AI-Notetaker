import os
from dotenv import load_dotenv
import whisper

def write_transcription_to_file(transcription, output_file_path=os.path.join("speech", "transcript.txt")):
    
    if os.path.exists(output_file_path):
        os.remove(output_file_path)

    """
    Write the transcription text to a specified file.
    Defaults to 'transcript.txt' if no file path is specified.
    """
    with open(output_file_path, 'w') as file:
        file.write(transcription)
    print(f"Transcription has been written to {output_file_path}")

def transcribe_audio():
    filename = os.path.join("speech", "output.mp3")

    if not os.path.exists(filename):
        return

    # Load environment variables from .env file
    load_dotenv()

    # Retrieve the API key from environment variables
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key is None:
        raise ValueError("API key not found. Please check your .env file.")
    
    # Load the model
    model = whisper.load_model("base")  # You can select other models like 'tiny', 'small', 'medium', or 'large'

    # Load the audio file and transcribe it
    result = model.transcribe(filename)
    write_transcription_to_file(result['text'])

