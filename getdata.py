import matplotlib.pyplot as plt
from wordcloud import WordCloud
import psycopg2
import plist
import re
import tweepy
import json
from nltk.corpus import stopwords

# Consumer keys and access tokens, used for OAuth
consumer_key = plist.consumer_key
consumer_secret = plist.consumer_secret
access_token = plist.access_token
access_token_secret = plist.access_token_secret
for_word_cloud=[]
numoftweets=0

con = psycopg2.connect(
    database="dcq831hkco5on8",
    user="tyderfzsicjagq",
    password="2FyTBBWnZgLDAU_rWICXUk5bDw",
    host="ec2-174-129-26-115.compute-1.amazonaws.com",
    port="5432"
)
cur=con.cursor()

class StdOutListener(tweepy.StreamListener):
    def on_data(self, data):
        # Twitter returns data in JSON format - we need to decode it first
        decoded = json.loads(data)
        if 'limit' in decoded:
            return True
        user=decoded['user']['screen_name'].encode('ascii','ignore')
        tweet=decoded['text'].encode('ascii','ignore')
        if 'limit' in decoded:
            return True
        if decoded['text']:
            low=word_magic(decoded['text'].encode('ascii', 'ignore'))
        # Also, we convert UTF-8 to ASCII ignoring all bad characters sent by users
        if decoded['user']['screen_name'] and decoded['text']:
            print '@%s: %s' % (decoded['user']['screen_name'], decoded['text'].encode('ascii', 'ignore'))
        slow=' '.join(low)
        entry=(user,tweet,slow)
        query='INSERT INTO tweets ("user","tweet", "low") VALUES (%s,%s,%s);'
        cur.execute(query,entry)
        con.commit()
        wc=add_word_cloud(low)
        createwc(wc)
        return True

    def on_error(self, status):
        print status
        return True

def add_word_cloud(tags):
    for_word_cloud.extend(tags)
    return for_word_cloud

def createwc(words):
    global numoftweets
    numoftweets +=1
    listtostring=' '.join(words)
    print listtostring
    print
    wcspec=WordCloud(ranks_only=True,background_color="white", max_words=2000)
    wordcloud=wcspec.generate(listtostring)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.draw()
    title= "Number of Tweets "+ str(numoftweets)
    plt.suptitle(title)
    #title="static/test"+str(numoftweets)+".png"
    plt.savefig("static/wordcloud.png")
    #plt.show()
    return True

def word_magic(text):
    low=[]
    stop=stopwords.words('english')
    stop.append('rt')
    stop.append('#love')
    stop.append('amp')
    for dirtyword in text.split():
        word=re.sub('[!#$,*~.-?":()]','',dirtyword)
        if word.lower() not in stop and not word.startswith('@') and 'http' not in word and word != '':
           low.append(word)
    return(low)

if __name__ == '__main__':
    l = StdOutListener()
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = tweepy.Stream(auth, l)
    stream.filter(track=['love'])

