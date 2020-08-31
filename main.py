import sys
import tweepy
from textblob import TextBlob
from wordcloud import WordCloud
import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

def main():
    # Twitter API credentials
    # You will need a twitter account 
    # to get your own credentials 
    # these credentials will expire 
    consumer_key = 'ycEZMmO2frdqYsFQfYSZlEZzy'
    consumer_secret = 'r9aJEgLmvmPte9HslJoM37RyP5Gay1ZJ3NfSam67wMTPFmq7IY'
    access_token = '1197336121107050496-7OTvNKMk5Z1v4nwgjJCpzDaJE5gIdc'
    access_t_secret = 'Wc9IwyuX48jsKLnF2lsn679sZ03g6yXuy2KZthziMLbgP'


    #create the authentication object
    authenticate = tweepy.OAuthHandler(consumer_key, consumer_secret)

    #Set the access tokens
    authenticate.set_access_token(access_token, access_t_secret)

    #Create API object while passing in the auth info
    api = tweepy.API(authenticate, wait_on_rate_limit = True)

    #Extract 100 tweets from a hashtag
    hashtag = api.search(q=get_topic(), lang='en', result_type='recent', count=100)

    #Create a dataframe
    df = pd.DataFrame([tweet.text for tweet in hashtag], columns=['Tweets'])

    #Cleaning text
    df['Tweets'] = df['Tweets'].apply(clean_text)

    #Create the new colums
    df['Subjectivity'] = df['Tweets'].apply(get_subjectivity)
    df['Polarity'] = df['Tweets'].apply(get_polarity)
    df['Analysis'] = df['Polarity'].apply(analysis)

    get_most_used_words(df)
    get_sentimental_analyis(df)  


#Get the topic 
def get_topic():
    if len(sys.argv) > 1:
        topic = sys.argv[1]
        return topic
    else:
        topic = 'twitter'
        return topic

#Show the analysis
def get_sentimental_analyis(df):
    plt.figure(figsize=(8,6))
    plt.title('Sentiment Analysis')
    plt.xlabel('Sentiment')
    plt.ylabel('Counts')
    df['Analysis'].value_counts().plot(kind='bar')
    plt.xticks(rotation=0)
    plt.show()

#Show the most used word
def get_most_used_words(df):
    all_words = ' '.join( [twts for twts in df['Tweets']] )
    word_cloud = WordCloud(width=500, height=300, random_state= 21, max_font_size=119).generate(all_words)

    plt.imshow(word_cloud, interpolation= 'bilinear')
    plt.axis('off')
    plt.show()

#Sentiment analysis
def analysis(score):
    if score < 0:
        return 'Negative'
    elif score == 0:
        return 'Neutral'
    else:
        return 'Positive'

# Create a function to get the subjectivity
def get_subjectivity(text):
    return TextBlob(text).sentiment.subjectivity

# Create a function to get the polarity
def get_polarity(text):
    return TextBlob(text).sentiment.polarity

#Create a function to clean the text
def clean_text(text):
    text = re.sub(r'@[A-za-z0-9]+', '', text) # removing @metions
    text = re.sub(r'#', '', text) # removing the '#' symbol
    text = re.sub(r'RT[\s]+', '', text) #removing RT's
    text = re.sub(r'https?:\/\/?', '', text) #removing links

    return text


if __name__ == '__main__':
    main()
    
