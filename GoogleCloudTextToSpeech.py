#!/usr/bin/env python
import argparse
from google.cloud import texttospeech

def text_to_speech(text_file):
    client = texttospeech.TextToSpeechClient()
    
    with open(text_file, 'r') as file:
        text = file.read()
        input_text = texttospeech.types.SynthesisInput(text=text)
        
    voice = texttospeech.types.VoiceSelectionParams(language_code='en-US', ssml_gender=texttospeech.enums.SsmlVoiceGender.MALE)
    audio_config = texttospeech.types.AudioConfig(audio_encoding=texttospeech.enums.AudioEncoding.MP3)
    response = client.synthesize_speech(input_text, voice, audio_config)
    
    with open('weather.mp3', 'wb') as out:
        out.write(response.audio_content)
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__,formatter_class=argparse.RawDescriptionHelpFormatter)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--text',
                       help='The text file from which to synthesize speech.')

    args = parser.parse_args()

    if args.text:
        text_to_speech(args.text)