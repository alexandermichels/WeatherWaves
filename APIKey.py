'''
Simple class to grab a WeatherUnderground API key from a file so I don't have to put that in Git
'''
class APIKey:
    key = ""
    def __init__(self, filename):
        file = open(filename)
        self.key = file.read()
    
    def __str__(self):
        return self.key

def main():
    key = APIKey("WeatherUndergroundAPIKey")
    print(key)
    
if __name__ == "__main__" :
    main()