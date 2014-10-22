# README #

This NFL Tracker app is a side project I picked up a little while ago in an attempt to start self educating in Big Data. Currently the python script just calls twitters API, grabs a bunch of tweets based on a search criteria, then stores those tweets in a file. 

Someday the goal is to store these tweets in a data store such as Cassandra, and then run some sort of algorithms on it.

I wrote the script to harvest the tweets in Python, this was my third python script I have ever written, so its practice.

Suggestions, improvements, comments welcome.

### Files ###

* harvester.py (Python script to perform the harvest)
* defaultConfig-orig.conf (Config file for connection settings formatted in JSON)

### Requirements ###

* Python 2.7
* Zip (On Debian systems the script will check if zip is installed)

### Running ###

1. Rename the defaultConfig-orig.conf to defaultConfig.conf
2. Add your apps keys and secrete values in the appropriate place holders within defaultConfig.conf
3. Run the script, "python harvester.py"

### Output ###
* Results will be written out in day organized folders (i.e. 2014-10-1)  divided into hourly blocks
* Every 24 hours the script will zip up the previous days results


### Contact ###

* Michael Akopov
* makopov@gmail.com
* http://michaelakopov.com