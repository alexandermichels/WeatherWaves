#!/usr/bin/env python
from __future__ import absolute_import
import json, urllib2, urllib
from io import open
from datetime import datetime

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
        raise Exception("This is an abstract class")

    def get_conditions(self, state, city):
        raise Exception("This is an abstract class")

    def get_forecast(self, state, city):
        raise Exception("This is an abstract class")

class DarkSkyConnector(WeatherConnector):

    def __init__(self, config_file):
        ''' add config file that takes long, lat, name of place '''
        with open(config_file) as config:
            data = json.load(config)
            self.key = data["darkskykey"]
            self.lat = float(data["latitude"])
            self.long = float(data["longitude"])
            self.location = data["location"]
            if "name" in data.keys():
                self.name = data["name"]
            else:
                self.name = None
        self.curr_json = None
        self.get_conditions(self.lat, self.long)

    def get_report_string(self):
        return u"{} {}".format(self.get_conditions_string(), self.get_daily_desc())

    def is_night(self):
        am_or_pm = datetime.utcfromtimestamp(int(self.curr_json["currently"]["time"])).strftime('%p')
        hour = int(datetime.utcfromtimestamp(int(self.curr_json["currently"]["time"])).strftime('%-I'))
        if (am_or_pm == "PM" and hour > 7) or (am_or_pm == "AM" and hour < 5):
            return True
        return False

    def is_weekend(self):
        day_of_week = datetime.utcfromtimestamp(int(self.curr_json["currently"]["time"])).strftime('%A')
        return day_of_week in ["Friday", "Saturday", "Sunday"]

    def is_alert(self):
        return "alerts" in self.curr_json

    def print_curr_json(self):
        if self.curr_json == None:
            self.get_conditions(self.lat, self.long)
        print(json.dumps(self.curr_json, sort_keys = True, indent = 4))

    def get_minutely_desc(self):
        return self.curr_json[u"minutely"][u'summary']

    def get_hourly_desc(self):
        return self.curr_json[u"hourly"][u'summary']

    def get_daily_desc(self):
        return self.curr_json[u"daily"][u'summary']

    def get_conditions(self, lat, long):
        self.curr_json = json.loads(urllib2.urlopen(u"https://api.darksky.net/forecast/{}/{},{}".format(self.key, lat, long)).read().decode(u"utf-8"))
        return self.curr_json

    def get_conditions_string(self):
        if (abs(self.get_curr_temp() - self.get_curr_feels_like()) > 5):
            return u"{} area weather, it is currently {}, but feels like {}, and it is {}".format(self.location, self.get_curr_temp(), self.get_curr_feels_like(), self.get_minutely_desc())
        else:
            return u"{} area weather, it is currently {} and it is {}".format(self.location, self.get_curr_temp(), self.get_minutely_desc())

    def get_curr_feels_like(self):
        return int(float(self.curr_json[u"currently"][u'apparentTemperature']))

    def get_curr_temp(self):
        return int(float(self.curr_json[u"currently"][u'temperature']))

    def get_date(self):
        return datetime.utcfromtimestamp(int(self.curr_json["currently"]["time"])).strftime('%A, %B %-d, %Y')

    def get_time(self):
        return datetime.utcfromtimestamp(int(self.curr_json["currently"]["time"])).strftime('%-I:%-M %p')

    def write_all(self):
        self.write_curr_json()
        self.write_report_string()

    def write_curr_json(self):
        f = open("curr_json.txt", "w")
        f.write(json.dumps(self.curr_json, sort_keys=True, indent=4, separators=(',', ': ')).decode('latin1'))
        f.close()

    def write_report_string(self):
        f = open("weather.txt", "w")
        f.write(self.get_report_string())
        f.close()

    def get_alert_title(self, alert_num=0):
        ''' return list and get rid of redundant warnings '''
        return self.curr_json["alerts"][alert_num]["title"]

    def get_alert_locations(self, alert_num=0):
        locations = ""
        for i in range(len(self.curr_json["alerts"][alert_num]["regions"])-1):
            locations+="{}, ".format(self.curr_json["alerts"][alert_num]["regions"][i])
        locations+="and {}".format(self.curr_json["alerts"][alert_num]["regions"][len(self.curr_json["alerts"][alert_num]["regions"])-1])
        return locations

    def get_alert_expiration(self, alert_num=0):
        return datetime.utcfromtimestamp(int(self.curr_json["alerts"][alert_num]["time"])).strftime('%A, %B %-d at %-I %p')

    def get_alerts_desc(self):
        if self.is_alert():
            alert_string = ""
            for i in range(len(d.curr_json["alerts"])):
                alert_string+="There is currently a {} under affect for {} until {}. ".format(self.get_alert_title(i), self.get_alert_locations(i), self.get_alert_expiration(i))
            return alert_string

def pretty_print(_json):
    print(json.dumps(_json, sort_keys=True, indent=4))

if __name__ == "__main__":
    d = DarkSkyConnector("keys/config.json")
    print(d.get_report_string())
    d.write_all()
    print(d.is_alert())
    print(d.get_alerts_desc())
