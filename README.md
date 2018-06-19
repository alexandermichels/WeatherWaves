# WeatherWaves

### Intro

WeatherWaves is a project I am developing for Westminster College's Titan Radio. We are hoping to automate various actions resulting from weather conditions such as updating the weather conditions and forecast when no one is on the air and sending out Tweets when there are severe weather warnings.

For the latest updates check out the [WeatherWaves GitHub](https://github.com/alexandermichels/WeatherWaves).


### Table of Contents
* WeatherConnector
* WeatherReporter
* WeatherTweeter

### WeatherConnector

WeatherConnector is a very simple class which takes either the filename of a file containing a WeatherUnderground API key or the API key itself and has methods for getting the current alerts, conditions, and forecasts in JSON. It is utilized by other classes in WeatherWaves such as WeatherReporter and WeatherTweeter.

### WeatherReporter

WeatherReporter is a package for fetching the current weather conditions and the forecast in order to produce a plaintext or MP3 weather report. Usage looks like this::

    reporter = WeatherReporter(u'PA', u'New_Wilmington', key_file = u'../WeatherUndergroundAPIKey') #instantiate
    reporter.get_report_mp3() #get MP3
    reporter.write_all() #writes report and JSONs to txt files
    reporter.read_mp3() #uses VLC to read to the MP3

WeatherReporter will produce different output based on the time of day and day of week. If it is Friday or Saturday, it will produce a report for the rest of the weekend (Friday through Sunday Night). At night, the report will be for the current conditions and the next day. All other times, the reporter reports on the current conditions and the next two times steps. For example, If it is Tuesday morning, the report will be for Tuesday, Tuesday Night, and Wednesday. These times are determined by WeatherUnderground and I rely on the title of the forecast to determine them. An example from an actual Tuesday forecast can be found below.

> New Wilmington area weather, it is currently 80 and it is Mostly cloudy skies. Tuesday Night you should expect Partly cloudy skies. Low of 62. Wednesday you should expect Rain showers early with overcast skies later in the day. High of 73. Chance of rain 40%.

### WeatherTweeter

WeatherTweeter currently just checks for alerts such as Severe Weather Warnings and tweets a brief synopsis including a description of the event (for example "Severe Thunderstorm Warning") and the time at which the warning expires. I am working to add more flexibility to this. Typical usage::

    tweeter = WeatherTweeter("TwitterAPIKey", u'NY', u'Portland', weather_key_file = u'../WeatherUndergroundAPIKey') #instantiate
    tweeter.print_alerts() #prints the text of the Tweet
    tweeter.connect_to_twitter() #connects to Twitter using your credentials
