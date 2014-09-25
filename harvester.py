import twitter
import json
import time
import os
import sys

def storeTweets(aTweets):
    bReturn = "true"
    strTodaysDate = time.strftime("%Y-%m-%d")
    
    #does a directory for today date exist yet?
    #if not create one
    if (os.path.exists("./" + strTodaysDate)) is False:
       os.makedirs(strTodaysDate) 
    
    strFile = strTodaysDate + "/" + time.strftime("%H") + ".txt"
    
    oTweetFile = open(strFile, "a")
    
    for strTweet in aTweets:
        oTweetFile.write(str(strTweet))

    oTweetFile.close()

    print "Results written to " + strFile
    return bReturn

oTwitterAPI = twitter.Api(consumer_key='q1xeSRo0kXP7aNpRTd89UtKl7',
	consumer_secret='LgqubqReINYxTjWnYGrATqkRhbBlzk0FGPMXJ1pFospnslUg03',
	access_token_key='585462531-VsarINfKCH2eJTUGLgp6vCsVGoFzZZGPA9xWXGS3',
	access_token_secret='Wvj4VXbZIJ3AYC95YepaM9Uxn4ya7n4klBl3X4tSo3d9i',
    use_gzip_compression='true')

bContinue = 'true'

while bContinue:
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
            aSearchResults = oTwitterAPI.GetSearch(term='broncos OR seahawks OR patriots OR nfl', count=500, include_entities='true')
            
            #check if we've hit our rate limit somehow
            if "message" in aSearchResults == True:
                #rate limit exceed..somehow, lets sleep
                break;
            else:
                aTweets += aSearchResults

            iLoopCount +=1
            iTweetCount += len(aSearchResults)

        storeTweets(aTweets)
        iDoneTime = time.time()

    del aTweets

    #Lets see what we got
    print "Interval execution time was " + str((iDoneTime - iStartTime)/60) + " minutes"
    print "Total number of tweets " + str(iTweetCount)
    print "Total number of search API calls " + str(iLoopCount)
    
    #Sleep untill next reset
    iCurrentTime = time.time()
    iTimeToSleepFor = iRequestsReset - iCurrentTime + 1
    
    print "Sleeping for " + str(iTimeToSleepFor) + " seconds.."
    time.sleep(iTimeToSleepFor)

