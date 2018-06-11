#!/usr/bin/env python
from __future__ import absolute_import
import json, vlc, urllib2, urllib, time
from io import open
from gtts import gTTS
from google.cloud import texttospeech
from google.oauth2 import service_account

class WeatherReporter(object):
    u'''
    Simple class to interact with the WeatherUnderground API 
    
    gcloud auth application-default login    
    
    ---Instance Variables
    curr_json = the JSON of the current conditions
    fore_json = the JSON of the current forecast
    key = a string containing the API key
    mp3_filename = the file name of the MP3 file containing the weather report
    
    ---Methods
    __init__(filename) = takes a string, opens said file, and sets the key field as the read().strip() output
    __str__ = returns the key field
    format_string(string) = changes abbreviations
    get_conditions(state, city) = sends an HTTP GET request to get the current conditions at the location and decodes the JSON
    get_report_mp3() = creates and saves a report MP3 based on get_report_string() and sets mp3_filename to this file
    get_conditions_string() = returns a string with the current temp and weather conditions as well as feels like if abs of diff > 5
    get_curr_feels_like() = returns the current condition's feels like temperature
    get_curr_temp() = returns the current condition's temperature in Farenheit
    get_curr_weather() = returns the string with the current weather conditions (cloudy, rainy, etc.)
    get_forecast(state, city) = sends an HTTP GET request to get the current forecast at the location and decodes the JSON
    get_forecast_next_step() = returns a JSON of the next time step in the forecast
    get_forecast_next_step_string() = a string with the time steps's name and conditions
    get_forecast_two_steps() = returns a JSON of the forecast two time steps in the future
    get_forecast_two_steps_string() = returns a string with the name and conditions two time steps in the future
    get_report_string() = returns a formated (format_string()) string with current conditions, and the next two time step's forecasts
    print_curr_json() = prints the curr_json field
    print_fore_json() = prints the fore_json field
    read_mp3() = plays the MP3 in the mp3_filename field
    '''

    curr_json = u""
    fore_json = u""
    key = u""
    mp3_filename = u"weather.mp3"
    
    def __init__(self, filename, state, city):
        file = open(filename)
        self.key = file.read().strip()
        self.get_conditions(state,city)
        self.get_forecast(state,city)
    
    def __str__(self):
        return self.key
    
    def format_string(self, string):
        string = string.replace(u"F.", u".")
        string = string.replace("cloudy", "cloudy skies")
        string = string.replace("Cloudy", "cloudy skies")
        string = string.replace("High", "High of")
        string = string.replace("Low", "Low of")
        dirAbr = [ u' N ', u' E ', u' S ', u' W ', u' NW ', u' NE ', u' SW ', u' SE ', u' NNE ', u' ENE ', u' ESE ', u' SSE ', u' SSW ', u' WSW ', u' WNW ', u' NNW ']
        dirStr = [ u' North ', u' East ', u' South ', u' West ', u' Northwest ', u' Northeast ', u' Southwest ', u' Southeast ', u' North Northeast ', u' East Northeast ', u' East Southeast ', u' South Southeast ', u' South Southwest ', u' West Southwest ', u' West Northwest ', u' North Northwest ']
        for i in xrange(0, len(dirAbr)):
            string = string.replace(dirAbr[i], dirStr[i])
        string = string +  (" It's currently %d degrees at Titan Radio." % (int(self.get_curr_temp())))
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
        
    def get_conditions(self, state, city):
        try:
            self.curr_json = json.loads(urllib2.urlopen(u"http://api.wunderground.com/api/{}/conditions/q/{}/{}.json".format(self.key, state, city)).read().decode(u"utf-8"))
            return self.curr_json
        except:
            time.sleep(.1)
            return self.get_conditions(state,city)
            
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
            return self.format_string_wind(u"Wilmington area weather, it is currently {}, but feels like {}, and it is {}.".format(self.get_curr_temp(), self.get_curr_feels_like(), self.get_curr_weather()))
        else:
            return self.format_string_wind(u"Wilmington area weather, it is currently {} and it is {}.".format(self.get_curr_temp(), self.get_curr_weather()))
        
    def get_curr_feels_like(self):
        return int(float(self.curr_json[u"current_observation"][u"feelslike_f"]))

    def get_curr_temp(self):
        return int(float(self.curr_json[u"current_observation"][u'temp_f']))
        
    def get_curr_weather(self):
        return self.curr_json[u"current_observation"][u'weather']
        
    def get_forecast(self, state, city):
        try:
            self.fore_json = json.loads(urllib2.urlopen(u"http://api.wunderground.com/api/{}/forecast/q/{}/{}.json".format(self.key, state, city)).read().decode(u"utf-8"))
            return self.curr_json
        except:
            time.sleep(.1)
            return self.get_forecast(state,city)
    
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
        while((("Friday" in self.fore_json[u"forecast"][u"txt_forecast"][u"forecastday"][i][u'title']) or ("Saturday" in self.fore_json[u"forecast"][u"txt_forecast"][u"forecastday"][i][u'title']) or ("Sunday" in self.fore_json[u"forecast"][u"txt_forecast"][u"forecastday"][i][u'title']))):
            s = s + self.format_string_wind(u" {} you should expect {}".format(self.fore_json[u"forecast"][u"txt_forecast"][u"forecastday"][i][u'title'], self.fore_json[u"forecast"][u"txt_forecast"][u"forecastday"][i][u'fcttext']))
            i = i+1
        return self.format_string(s)
        
    def get_report_string(self):
        if self.is_weekend():
            return self.get_forecast_weekend_string()
        elif self.is_night():
            s = u"{} {}".format(self.get_conditions_string(), self.get_forecast_next_step_string())
            return self.format_string(s)
        else:
            s = u"{} {} {}".format(self.get_conditions_string(), self.get_forecast_next_step_string(), self.get_forecast_two_steps_string())
            return self.format_string(s)
    
    def is_night(self):
        return ("night" in self.fore_json[u"forecast"][u"txt_forecast"][u"forecastday"][0][u"title"])
    
    def is_weekend(self):
        return (("Friday" in self.fore_json[u"forecast"][u"txt_forecast"][u"forecastday"][0][u"title"]) or ("Saturday" in self.fore_json[u"forecast"][u"txt_forecast"][u"forecastday"][0][u"title"]) or ("Sunday" in self.fore_json[u"forecast"][u"txt_forecast"][u"forecastday"][0][u"title"]))

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
    key = WeatherReporter(u'WeatherUndergroundAPIKey', u'PA', u'New_Wilmington')
    key.get_report_mp3()
    key.write_all()
    key.read_mp3()
    
    
if __name__ == u"__main__" :
    main()
