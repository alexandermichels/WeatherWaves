import urllib.request, json, vlc
from gtts import gTTS

class WeatherReporter:
    '''
    Simple class to interact with the WeatherUnderground API 
    
    ---Instance Variables
    key = a string containing the API key
    
    ---Methods
    __init__(filename) = takes a string, opens said file, and sets the key field as the read().strip() output
    __str__ = returns the key field
    get_weather(state, city) = returns the JSON of the weather at the location
    '''
    key = ""
    curr_json = ""
    fore_json = ""
    mp3_filename = "weather.mp3"
    def __init__(self, filename, state, city):
        file = open(filename)
        self.key = file.read().strip()
        self.get_conditions(state,city)
        self.get_forecast(state,city)
    
    def __str__(self):
        return self.key
    
    def format_string(self, string):
        string = string.replace("F.", ".")
        dirAbr = [ ' N ', ' E ', ' S ', ' W ', ' NW ', ' NE ', ' SW ', ' SE ', ' NNE ', ' ENE ', ' ESE ', ' SSE ', ' SSW ', ' WSW ', ' WNW ', ' NNW ']
        dirStr = [ ' North ', ' East ', ' South ', ' West ', ' Northwest ', ' Northeast ', ' Southwest ', ' Southeast ', ' North Northeast ', ' East Northeast ', ' East Southeast ', ' South Southeast ', ' South Southwest ', ' West Southwest ', ' West Northwest ', ' North Northwest ']
        for i in range(0, len(dirAbr)):
            string = string.replace(dirAbr[i], dirStr[i])
        return string
        
    def get_conditions(self, state, city):
        self.curr_json = json.loads(urllib.request.urlopen("http://api.wunderground.com/api/{}/conditions/q/{}/{}.json".format(self.key, state, city)).read().decode("utf-8"))
        return self.curr_json
            
    def get_report_mp3(self):
        tts = gTTS(text = self.get_report_string(), lang='en')
        tts.save(self.mp3_filename)
        
    def get_conditions_string(self):
        #add logic
        return "It is currently {} degrees farenheit, but feels like {}, and it is {} out.".format(self.get_curr_temp(), self.get_curr_feels_like(), self.get_curr_weather())
        
    def get_curr_feels_like(self):
        return self.curr_json["current_observation"]["feelslike_f"]

    def get_curr_temp(self):
        return self.curr_json["current_observation"]['temp_f']       
        
    def get_curr_weather(self):
        return self.curr_json["current_observation"]['weather']
        
    def get_forecast(self, state, city):
        self.fore_json = json.loads(urllib.request.urlopen("http://api.wunderground.com/api/{}/forecast/q/{}/{}.json".format(self.key, state, city)).read().decode("utf-8"))
        return self.curr_json
    
    def get_forecast_next_step(self):
        return self.fore_json["forecast"]["txt_forecast"]["forecastday"][1]
    
    def get_forecast_next_step_string(self):
        s = self.get_forecast_next_step()
        return "{} you should expect {}".format(s['title'], s['fcttext'])
    
    def get_forecast_two_steps(self):
        return self.fore_json["forecast"]["txt_forecast"]["forecastday"][2]
        
    def get_forecast_two_steps_string(self):
        s = self.get_forecast_two_steps()
        return "{} you should expect {}".format(s['title'], s['fcttext'])
    
    def get_report_string(self):
        s = "{} {} {}".format(self.get_conditions_string(), self.get_forecast_next_step_string(), self.get_forecast_two_steps_string())
        return self.format_string(s)

    def print_curr_json(self):
        print(json.dumps(self.curr_json, sort_keys = True, indent = 4))
    
    def print_fore_json(self):
        print(json.dumps(self.fore_json, sort_keys = True, indent = 4))
        
    def read_mp3(self):
        vlc.MediaPlayer(self.mp3_filename).play()
        
def main():
    key = WeatherReporter('WeatherUndergroundAPIKey', 'PA', 'New_Wilmington')
    key.print_fore_json()
    print(key.get_report_string())
    key.get_report_mp3()
    key.read_mp3()
    #deal with degree and NWSE abbrevations
    
    
if __name__ == "__main__" :
    main()
