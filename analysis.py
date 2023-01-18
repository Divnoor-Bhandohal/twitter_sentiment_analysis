import datetime
from datetime import timezone

import rfc3339  

import time

import re

import string

import numpy as np

import tweepy

from tweepy import OAuthHandler

from textblob import TextBlob

import matplotlib.pyplot as plt

import pandas as pd


# twitter developer account credentials needed to make an API call

api_key = 'Q6cLxjRi5OAQJpxRUhXpTW9nT'

api_secret = 'VYPWZn6sTAFA38aXer3vA2ypW2yEfgQ5dq45LWburbqaCtOizw'

bearer_token = '''AAAAAAAAAAAAAAAAAAAAAGZLkwEAAAAAi%2F1nRZ5f50Mgs0Pdn%2B%2BNTXP94uU%3DooQbmsZmtOSM4xGGDwPqItPnEDUeUHMu2U8aPtYXEM2Qk9QU58'''

access_token = '1101547718432956416-6ZoFINywGbiY0lurqnjSp841CQlvuD'

access_token_secret = 'w0O5YxHF7plcLIFAEgkbxK7jAoU949hwQnUZmqLzkR8qq'

day = input('Enter the date you want to get the analysis for in Format DD (Maximum of Six days Ago from Now) OR (Press Enter to get for Today): ')
print(day)

if(day): 
   day = int(day)
   analysisDay = datetime.datetime(2023,datetime.datetime.now().month, day)
   rfcDate= rfc3339.rfc3339(analysisDay)

else:
    rfcDate=None

query = input("Please enter the topic you want to get the analysis for: ")

#  Only getting the Tweets in English by using a filter

filtered = query + " -is:retweet lang:en"




client = tweepy.Client(bearer_token=bearer_token)
res = client.search_recent_tweets(query=filtered, max_results=100, start_time = rfcDate)

#  making a list for all the tweets in the response

list1 = [[tweet.text] for tweet in res.data]


# making a data frame from all the tweets

df = pd.DataFrame(data=list1,
                  columns=['tweets'])


tweet_list = df.tweets.to_list()

#  cleaning the tweets by removing all the unwanted characters 
def clean_tweet(tweet):
    regex = tweet.lower()
    # This is to avoid removing contractions in english
    regex = re.sub("'", "", regex)
    regex = re.sub("@[A-Za-z0-9_]+", "", regex)
    regex = re.sub("#[A-Za-z0-9_]+", "", regex)
    regex = re.sub(r'http\S+', '', regex)
    regex = re.sub('[()!?]', ' ', regex)
    regex = re.sub('\[.*?\]', ' ', regex)
    regex = re.sub("[^a-z0-9]", " ", regex)
    regex = regex.split()
    stopwords = ["for", "on", "an", "a", "of", "and", "in", "the", "to", "from"]
    regex = [w for w in regex if not w in stopwords]
    regex = " ".join(word for word in regex)
    return regex


#  creating a new data frame with the cleaned tweets
cleaned = [clean_tweet(tw) for tw in tweet_list]

df = pd.DataFrame(data=cleaned,
                  columns=['tweets'])


# making sentiment objects using TextBlob

sentiment_objects = [TextBlob(tweet) for tweet in cleaned]


# Creating a list of polarity values and tweets

sentiment_values = [[tweet.sentiment.polarity,
                     str(tweet)] for tweet in sentiment_objects]


sentiment_df = pd.DataFrame(sentiment_values, columns=["polarity", "tweet"])


# Saving the polarity column as 'n'.

n = sentiment_df["polarity"]

# Converting this column into a series.

m = pd.Series(n)


# Initialize variables, 'pos', 'neg', 'neu'.

pos = 0
neg = 0
neu = 0

# Create a loop to classify the tweets as Positive, Negative, or Neutral.
# Count the number of each.

for polarity in m:
    if polarity > 0:
        pos = pos+1
    elif polarity < 0:
        neg = neg+1
    else:
        neu = neu+1

print(pos, neg, neu)


# plotting the results as a pie chart

pieLabels = ["Positive", "Negative", "Neutral"]

populationShare = [pos, neg, neu]

figureObject, axesObject = plt.subplots()

axesObject.pie(populationShare, labels=pieLabels,
               autopct='%1.2f', startangle=90)

axesObject.axis('equal')

plt.show()
