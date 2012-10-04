import urllib 
import summarize
import re
import json
from bs4 import BeautifulSoup
from HTMLParser import HTMLParseError

from content_parser import parse, parse2

def run():
    url = 'http://api.ihackernews.com/page'
    try:
        data = json.load(urllib.urlopen(url))
    except ValueError:
        print 'Page not available'
        return

    for item in data['items']:
        print item['title']
        print gistof(item['url'])
        print '\n\n'


def gistof(url):
    #content = parse(url)
    content = parse2(url)
    content = content.replace('  ',' ')
    content = content.replace('  ',' ')
    summarizer = summarize.SimpleSummarizer()
    summary = summarizer.summarize(content, 3)
    return summary

if __name__ == '__main__':
    run()
