#!/usr/bin/env python
from __future__ import absolute_import
import json, urllib2, urllib, time, sys, twitter
from io import open
from weatherwaves.WeatherConnector import *

class WeatherTweeter(object):
    
    def __init__(self, twitter_key, state, city, weather_key_file = None, weather_key = None):
        if (weather_key_file == None and weather_key == None):
            pass
        elif (weather_key == None):
            self.weather_connector = WeatherConnector(filename = weather_key_file)
        elif (weather_key_file == None):
            self.weather_connector = WeatherConnector(api_key = weather_key)
        
        self.twitter_key = twitter_key
        self.state = state
        self.city = city
        self.get_alerts()
        
    def connect_to_twitter(self):
        file = open(self.twitter_key)
        self.twitter_key_dict = {}
        self.twitter_key_dict['consumer_key'] = file.readline().strip()
        self.twitter_key_dict['consumer_secret'] = file.readline().strip()
        self.twitter_key_dict['access_token'] = file.readline().strip()
        self.twitter_key_dict['access_token_secret'] = file.readline().strip()
        self.twitter_api = twitter.Api(consumer_key=self.twitter_key_dict['consumer_key'], consumer_secret=self.twitter_key_dict['consumer_secret'], access_token_key=self.twitter_key_dict['access_token'], access_token_secret=self.twitter_key_dict['access_token_secret'])
        
    def is_alert(self):
        return len(self.alerts["alerts"])
        
    def format_message(self):
        if (self.is_alert() == 1):
            description = self.alerts["alerts"][0]["description"]
            expires = self.alerts["alerts"][0]["expires"].replace("EDT ", "")
            return "The National Weather Service has issued a {} for the New Wilmington area which expires {}. Stay safe!".format(description, expires)
        else:
            s = ""
            for i in range(len(self.alerts["alerts"])):
                s += "\n{} which expires {}".format(self.alerts["alerts"][i]["description"], self.alerts["alerts"][i]["expires"].replace("EDT ", ""))
            return "The National Weather Service has issued the following for the New Wilmington area:" + s + "\nStay safe!"
        
    def get_alerts(self):
        try:
            self.alerts = self.weather_connector.get_alerts(state = self.state, city = self.city)
            try:
                self.alerts["alerts"]
                return self.alerts
            except:            
                time.sleep(.1)
                return self.weather_connector.get_alerts(state = self.state, city = self.city)
        except:
            time.sleep(.1)
            return self.get_alerts()

    def print_alerts(self):
        print(json.dumps(self.alerts, sort_keys = True, indent = 4))
        
    def print_twitter_credentials(self):
        print(self.twitter_credentials)
        
    def tweet_alerts(self):
        if (self.is_alert() > 0):
            self.twitter_api.PostUpdate(self.format_message())
    
            
def main():
    tweeter = WeatherTweeter("TwitterAPIKey", u'NY', u'Portland', weather_key_file = u'WeatherUndergroundAPIKey')
    tweeter.print_alerts()
    tweeter.connect_to_twitter()
    tweeter.tweet_alerts()
    
if __name__ == u"__main__" :
    main()