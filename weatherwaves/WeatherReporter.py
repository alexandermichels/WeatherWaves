#!/usr/bin/env python
from __future__ import absolute_import
import json, vlc, urllib2, time, sys
from io import open
from gtts import gTTS
from google.cloud import texttospeech
from google.oauth2 import service_account
from WeatherConnector import *

class WeatherReporter(object):
    ''' severely out of date '''

    mp3_filename = u"weather.mp3"

    def __init__(self, state, city, google_API_key = None, weather_key_file = None, weather_key = None):
        if (weather_key_file == None and weather_key == None):
            pass
        elif (weather_key == None):
            self.weather_connector = WeatherConnector(filename = weather_key_file)
        elif (weather_key_file == None):
            self.weather_connector = WeatherConnector(api_key = weather_key)

        self.state = state
        self.city = city
        self.google_API_key = google_API_key
        self.get_conditions()
        self.get_forecast()

    def __str__(self):
        return self.key

    def get_report_mp3(self):
        try:
            client = texttospeech.TextToSpeechClient(credentials=service_account.Credentials.from_service_account_file(self.google_API_key, scopes= ['https://www.googleapis.com/auth/cloud-platform']))
            response = client.synthesize_speech(texttospeech.types.SynthesisInput(text=self.get_report_string()), texttospeech.types.VoiceSelectionParams(language_code=u'en-US', ssml_gender=texttospeech.enums.SsmlVoiceGender.MALE), texttospeech.types.AudioConfig(audio_encoding=texttospeech.enums.AudioEncoding.MP3))

            with open(self.mp3_filename, 'wb') as out:
                out.write(response.audio_content)

        except:
            tts = gTTS(text = self.get_report_string(), lang="en")
            tts.save(self.mp3_filename)


    def read_mp3(self):
        vlc.MediaPlayer(self.mp3_filename).play()


def main():
    reporter = WeatherReporter("PA", "New_Wilmington", google_API_key = "GoogleKey.json", weather_key_file = u'WeatherUndergroundAPIKey')
    reporter.get_report_mp3()
    reporter.write_all()
    reporter.read_mp3()


if __name__ == u"__main__" :
    main()
