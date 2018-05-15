import urllib.request, json

class APIKey:
    '''
    Simple class to interact with the WeatherUnderground API 
    
    ---Instance Variables
    key = a string containing the API key
    
    ---Methods
    __init__(filename) = takes a string, opens said file, and sets the key field as the read().strip() output
    __str__ = returns the key field
    get_weather_url(state, city, key)
    '''
    key = ""
    def __init__(self, filename):
        file = open(filename)
        self.key = file.read().strip()
    
    def __str__(self):
        return self.key
        
    def get_weather(self, state, city):
        return urllib.request.urlopen("http://api.wunderground.com/api/{}/conditions/q/{}/{}.json".format(self.key, state, city)).read().decode("utf-8")

def main():
    key = APIKey('WeatherUndergroundAPIKey')
    res = key.get_weather('PA', 'New_Wilmington')
    print(res)
    
if __name__ == "__main__" :
    main()
