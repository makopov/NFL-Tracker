import twitter
import json
import time

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

    if iRequestsRemaining > 0:
        #Get Tweets if we have requests available
        statuses = oTwitterAPI.GetSearch(term='#broncos', count=500, include_entities='true')
        iCount = 0

        for s in statuses:
            iCount += 1
            #print '%s\n' % s.text

        print "#broncos count = " + str(iCount)

        iCount = 0
        statuses = oTwitterAPI.GetSearch(term='#nfl', count=500, include_entities='true')

        for s in statuses:
            iCount += 1 
            #print '%s\n' % s.text

        print "#patriots count = " + str(iCount)

    #Sleep untill next reset
    iCurrentTime = time.time()
    iTimeToSleepFor = iRequestsReset - iCurrentTime + 1
    
    print str(iCurrentTime) + " - " + str(iRequestsReset) + " = " + str(iTimeToSleepFor)
    time.sleep(iTimeToSleepFor)

