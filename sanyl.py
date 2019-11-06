import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob

# query var
q = input("Enter query --> ")

# Generic Twitter Class for sent analysis


class TwitterClient(object):
    # class constructor
    def __init__(self):
        # keys and tokens from the Twitter Dev Console
        consumer_key = 'G7rkAffuSU0HQmQu5IvAkOLfL'
        consumer_secret = 'XWKtMCpHflObRNHBDhijvfkqkoDPy0Pa8XfTn4kogH6FO2rtDF'
        access_token = '832334793996132352-QOPhUzY3RtSvbRDwCzY4VReRmOmEAmR'
        access_token_secret = 'MEwxx1QkZobE0IDiF825pP6BGcd0jNN47bDoLiTym5aeU'

        # attempt authentication
        try:
            # create OAuthHandler object
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            # set acccess token and secret
            self.auth.set_access_token(access_token, access_token_secret)
            # create tweepy API object to fetch tweets
            self.api = tweepy.API(self.auth)
        except:
            print("Error: authentication failed")

    # utility function to clean tweets text by removing links and special characters using simple regex statements
    def clean_tweet(self, tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    # utitlity function to classify sentiment of passed tweet using textblob's sentiment method
    def get_tweet_sentiment(self, tweet):
        # create TextBlob object of passed tweet text
        analysis = TextBlob(self.clean_tweet(tweet))
        # set sentiment
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'

    # main function to fetch tweets and parse them
    def get_tweets(self, query, count=10):
        # empty list to store the parsed tweets
        tweets = []

        try:
            # call twitter api to fetch tweets
            fetched_tweets = self.api.search(q=query, count=count)

            # parsing tweets one by one
            for tweet in fetched_tweets:
                # empty dictionary to store required params of a tweet
                parsed_tweet = {}

                # saving text of tweet
                parsed_tweet['text'] = tweet.text
                # saving sentiment of tweet
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(
                    tweet.text)

                # appending parsed tweet to tweets list
                if tweet.retweet_count > 0:
                    # if tweet has retweets, ensure that it's appended only once
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)
            # return parsed tweets
            return tweets

        except tweepy.TweepError as e:
            # print error (if any)
            print("Error: " + str(e))


def main():
    # creating object of TwitterClient class
    api = TwitterClient()
    # calling functiojns to get tweets
    tweets = api.get_tweets(query=q, count=200)
    # picking positive tweets from tweets
    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']

    # print query
    print("Query: " + q)
    # precentage of positive tweets
    print("Positive tweets precentage: {} %".format(
        100*len(ptweets)/len(tweets)))
    # picking negative tweets from tweets
    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
    # precentage of negative tweets
    print("Negative tweets precentage: {} %".format(
        100*len(ntweets)/len(tweets)))
    # precentage of neutral tweets
    '''
    print("Neutral tweets precentage: {} % ".format(
        100*len(tweets - ntweets - ptweets)/len(tweets)))
    '''

    # printing first 5 positive tweets
    print("\n\nPositive Tweets:")
    for tweet in ptweets[:10]:
        print(tweet['text'])

    # printing first 5 negative tweets
    print("\n\nNegative Tweets")
    for tweet in ntweets[:10]:
        print(tweet['text'])


if __name__ == "__main__":
    # calling main function
    main()
