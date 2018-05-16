import urllib.request, json, vlc
from gtts import gTTS

class APIKey:
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
    def __init__(self, filename):
        file = open(filename)
        self.key = file.read().strip()
    
    def __str__(self):
        return self.key
        
    def get_weather(self, state, city):
        self.curr_json = json.loads(urllib.request.urlopen("http://api.wunderground.com/api/{}/conditions/q/{}/{}.json".format(self.key, state, city)).read().decode("utf-8"))
        return self.curr_json
    
    def print_json(self):
        print(json.dumps(self.curr_json, sort_keys = True, indent = 4))

    def get_curr_temp(self):
        return self.curr_json["current_observation"]['temp_f']       
        
    def get_curr_weather(self):
        return self.curr_json["current_observation"]['weather']
        
    def get_curr_feels_like(self):
        return self.curr_json["current_observation"]["feelslike_f"]
        
    def get_report(self):
        return "It is currently {} degrees farenheit, but feels like {}, and it is {} out today".format(self.get_curr_temp(), self.get_curr_feels_like(), self.get_curr_weather())
        
        
def main():
    key = APIKey('WeatherUndergroundAPIKey')
    res = key.get_weather('PA', 'New_Wilmington')
    key.print_json()
    print(key.get_report())
    tts = gTTS(text=key.get_report(), lang='en')
    tts.save("weather.mp3")
    p = vlc.MediaPlayer("weather.mp3")
    p.play()
    
if __name__ == "__main__" :
    main()
