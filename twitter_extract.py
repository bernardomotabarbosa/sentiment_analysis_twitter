import argparse
import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
from google_trans_new import google_translator
from spacy.lang.en import STOP_WORDS
from spacy.lang.pt import stop_words
import string
import emoji
import pandas as pd
import time
import datetime


class TwitterClient(object):
    '''
    Generic Twitter Class for sentiment analysis.
    '''

    def __init__(self):
        '''
        Class constructor or initialization method.
        '''
        # keys and tokens from the Twitter Dev Console
        self.translator = google_translator()
        self.pt_stopwords = stop_words.STOP_WORDS
        self.en_stopwords = STOP_WORDS
        self.others_words = ('rt', 'rt ' 'te', 'plenoNews', 'seg', 'google', 'pra', 'pro', 'ainda', 'vc', 'são', 's',
                             'se', 'teria', 'hoje', 'de', 'há', 'https', 'tmj', 'bj', 'abs', 'dmr', 'tlg', 'tlgd', 'RJ',
                             'ES', 'MG', 'SP')
        self.sentiment_words = ('brasil', 'brazil', 'guedes', 'bolsonaro', 'lula', 'covid', 'covid19', 'covid-19')
        self.punctuations = string.punctuation + '‘' + 'º' + '’' + '-' + '"' + "”" + "'" + "“" + '...' + '#' + '@'
        self.list_of_words = []
        self.consumer_key = 'dXkYZCN9hrtqJ9Zy7PY1Gq1e2'
        self.consumer_secret = 'LLHE5PIqXRfYXPL0UUVp0OmoZ78HYht2GuynvYal48FIhSsIvW'
        self.access_token = '1268541340410957827-4RUVGZ8gvWIJvlx9KP3eBtuexv2tyD'
        self.access_token_secret = '7VAfqLjRuswvXFadF5ynOBHUt079Vt8niAdTbu4RZufr4'

        # attempt authentication
        try:
            # create OAuthHandler object
            self.auth = OAuthHandler(self.consumer_key, self.consumer_secret)
            # set access token and secret
            self.auth.set_access_token(self.access_token, self.access_token_secret)
            # create tweepy API object to fetch tweets
            self.api = tweepy.API(self.auth)
        except:
            print("Error: Authentication Failed")

    def remove_emoji(self, text):
        return emoji.get_emoji_regexp().sub(u'', text)

    def remove_punctuations(self, text):
        for punctuation in self.punctuations:
            text = text.replace(punctuation, '')
        return text

    def clean_tweet(self, tweet, translate=False):
        '''
        Utility function to clean tweet text by removing links, special characters
        using simple regex statements.
        '''
        tweet = tweet.lower()
        tweet = tweet.strip()
        if tweet[-1] == '…':
            tweet = ' '.join(tweet.split()[:-1])
        tweet = tweet.replace('tbm', ' também ').replace('vc', ' você ').replace('vcs', ' vocês ').replace(
            'cv', 'conversa').replace('hj', '').replace('dnv', '').replace(' n ', 'não').replace(' s ',
                                                                                                 'sim').replace(
            'dps', '').replace(' agr ', 'agora').replace('pq', 'por que').replace(' obs ', 'observação').replace(
            ' q ', 'que').replace('fzr', 'fazer').replace('gnt', 'gente').replace(' net ', 'internet').replace(
            'cmg', 'comigo').replace('msg', 'mensagem').replace('mt', 'muito').replace(' ces ', 'vocês').replace(
            ' ce ',
            'você')
        tweet = re.sub('rt @\w+: ', " ", tweet)
        tweet = re.sub(r'https?:\/\/[A-Za-z0-9\.\/]+', '', tweet)
        tweet = tweet.strip()
        if tweet[-1] == '…':
            tweet = ' '.join(tweet.split()[:-1])
        tweet = ' '.join(re.sub("(@[A-Za-z0-9]+)|(\w+:\/\/\S+)", " ", tweet).split())
        tweet = self.remove_emoji(tweet)
        tweet = re.sub('kk+', '', tweet)
        if translate:
            tweet_en = self.translator.translate(tweet, lang_tgt='en')
            time.sleep(0.5)
            tweet_en = tweet_en.lower()
            tweet_en = ' '.join([word for word in tweet_en.split() if
                                 word not in (self.en_stopwords) and word not in (self.others_words) and word not in (
                                     self.sentiment_words) and word not in tuple(self.list_of_words)])
            tweet_en = self.remove_punctuations(tweet_en)
            tweet_en = ' '.join([w for w in tweet_en.split() if not w.isdigit()])
            tweet_en = ' '.join([w for w in tweet_en.split() if not len(w) == 1])
            tweet_en = re.sub('  +', '', tweet_en)
            tweet_en = tweet_en.encode('ascii', 'ignore').decode('ascii')

            tweet = ' '.join([word for word in tweet.split() if
                              word not in (self.pt_stopwords) and word not in (self.others_words)])
            tweet = self.remove_punctuations(tweet)
            tweet = ' '.join([w for w in tweet.split() if not w.isdigit()])
            tweet = ' '.join([w for w in tweet.split() if not len(w) == 1])
            tweet = re.sub('  +', '', tweet)

            return tweet, tweet_en

        else:
            tweet = ' '.join([word for word in tweet.split() if
                              word not in (self.pt_stopwords) and word not in (self.others_words)])
            tweet = self.remove_punctuations(tweet)
            tweet = ' '.join([w for w in tweet.split() if not w.isdigit()])
            tweet = ' '.join([w for w in tweet.split() if not len(w) == 1])
            tweet = re.sub('  +', '', tweet)

            return tweet

    def get_tweet_sentiment(self, tweet):
        '''
        Utility function to classify sentiment of passed tweet
        using textblob's sentiment method
        '''
        # create TextBlob object of passed tweet text
        analysis = TextBlob(tweet)
        # set sentiment
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'

    def get_tweet_text(self, query, total_count):

        tweets_clean = []
        tweets_clean_en = []
        initial_tweets = []
        sentiments = []
        create_dates = []

        date = datetime.datetime.now() + datetime.timedelta(1)
        if len(str(date.month)) == 1:
            month = '0' + str(date.month)
        else:
            month = date.month
        if len(str(date.day)) == 1:
            day = '0' + str(date.day)
        else:
            day = date.day
        date_str = f'{date.year}-{month}-{day}'

        while True:
            fetched_tweets = self.api.search(q=query, count=total_count, lang='pt', result_type='mixed',
                                             until=date_str)
            if len(fetched_tweets) == 0:
                break

            for tweet in fetched_tweets:
                tweet_text, tweet_text_en = self.clean_tweet(tweet.text, translate=True)
                sentiment = self.get_tweet_sentiment(tweet_text_en)
                sentiments.append(sentiment)
                tweets_clean.append(tweet_text)
                tweets_clean_en.append(tweet_text_en)
                initial_tweets.append(tweet.text)
                create_dates.append(tweet.created_at.strftime("%d/%m/%Y"))

            day = str(int(date_str.split('-')[-1]) - 1)
            if len(str(day)) == 1:
                day = '0' + str(day)
            list_date = date_str.split('-')
            list_date[-1] = day
            date_str = '-'.join(list_date)
            print('Extraction date', date_str)
        return tweets_clean, initial_tweets, sentiments, create_dates, tweets_clean_en

    def data_base_tweets(self, num_tweets_word_by_day, path_to_save):
        api = TwitterClient()
        if path_to_save[-1] != '/':
            path_to_save = path_to_save + '/'
        list_tweets = []
        list_initial_tweets = []
        list_sentiments = []
        list_words_searched = []
        list_dates = []
        list_tweets_clean_en = []
        for id, word in enumerate(self.list_of_words):
            print(f'Percentage of processing: {round(id / len(self.list_of_words), 2)} %, current word: {word}')
            tweets, initial_tweets, sentiments, create_dates, tweets_clean_en = api.get_tweet_text(query=word,
                                                                                                   total_count=num_tweets_word_by_day)
            for ele in range(len(tweets)):
                list_tweets.append(tweets[ele])
                list_initial_tweets.append(initial_tweets[ele])
                list_sentiments.append(sentiments[ele])
                list_words_searched.append(word)
                list_dates.append(create_dates[ele])
                list_tweets_clean_en.append(tweets_clean_en[ele])
        df = pd.DataFrame(columns=['word', 'date', 'tweet_initial', 'tweet_clean', 'tweet_to_sentiment', 'sentiment'])
        df['word'] = list_words_searched
        df['date'] = list_dates
        df['tweet_initial'] = list_initial_tweets
        df['tweet_clean'] = list_tweets
        df['tweet_to_sentiment'] = list_tweets_clean_en
        df['sentiment'] = list_sentiments
        df.drop_duplicates(subset="tweet_initial", inplace=True)
        writer = pd.ExcelWriter(path_to_save + f'{time.time()}_tweets.xlsx', engine='xlsxwriter')
        df.to_excel(writer, sheet_name='welcome', index=False)
        writer.save()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--list", nargs="+", default=["a", "b"], required=True, help="List of words to search")
    parser.add_argument('-n', '--num_tweets_each_word_per_day', required=True,
                        help="Number of tweets of each word per day")
    parser.add_argument('-p', '--path_to_save_xlsx', required=True,
                        help="Path to save output file containing all the results.")
    args = parser.parse_args()

    api = TwitterClient()
    api.list_of_words = args.list
    api.data_base_tweets(num_tweets_word_by_day=int(args.num_tweets_each_word_per_day),
                         path_to_save=args.path_to_save_xlsx)

# python twitter_extract.py --list vacinação coronavac -n 1 -p "C:/Users/UserVert/Desktop/all/sentiment_analysis_twitter/dfs/"