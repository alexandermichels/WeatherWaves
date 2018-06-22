#!/usr/bin/env python
from __future__ import absolute_import
import json, vlc, urllib2, time, sys
from io import open
from gtts import gTTS
from google.cloud import texttospeech
from google.oauth2 import service_account
from weatherwaves.WeatherConnector import *

class WeatherReporter(object):

    mp3_filename = u"weather.mp3"
    
    def __init__(self, state, city, key_file = None, weather_key = None):
        if (key_file == None and weather_key == None):
            pass
        elif (weather_key == None):
            self.weather_connector = WeatherConnector(filename = key_file)
        elif (key_file == None):
            self.weather_connector = WeatherConnector(api_key = weather_key)
        
        self.state = state
        self.city = city
        self.get_conditions()
        self.get_forecast()
    
    def __str__(self):
        return self.key
    
    def format_string(self, string):
        string = string.replace(u"F.", u".").replace("Low", "Low of").replace("High", "High of").replace("Cloudy", "cloudy")
        string = string.replace("cloudy", "cloudy skies")
        string = string.replace("skies skies", "skies")
        dirAbr = [ u' N ', u' E ', u' S ', u' W ', u' NW ', u' NE ', u' SW ', u' SE ', u' NNE ', u' ENE ', u' ESE ', u' SSE ', u' SSW ', u' WSW ', u' WNW ', u' NNW ']
        dirStr = [ u' North ', u' East ', u' South ', u' West ', u' Northwest ', u' Northeast ', u' Southwest ', u' Southeast ', u' North Northeast ', u' East Northeast ', u' East Southeast ', u' South Southeast ', u' South Southwest ', u' West Southwest ', u' West Northwest ', u' North Northwest ']
        for i in xrange(0, len(dirAbr)):
            string = string.replace(dirAbr[i], dirStr[i])
        return string
    
    def format_string_wind(self, string):
        orig = string
        ind = string.find(" Winds")
        string = string[ind:string.find(".",ind)+1]
        if string == ".":
            return orig
        for i in range(3,9):
            if (str(i) in string):
                if i == 5 and i in [5,15,25]:
                    pass
                else:
                    return orig
        return orig.replace(string,"")
        
    def get_conditions(self):
        try:
            self.curr_json = self.weather_connector.get_conditions(state = self.state, city = self.city)
            return self.curr_json
        except:
            time.sleep(.1)
            return self.weather_connector.get_conditions(state = self.state, city = self.city)
            
    def get_report_mp3(self):
        try:
            SCOPES = ['https://www.googleapis.com/auth/cloud-platform']
            SERVICE_ACCOUNT_FILE = 'GoogleKey.json'
            credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
            client = texttospeech.TextToSpeechClient(credentials=credentials)
            input_text = texttospeech.types.SynthesisInput(text=self.get_report_string())
            voice = texttospeech.types.VoiceSelectionParams(language_code=u'en-US', ssml_gender=texttospeech.enums.SsmlVoiceGender.MALE)
            audio_config = texttospeech.types.AudioConfig(audio_encoding=texttospeech.enums.AudioEncoding.MP3)
            response = client.synthesize_speech(input_text, voice, audio_config)
            
            with open(self.mp3_filename, 'wb') as out:
                out.write(response.audio_content)
                
        except:
            tts = gTTS(text = self.get_report_string(), lang="en")
            tts.save(self.mp3_filename)
        
    def get_conditions_string(self):
        if (abs(self.get_curr_temp() - self.get_curr_feels_like()) > 5):
            return self.format_string_wind(u"{} area weather, it is currently {}, but feels like {}, and it is {}.".format(self.city.replace("_", " "), self.get_curr_temp(), self.get_curr_feels_like(), self.get_curr_weather()))
        else:
            return self.format_string_wind(u"{} area weather, it is currently {} and it is {}.".format(self.city.replace("_", " "), self.get_curr_temp(), self.get_curr_weather()))
        
    def get_curr_feels_like(self):
        return int(float(self.curr_json[u"current_observation"][u"feelslike_f"]))

    def get_curr_temp(self):
        return int(float(self.curr_json[u"current_observation"][u'temp_f']))
        
    def get_curr_weather(self):
        return self.curr_json[u"current_observation"][u'weather']
        
    def get_forecast(self):
        try:
            self.fore_json = self.weather_connector.get_forecast(state = self.state, city = self.city)
            return self.fore_json
        except:
            time.sleep(.1)
            return self.weather_connector.get_forecast(state = self.state, city = self.city)
    
    def get_forecast_next_step(self):
        return self.fore_json[u"forecast"][u"txt_forecast"][u"forecastday"][1]
    
    def get_forecast_next_step_string(self):
        s = self.get_forecast_next_step()
        return self.format_string_wind(u"{} you should expect {}".format(s[u'title'], s[u'fcttext']))
    
    def get_forecast_two_steps(self):
        return self.fore_json[u"forecast"][u"txt_forecast"][u"forecastday"][2]
        
    def get_forecast_two_steps_string(self):
        s = self.get_forecast_two_steps()
        return self.format_string_wind(u"{} you should expect {}".format(s[u'title'], s[u'fcttext']))
        
    def get_forecast_weekend_string(self):
        i = 1
        s = self.get_conditions_string()
        while((("Friday" in self.fore_json["forecast"]["txt_forecast"]["forecastday"][i][u'title']) or ("Saturday" in self.fore_json[u"forecast"][u"txt_forecast"][u"forecastday"][i][u'title']) or ("Sunday" in self.fore_json[u"forecast"][u"txt_forecast"][u"forecastday"][i][u'title']))):
            s = s + self.format_string_wind(u" {} you should expect {}".format(self.fore_json[u"forecast"][u"txt_forecast"][u"forecastday"][i][u'title'], self.fore_json[u"forecast"][u"txt_forecast"][u"forecastday"][i][u'fcttext']))
            i = i+1
        return s
        
    def get_report_string(self):
        if self.is_weekend():
            return self.format_string(self.get_forecast_weekend_string())
        elif self.is_night():
            s = u"{} {}".format(self.get_conditions_string(), self.get_forecast_next_step_string())
            return self.format_string(s)
        else:
            s = u"{} {} {}".format(self.get_conditions_string(), self.get_forecast_next_step_string(), self.get_forecast_two_steps_string())
            return self.format_string(s)
    
    def is_night(self):
        return ("night" in self.fore_json[u"forecast"][u"txt_forecast"][u"forecastday"][0][u"title"])
    
    def is_weekend(self):
        return (("Friday" in self.fore_json[u"forecast"][u"txt_forecast"][u"forecastday"][0][u"title"]) or ("Saturday" in self.fore_json[u"forecast"][u"txt_forecast"][u"forecastday"][0][u"title"]))

    def print_curr_json(self):
        print json.dumps(self.curr_json, sort_keys = True, indent = 4)
    
    def print_fore_json(self):
        print json.dumps(self.fore_json, sort_keys = True, indent = 4)
        
    def read_mp3(self):
        vlc.MediaPlayer(self.mp3_filename).play()
        
    def write_all(self):
        self.write_curr_json()
        self.write_fore_json()
        self.write_report_string()
        
    def write_curr_json(self):
        f = open("curr_json.txt", "w")
        f.write(json.dumps(self.curr_json, sort_keys=True, indent=4, separators=(',', ': ')).decode('latin1'))
        f.close()
        
    def write_fore_json(self):
        f = open("fore_json.txt", "w")
        f.write(json.dumps(self.fore_json, sort_keys=True, indent=4, separators=(',', ': ')).decode('latin1'))
        f.close()
    
    def write_report_string(self):
        f = open("weather.txt", "w")
        f.write(self.get_report_string())
        f.close()
        
def main():
    reporter = WeatherReporter(u'PA', u'New_Wilmington', key_file = u'WeatherUndergroundAPIKey')
    reporter.get_report_mp3()
    reporter.write_all()
    reporter.read_mp3()
    
    
if __name__ == u"__main__" :
    main()
