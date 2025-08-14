import tweepy

# Paste your credentials here
api_key = "uzu9gKTi35KseiUZcQuw0zOoe"
api_secret = "KOLm1eigLtqrpx6PzlLbCeXBhvrGi3eCCIWP2GL6C2rfxPzfPw"
access_token = "1946100414149255168-2VJ6KGXvGjkgitFLeaO3hCb9ulm3hx"
access_token_secret = "0liCAlxRGocrTF1x9U6OHgq6kcZsjKVK09Xx4tCj32WI3"

# Authenticate
auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_token_secret)
api = tweepy.API(auth)

# Your tweet
tweet = "Hello world! This is my first automated tweet using #Python and #Tweepy 🚀"

# Post the tweet
api.update_status(status=tweet)
print("Tweet posted successfully!")
