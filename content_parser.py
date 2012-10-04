#!/usr/bin/env python
import sys
from contextlib import closing

import lxml.html as html # pip install 'lxml>=2.3.1'
from lxml.html.clean        import Cleaner
from selenium.webdriver     import Firefox         # pip install selenium
from werkzeug.contrib.cache import FileSystemCache # pip install werkzeug

import contextlib

def parse(url):
    cache = FileSystemCache('.cachedir', threshold=100000)

    # get page
    page_source = cache.get(url)
    if page_source is None:
        # use firefox to get page with javascript generated content
        with closing(Firefox()) as browser:
            browser.get(url)
            page_source = browser.page_source
            cache.set(url, page_source, timeout=60*60*24*7) # week in seconds

    # extract text
    root = html.document_fromstring(page_source)
    # remove flash, images, <script>,<style>, etc
    Cleaner(kill_tags=['noscript'], style=True)(root) # lxml >= 2.3.1
    return root.text_content() # extract text

def parse2(url):
    ignore_tags=('script','noscript','style')
    fulltext = []
    with contextlib.closing(Firefox()) as browser:
        browser.get(url) # Load page
        content = browser.page_source
        cleaner = Cleaner()
        content = cleaner.clean_html(content)    
        source = content.encode('utf-8')
        doc = html.fromstring(content)
        
        for elt in doc.iterdescendants():
            if elt.tag in ignore_tags: continue
            text=elt.text or ''
            tail=elt.tail or ''
            words=' '.join((text,tail)).strip()
            if words:
                fulltext.append(words.encode('utf-8'))
    return '\n'.join(fulltext)

if __name__ == '__main__':
    url = sys.argv[1] if len(sys.argv) > 1 else "http://stackoverflow.com/q/7947579"
    print parse(url)
