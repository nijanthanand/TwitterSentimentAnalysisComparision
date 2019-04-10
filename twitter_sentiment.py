from textblob import TextBlob
from wordcloud import WordCloud,STOPWORDS
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import tweepy
import os
currdir=os.path.dirname(__file__)

consumer_key = "FiUVp423ot8jHrIcNMlwY7RnT"
consumer_secret = "fe2i5dmE8NlTtDmf2d9GQbbtUWGT7twTUqkbHlnZEhu9bilArV"
access_token = "128196352-S4SjqFEpxKMB7WNcOFEC9VpmW8z3AyplRUCszwAv"
access_token_secret = "57TIb9Q9xx3plDqc3n1HLhQYKOAmkJ4q5n3ljLqSHek7x"
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)   # Creating the authentication object
auth.set_access_token(access_token, access_token_secret)    # Setting your access token and secret
api = tweepy.API(auth)                                      # Creating the API object while passing in auth information

query1=input("What is the first Keyword to analyse:")       #Search Query 1
query2=input("What is the second Keyword to analyse:")      #Search Query 2

language = "en"                                             # Language code (follows ISO 639-1 standards)
tweetCount = 100
results1 = api.search(q=query1,count=tweetCount,lang=language)   # Calling the twitter api function with our parameters
results2 = api.search(q=query2,count=tweetCount,lang=language)   # Calling the twitter api function with our parameters

#We define the Sentiment function that displays the sentiment predictions and a Pie chart visualisation
def sentiment(query,results,number):
   sum1 = 0
   avg1 = 0
   positive1 = 0
   negative1 = 0
   neutral1 = 0
   for tweet in results:  # Find the tweets in the JSON file pulled from API
      a = TextBlob(tweet.text)  # Convert to TextBlob format
      sum1 += a.sentiment.polarity  # Add the polarity of all tweets parsed through the sentiment.polarity function
      if a.sentiment.polarity >= 0.05:
         positive1 += 1  # Tuned Sentiment as positive if polarity greater than 0.05
      elif a.sentiment.polarity < 0:
         negative1 += 1  # Tuned Sentiment as negative if polarity is lesser than 0
      else:
         neutral1 += 1  # Tuned Sentiment as neutral if polarity is between 0 and 0.05
   tweetCount = positive1 + negative1 + neutral1
   avg1 = sum1 / tweetCount  # Define the average polarity byy dividing sum with tweet count
   avg1 = format(avg1, ".2f")  # We make average a two decimal point float for printing purpose
   print("Sentiment Analysis of " + query)
   print("Number of positive Tweets is:" + str(positive1))
   print("Number of neutral Tweets is:" + str(neutral1))
   print("Number of negative Tweets is:" + str(negative1))
   print("Average Polarity of the Tweets is:" + str(avg1))
   positive_percentage = positive1 * 100 / tweetCount
   negative_percentage = negative1 * 100 / tweetCount
   neutral_percentage = neutral1 * 100 / tweetCount
   positive_percentage = format(positive_percentage, ".2f")   #format the percentage values to 2 digits
   negative_percentage = format(negative_percentage, ".2f")
   neutral_percentage = format(neutral_percentage, ".2f")
   ##Pie Chart of Sentiment Predictions
   plt.figure(number)   # Define the pie chart with number so we can call all pie charts created at once
   labels = ["Positive Tweets: " + str(positive_percentage) + "%", "Neutral Tweets: " + str(neutral_percentage) + "%",
             "Negative Tweets: " + str(negative_percentage) + "%"]   # Define the labels of the pie chart
   sizes = [positive1, neutral1, negative1]
   colors = ['darkgreen', 'orange', 'red']
   patches, texts = plt.pie(sizes, colors=colors, startangle=90)
   plt.legend(patches, labels, loc="best")
   plt.title("Tweet sentiments of " + query + ". Average Polarity=" + str(avg1) + ".")   #Display dynamic title based on query
   plt.tight_layout()
   plt.axis('equal')

sentiment(query1,results1,0)   #Call the sentiment analysis function
sentiment(query2,results2,1)
print("Sentiment Analysis has been Completed, close the Pie charts visible to proceed for the WordCloud")
print("NOTE: WordCloud of the Top 100 words will be available in the directory only after you close the Pie Charts")
plt.show(2)

def wordcloudder(results1,ab):            # Function to displays top 100 words on Wordcloud in a Twitter mask
   x1 = ' '
   for tweet in results1:                 # Find the tweets in the JSON file pulled from API
      print(tweet.text)                   # Print the Retrived Tweets
      x1 = x1 + tweet.text
   from wordcloud import WordCloud, STOPWORDS
   stopwords=set(STOPWORDS)               # Define the stopwords we don't want in the Wordcloud image
   mask=np.array(Image.open(os.path.join(currdir,"twitter_mask.png")))
   wc=WordCloud(background_color='white',max_words=100,stopwords=stopwords,mask=mask)
   wc.generate(x1)                        # Generate the wordcloud based on the above parameters
   wc.to_file(os.path.join(currdir,ab))   # Save the Wordcloud image at path currdir with the name ab

wordcloudder(results1,query1+'.png')   #call the wordcloud function
wordcloudder(results2,query2+'.png')

print("Sentiment Analysis completed. Please check in directory:"+ currdir)