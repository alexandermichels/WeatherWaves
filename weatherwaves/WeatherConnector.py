#!/usr/bin/env python
from __future__ import absolute_import
import json, urllib2, urllib
from io import open

class WeatherConnector(object):
    
    def __init__(self, filename = None, api_key = None):
        if (filename == None and api_key == None):
            self.key = None
        elif (api_key == None):
            file = open(filename)
            self.key = file.read().strip()
        elif (filename == None):
            self.key = api_key
    
    def get_alerts(self, state, city):
        return json.loads(urllib2.urlopen("http://api.wunderground.com/api/{}/alerts/q/{}/{}.json".format(self.key, state, city)).read().decode(u"utf-8"))
    
    def get_conditions(self, state, city):
        return json.loads(urllib2.urlopen(u"http://api.wunderground.com/api/{}/conditions/q/{}/{}.json".format(self.key, state, city)).read().decode(u"utf-8"))
        
    def get_forecast(self, state, city):
        return json.loads(urllib2.urlopen(u"http://api.wunderground.com/api/{}/forecast/q/{}/{}.json".format(self.key, state, city)).read().decode(u"utf-8"))
        