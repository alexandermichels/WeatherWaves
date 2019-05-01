#!/usr/bin/env python
from __future__ import absolute_import
import json, urllib2, urllib, time, sys, twitter
from io import open
from WeatherConnector import *

class WeatherTweeter(object):

    def __init__(self, config_file_path, weatherconnector):
        with open(config_file_path) as config:
            data = json.load(config)
            try:
                self.twitter_keys = data["twitter_keys"]
            except Exception as e:
                print("The following error occurred while accessing Twitter keys in config file {}:\n{}".format(config_file_path, e))
        try:
            print("Establishing a connection to Twitter...")
            self.twitter_api = twitter.Api(consumer_key=self.twitter_keys['consumer_key'], consumer_secret=self.twitter_keys['consumer_secret'], access_token_key=self.twitter_keys['access_token'], access_token_secret=self.twitter_keys['access_token_secret'])
        except Exception as e:
            print("There was an error connecting to Twitter:\n{}".format(e))

        self.weatherconnector = weatherconnector

    def format_message(self):
        if (self.is_alert() == 1):
            description = self.alerts["alerts"][0]["description"]
            expires = self.alerts["alerts"][0]["expires"].replace("EDT ", "")
            return "The National Weather Service has issued a {} for the {} area which expires {}. Stay safe!".format(description, self.city.replace("_", " "), expires)
        else:
            s = ""
            for i in range(len(self.alerts["alerts"])):
                s += "\n{} which expires {}".format(self.alerts["alerts"][i]["description"], self.alerts["alerts"][i]["expires"].replace("EDT ", ""))
            return "The National Weather Service has issued the following for the " + self.city.replace("_", " ") + " area:" + s + "\nStay safe!"

    def print_alerts(self):
        if self.weatherconnector.is_alert():
            print(self.weatherconnector.get_alert_desc())
        else:
            print("No alerts for {} at the moment".format(self.weatherconnector.location))

    def tweet_alerts(self):
        if self.weatherconnector.is_alert():
            self.twitter_api.PostUpdate(self.format_message())


def main():
    d = DarkSkyConnector("keys/config.json")
    tweeter = WeatherTweeter("keys/config.json", d)
    tweeter.print_alerts()
    # tweeter.tweet_alerts()

if __name__ == u"__main__" :
    main()
