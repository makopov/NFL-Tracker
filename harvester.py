import json
import time
import os
import sys
import commands
import datetime
import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

# This is if we're running on none debian systems
try:
    import apt

    cache = apt.Cache()
    if cache['zip'].is_installed == False:
        print "\nERROR: zip pacakge not installed on this system, please install before proceeding."
        exit(1)
except ImportError:
    print "\nWARNING: apt module not available to python, this script will be unable to determine if zip is available.\nPlease be sure the zip package is installed on this system, otherwise archiving will fail."

    # Give the user a moment to read this message
    time.sleep(3)


class TweetHarvester(StreamListener):
    strConsumerKey = ""
    strConsumerSecret = ""
    strAccessTokenKey = ""
    strAccessTokenSecret = ""
    bUseGzip = True
    bPaused = False
    oAuth = None
    oStream = None
    oTweepyAPI = None

    # Default constructor for setting up the object
    def __init__(self):
        self.readCommandLineArgs()
        self.loadConfiguration()
        self.connectToTwitter()

    def on_data(self, strData):
        bReturn = True

        # TODO: threading
        # import threading
        # threading.Thread(self.storeTweets, (strData,)).start()
        self.storeTweets(strData)

        # Lets see if theres anything to archive
        self.archiveFiles()

        # TODO: At the top of every hour report how many tweets have been harvested
        return bReturn

    def on_error(self, strError):
        # Log this to the error file
        bReturn = "true"
        oToday = datetime.date.today ()
        strTodaysDate = oToday.strftime("%Y-%m-%d")

        # does a directory for today date exist yet?
        # if not create one
        if (os.path.exists("./" + strTodaysDate)) is False:
           os.makedirs(strTodaysDate)

        strFile = strTodaysDate + "/" + time.strftime("%H") + ".error"

        oTweetFile = open(strFile, "a")

        oTweetFile.write('\n' + strError)

        oTweetFile.close()

        return bReturn

    def str2bool(self, bValue):
        return bValue.lower() in ("yes", "true", "t", "1")

    def storeTweets(self, strTweets):
        bReturn = "true"
        oToday = datetime.date.today ()
        strTodaysDate = oToday.strftime("%Y-%m-%d")

        # does a directory for today date exist yet?
        # if not create one
        if (os.path.exists("./" + strTodaysDate)) is False:
            os.makedirs(strTodaysDate)

        strFile = strTodaysDate + "/" + time.strftime("%H") + ".txt"

        oTweetFile = open(strFile, "a")

        oTweetFile.write(strTweets)

        oTweetFile.close()

        return bReturn

    def connectToTwitter(self):
        self.oAuth = OAuthHandler(self.strConsumerKey, self.strConsumerSecret)
        self.oAuth.set_access_token(self.strAccessTokenKey, self.strAccessTokenSecret)
        self.oTweepyAPI = tweepy.API(self.oAuth, compression=self.bUseGzip)
        self.oStream = Stream(self.oAuth, self)

    def archiveFiles(self, strFileName=''):
        # If no filename is passed in, lets set one
        if strFileName == '':
            # Lets determine the name of the last directory we created
            oYesterday = datetime.date.today () - datetime.timedelta (days=1)
            strFileToArchive = str(oYesterday.strftime("%Y-%m-%d"))

            strFileName = strFileToArchive

        strZipFileName = strFileName + '.zip'
        strZipCommand = "zip -r " + strZipFileName + " " + strFileName
        iZipCommandStatus, strZipCommandOutput = commands.getstatusoutput(strZipCommand)

        # Check if the file exists firest
        strFileExistsCommand = "ls " + strFileName
        iFileExistsCommandStatus, strExistsCommandOutput = commands.getstatusoutput(strFileExistsCommand)

        # If the file exists, lets continue, otherwise, lets exit
        if iFileExistsCommandStatus == 0:
            # Run the zip command
            if iZipCommandStatus != 0:
                print "Something went wrong while compressing the " + strFileName + " directory"
                print "\tThe following command was issued: `" + strZipCommand + "`"
                print "\tThe following output was recieved: '" + strZipCommandOutput + "'"
            else:
                # If that succeeds lets remove the uncompressed version
                print "Successfully archived '" + strFileName + "' to '" + strZipFileName + "'"

                strDeleteOldFileCommand = "rm -rf " + strFileName
                iRmCommandStatus, strRmCommandOutput = commands.getstatusoutput(strDeleteOldFileCommand)

                if iRmCommandStatus != 0:
                    print "Something went wrong while deleting the " + strFileName + " directory"
                    print "\tThe following command was issued: `" + strDeleteOldFileCommand + "`"
                    print "\tThe following output was recieved: '" + strRmCommandOutput + "'"
                else:
                    print "Successfully deleted uncompressed file '" + strFileName + "'"

        # Put a sleep command in here to sleep this thread for 24 hours
        # print "Archiver sleeping for 24 hours"
        # time.sleep(86400)

    def loadConfiguration(self, strConfigurationFile = ""):
        # If no filename is passed in, lets default to defaultConfig.conf
        if strConfigurationFile == "":
            strConfigurationFile = 'defaultConfig.conf'

        oConfigFile = open(strConfigurationFile)
        oConfigData = json.load(oConfigFile)

        self.strConsumerKey = oConfigData["consumer_key"]
        self.strConsumerSecret = oConfigData["consumer_secret"]
        self.strAccessTokenKey = oConfigData["access_token_key"]
        self.strAccessTokenSecret = oConfigData["access_token_secret"]
        self.bUseGzip = self.str2bool(oConfigData["use_gzip_compression"])

        oConfigFile.close()

    # Read in command line parameters for things like output directory
    def readCommandLineArgs(self):
        foo = "bar"

    def run(self):
        while not self.bPaused:
            self.query()

    def query(self):
        self.oStream.filter(track=['nfl', 'broncos', 'patriots', 'seahawks'], async=True)


oHarvester = TweetHarvester()
oHarvester.run()
