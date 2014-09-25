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

    print "reset= " + str(iRequestsReset) + ", remaining = " + str(iRequestsRemaining) + ", allowed = " + str(iRequestsAllowed)

    sys.exit(0)
    if iRequestsRemaining > 0:
        #TODO: If we can make API calls, we need to re read the terms file
        #make some function call here to read in terms

        for iLoop in range(0, iRequestsRemaining):
            #Get Tweets if we have requests available
            aTweets = oTwitterAPI.GetSearch(term='broncos OR seahawks OR patriots OR nfl', count=500, include_entities='true')
            
            storeTweets(aTweets)

            iLoopCount +=1
            iTweetCount += len(aTweets)

    
    #Lets see what we got
    print "Total number of tweets " + str(iTweetCount)
    print "Total number of search API calls " + str(iLoopCount)
    
    #Sleep untill next reset
    iCurrentTime = time.time()
    iTimeToSleepFor = iRequestsReset - iCurrentTime + 1
    
    print str(iCurrentTime) + " - " + str(iRequestsReset) + " = " + str(iTimeToSleepFor)
    time.sleep(iTimeToSleepFor)

