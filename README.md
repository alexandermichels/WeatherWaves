# WeatherWaves

WeatherWaves is a project I am developing for Westminster College's Titan Radio. We are hoping to automate various actions resulting from weather conditions such as updating the weather conditions and forecast when no one is on the air and sending out Tweets when there are severe weather warnings.

For the latest updates check out the [WeatherWaves GitHub](https://github.com/alexandermichels/WeatherWaves).


Table of Contents
=================
* WeatherReporter
* WeatherTweeter

WeatherReporter
===============

WeatherReporter is a package for fetching the current weather conditions and the forecast in order to produce a plaintext or MP3 weather report. Usage looks like this::

    reporter = WeatherReporter(path_to_WeatherUnderground_API_key, state, city) #instantiate
    reporter.get_report_mp3() #get MP3
    reporter.write_all() #writes report and JSONs to txt files
    reporter.read_mp3() #uses VLC to read to the MP3

WeatherTweeter
==============

WeatherTweeter currently just checks for alerts such as Severe Weather Warnings and tweets a brief synopsis including a description of the event (for example "Severe Thunderstorm Warning") and the time at which the warning expires. I am working to add more flexibility to this. Typical usage::

    tweeter = WeatherTweeter(path_to_WeatherUnderground_API_key, path_to_Twitter_API_key, state, city) #instantiate
    tweeter.print_alerts() #prints the text of the Tweet
    tweeter.connect_to_twitter() #connects to Twitter using your credentials
