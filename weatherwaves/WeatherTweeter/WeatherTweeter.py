#!/usr/bin/env python
from __future__ import absolute_import
import json, urllib2, urllib, time, sys, twitter
from io import open

class WeatherTweeter(object):
    
    def __init__(self, weather_key, twitter_key, state, city):
        file = open(weather_key)
        self.key = file.read().strip()
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
        api = twitter.Api(consumer_key=self.twitter_key_dict['consumer_key'], consumer_secret=self.twitter_key_dict['consumer_secret'], access_token_key=self.twitter_key_dict['access_token'], access_token_secret=self.twitter_key_dict['access_token_secret'])
        self.twitter_credentials = api.VerifyCredentials()
        return True
        
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
            self.alerts = json.loads(urllib2.urlopen("http://api.wunderground.com/api/{}/alerts/q/{}/{}.json".format(self.key, self.state, self.city)).read().decode(u"utf-8"))
            try:
                self.alerts["alerts"]
                return self.alerts
            except:            
                time.sleep(.1)
                return self.get_alerts()
        except:
            time.sleep(.1)
            return self.get_alerts()

    def print_alerts(self):
        print(json.dumps(self.alerts, sort_keys = True, indent = 4))
        
    def print_twitter_credentials(self):
        print(self.twitter_credentials)
    
            
def main():
    tweeter = WeatherTweeter(u'../WeatherUndergroundAPIKey', "TwitterAPIKey", u'NY', u'Portland')
    tweeter.print_alerts()
    tweeter.connect_to_twitter()
    tweeter.print_twitter_credentials()
    
if __name__ == u"__main__" :
    main()