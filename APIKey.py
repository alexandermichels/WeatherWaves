'''
Simple class to grab a WeatherUnderground API key from a file so I don't have to put that in Git
'''
import urllib.request, json

class APIKey:
    key = ""
    def __init__(self, filename):
        file = open(filename)
        self.key = file.read().strip()
    
    def __str__(self):
        return self.key
        
    def get_weather_url(state, city, key):
        return "http://api.wunderground.com/api/{}/conditions/q/{}/{}.json".format(key, state, city)

def main():
    key = APIKey('WeatherUndergroundAPIKey')
    print(key)
    url = key.get_weather_url('PA', 'New_Wilmington')
    print(url)
    res = urllib.request.urlopen(url)
    print(res)
    
if __name__ == "__main__" :
    main()
