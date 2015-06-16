import os
from flask import Flask,render_template
import psycopg2
import urlparse
import plist
import re
import tweepy
import json
from nltk.corpus import stopwords

app = Flask(__name__, static_folder="static",static_url_path="")
# Consumer keys and access tokens, used for OAuth
consumer_key = plist.consumer_key
consumer_secret = plist.consumer_secret
access_token = plist.access_token
access_token_secret = plist.access_token_secret

urlparse.uses_netloc.append("postgres")
url = urlparse.urlparse(os.environ["DATABASE_URL"])

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
        return True

    def on_error(self, status):
        print status
        return True

def word_magic(text):
    low=[]
    stop=stopwords.words('english')
    stop.append('rt')
    stop.append('#love')
    for dirtyword in text.split():
        word=re.sub('[!#$,*~.-?":()]','',dirtyword)
        if word.lower() not in stop and not word.startswith('@') and 'http' not in word and word != '':
           low.append(word)
    return(low)

@app.route('/')
def hello():
    l = StdOutListener()
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = tweepy.Stream(auth, l)
    stream.filter(track=['love','hate'])
    return render_template("presentation.html")