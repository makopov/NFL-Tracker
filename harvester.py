import twitter
import json
import time
import os
import sys
import commands
import datetime
#This is if we're running on none debian systems
try:
    import apt

    cache = apt.Cache()
    if cache['zip'].is_installed == False:
        print "\nERROR:\tzip pacakge not installed on this system, please install before proceeding."
        exit(1)
except ImportError:
    print "\nWARNING:\tapt module not available to python, this script will be unable to determine if zip is available.\nPlease be sure the zip package is installed on this system, otherwise archiving will fail."

    #Give the user a moment to read this message
    time.sleep(3)

class TweetHarvester:
    strConsumerKey = ""
    strConsumerSecret = ""
    strAccessTokenKey = ""
    strAccessTokenSecret = ""
    bUseGzip = True
    bPaused = False

    #Default constructor for setting up the object
    def __init__(self):
        self.readCommandLineArgs()
        self.loadConfiguration()

    def str2bool(self, bValue):
      return bValue.lower() in ("yes", "true", "t", "1")

    def storeTweets(self, aTweets):
        bReturn = "true"
        oToday = datetime.date.today ()
        strTodaysDate = oToday.strftime("%Y-%m-%d")

        #does a directory for today date exist yet?
        #if not create one
        if (os.path.exists("./" + strTodaysDate)) is False:
           os.makedirs(strTodaysDate)

        strFile = strTodaysDate + "/" + time.strftime("%H") + ".txt"

        oTweetFile = open(strFile, "a")

        oTweetFile.write('\n'.join(str(tweet) for tweet in aTweets))

        oTweetFile.close()

        print "Results written to " + strFile
        return bReturn

    def connectToTwitter(self):
        return twitter.Api(
            consumer_key = self.strConsumerKey,
            consumer_secret = self.strConsumerSecret,
            access_token_key = self.strAccessTokenKey,
            access_token_secret = self.strAccessTokenSecret,
            use_gzip_compression = self.bUseGzip
            )

    def archiveFiles(self, strFileName=''):
        #If no filename is passed in, lets set one
        if (strFileName == ''):
            #Lets determine the name of the last directory we created
            oYesterday = datetime.date.today () - datetime.timedelta (days=1)
            strFileToArchive = str(oYesterday.strftime("%Y-%m-%d"))

            strFileName = strFileToArchive

        strZipFileName = strFileName + '.zip'
        strZipCommand = "zip -r " + strZipFileName + " " + strFileName
        iZipCommandStatus, strZipCommandOutput = commands.getstatusoutput(strZipCommand)

        #Check if the file exists firest
        strFileExistsCommand = "ls " + strFileName
        iFileExistsCommandStatus, strExistsCommandOutput = commands.getstatusoutput(strFileExistsCommand)

        #If the file exists, lets continue, otherwise, lets exit
        if (iFileExistsCommandStatus == 0):
            #Run the zip command
            if (iZipCommandStatus != 0):
                print "Something went wrong while compressing the " + strFileName + " directory"
                print "\tThe following command was issued: `" + strZipCommand + "`"
                print "\tThe following output was recieved: '" + strZipCommandOutput + "'"
            else:
                #If that succeeds lets remove the uncompressed version
                print "Successfully archived '" + strFileName + "' to '" + strZipFileName + "'"

                strDeleteOldFileCommand = "rm -rf " + strFileName
                iRmCommandStatus, strRmCommandOutput = commands.getstatusoutput(strDeleteOldFileCommand)

                if (iRmCommandStatus != 0):
                    print "Something went wrong while deleting the " + strFileName + " directory"
                    print "\tThe following command was issued: `" + strDeleteOldFileCommand + "`"
                    print "\tThe following output was recieved: '" + strRmCommandOutput + "'"
                else:
                    print "Successfully deleted uncompressed file '" + strFileName + "'"
        else:
            print "The file '" + strFileName + "' doesnt exist, nothing to compress"

        #Put a sleep command in here to sleep this thread for 24 hours
        #print "Archiver sleeping for 24 hours"
        #time.sleep(86400)

    def loadConfiguration(self, strConfigurationFile = ""):
        #If no filename is passed in, lets default to defaultConfig.conf
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

    #Read in command line parameters for things like output directory
    def readCommandLineArgs(self):
        foo = "bar"

    def run(self):
        while not self.bPaused:
            self.query()

    def query(self):
        oTwitterAPI = self.connectToTwitter()

        #Check our rate limit
        oRateLimit = oTwitterAPI.GetRateLimitStatus()

        iRequestsAllowed =  oRateLimit["resources"]["search"]["/search/tweets"]["limit"]
        iRequestsRemaining = oRateLimit["resources"]["search"]["/search/tweets"]["remaining"]
        iRequestsReset = oRateLimit["resources"]["search"]["/search/tweets"]["reset"]

        iTweetCount = 0
        iLoopCount = 0
        iStartTime = 0
        iDoneTime = 0
        aTweets = list()

        if iRequestsRemaining > 0:
            print "Starting next interval of search requests.."
            print str(iRequestsRemaining) + " search requests are available at this time"
            iStartTime = time.time()

            #TODO: If we can make API calls, we need to re read the terms file
            #make some function call here to read in terms

            for iLoop in range(0, iRequestsRemaining):
                #Get Tweets if we have requests available
                try:
                    aSearchResults = oTwitterAPI.GetSearch(term='broncos OR seahawks OR patriots OR nfl', count=500, include_entities=True)
                except twitter.TwitterError:
                    print "Something went wrong with the connection..."
                    oTwitterAPI = self.connectToTwitter()
                    break
                except:
                    print "Something went wrong, we'll re establish a connection and try again"
                    oTwitterAPI = self.connectToTwitter()
                    break

                #check if we've hit our rate limit somehow
                if "message" in aSearchResults == True:
                    #rate limit exceeded..somehow, lets sleep
                    break;
                else:
                    aTweets += aSearchResults

                iLoopCount +=1
                iTweetCount += len(aSearchResults)
                del aSearchResults

            #TODO: threading
            #import threading
            #threading.Thread(storeTweets, (aTweets,)).start()

            self.storeTweets(aTweets)
            iDoneTime = time.time()

        del aTweets

        #Lets see what we got
        print "Interval execution time was " + str((iDoneTime - iStartTime)/60) + " minutes"
        print "Total number of tweets " + str(iTweetCount)
        print "Total number of search API calls " + str(iLoopCount)

        #Sleep untill next reset
        iCurrentTime = time.time()
        iTimeToSleepFor = iRequestsReset - iCurrentTime + 1

        #Lets see if theres anything to archive
        self.archiveFiles()

        print "Sleeping for " + str(iTimeToSleepFor) + " seconds.."
        time.sleep(iTimeToSleepFor)

oHarvester = TweetHarvester()
oHarvester.run()
