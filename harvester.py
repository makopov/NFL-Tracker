import twitter
import json

oTwitterAPI = twitter.Api(consumer_key='q1xeSRo0kXP7aNpRTd89UtKl7',
	consumer_secret='LgqubqReINYxTjWnYGrATqkRhbBlzk0FGPMXJ1pFospnslUg03',
	access_token_key='585462531-VsarINfKCH2eJTUGLgp6vCsVGoFzZZGPA9xWXGS3',
	access_token_secret='Wvj4VXbZIJ3AYC95YepaM9Uxn4ya7n4klBl3X4tSo3d9i')

statuses = oTwitterAPI.GetSearch(term='#broncos', count=500, result_type="recent", include_entities='true')

for s in statuses:
    print '%s\n' % s.text

statuses = oTwitterAPI.GetSearch(term='#patriots', count=500, result_type="recent", include_entities='true')

for s in statuses:
    print '%s\n' % s.text


iRateLimit = oTwitterAPI.GetRateLimitStatus()
#oJsonRateLimit = json.load(iRateLimit)

print iRateLimit
#print oJsonRateLimit
