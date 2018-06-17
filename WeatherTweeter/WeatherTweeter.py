#!/usr/bin/env python
from __future__ import absolute_import
import json, urllib2, urllib, time
from io import open

class WeatherTweeter(object):
    
    def __init__(self, filename, state, city, verbosity=1):
        file = open(filename)
        self.key = file.read().strip()
        self.state = state
        self.city = city
        self.get_alerts()
        self.verbosity = verbosity
    
    def get_alerts(self):
        try:
            self.alerts = json.loads(urllib2.urlopen("http://api.wunderground.com/api/{}/alerts/q/{}/{}.json".format(self.key, self.state, self.city)).read().decode(u"utf-8"))
            return self.alerts
        except:
            time.sleep(.1)
            return self.get_alerts()

    def print_alerts(self):
        print json.dumps(self.alerts, sort_keys = True, indent = 4)
            
def main():
    key = WeatherTweeter(u'../WeatherUndergroundAPIKey', u'PA', u'New_Wilmington')
    key.print_alerts()
    
if __name__ == u"__main__" :
    main()