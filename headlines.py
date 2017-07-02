# encoding=utf-8
# Created by {donglida} on {17-7-1} {下午1:27}

import feedparser
from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)

RSS_FEEDS = {'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',\
                'python': 'http://feeds.memect.com/py.rss.xml',\
                'fox': 'http:/feeds.foxnews.com/foxnews/latest',\
                'iol': 'http://www.iol.co.za/cmlink/1.640'}

@app.route("/")
@app.route('/<publication>')
def get_news():
    query = request.args.get('publication')
    if not query or query.lower() not in RSS_FEEDS:
        publication = "bbc"
    else:
        publication = query.lower()
    feed = feedparser.parse(RSS_FEEDS[publication])
    first_article = feed['entries'][0]
    return render_template('home.html', articles=feed['entries'])

if __name__ == "__main__":
    app.run(port=5000, debug=True)
