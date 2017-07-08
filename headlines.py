# encoding=utf-8
# Created by {donglida} on {17-7-1} {下午1:27}
import urllib.request
import urllib.parse
import feedparser
from flask import Flask, json
from flask import render_template
from flask import request

app = Flask(__name__)

RSS_FEEDS = {'bbc': 'http://feeds.bbci.co.uk/news/rss.xml', 'python': 'http://feeds.memect.com/py.rss.xml',
             'fox': 'http:/feeds.foxnews.com/foxnews/latest', 'iol': 'http://www.iol.co.za/cmlink/1.640'}

DEFAULTS = {'publication': 'bbc', 'city': 'London,UK'}


@app.route("/")
def home():
    # get customized headlines, based on user input or default
    publication = request.args.get('publication')
    if not publication:
        publication = DEFAULTS['publication']
    articles = get_news(publication)
    # get customized weather based on user input or default
    city = request.args.get('city')
    if not city:
        city = DEFAULTS['city']
    weather = get_weather(city)
    return render_template('home.html', articles=articles, weather=weather)


def get_news(query):
    if not query or query.lower() not in RSS_FEEDS:
        publication = DEFAULTS['publication']
    else:
        publication = query.lower()
    feed = feedparser.parse(RSS_FEEDS[publication])
    return feed['entries']


def get_weather(query):
    api_url = " http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=982b3de862cbb7c009e4d093cd507d19"
    query = urllib.parse.quote(query)
    url = api_url.format(query)
    data = urllib.request.urlopen(url).read()
    parsed = json.loads(data)
    weather = None
    if parsed.get("weather"):
        weather = dict(description=parsed["weather"][0]["description"], temperature=parsed["main"]["temp"],
                       city=parsed["name"])
    return weather


if __name__ == "__main__":
    app.run(port=5000, debug=True)
