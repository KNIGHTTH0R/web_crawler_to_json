#!/usr/bin/python
# -*- coding: utf-8 -*-

import feedparser
import json
from collections import OrderedDict
from bs4 import BeautifulSoup

def main():
    url = 'http://revistaautoesporte.globo.com/rss/ultimas/feed.xml'
    feed = feedparser.parse(url)

    data = {'feed': []}
    for post in feed.entries:
        item = OrderedDict()
        item['title']       = post.title
        item['link']        = post.link
        item['description'] = parse_description(post.description)

        data['feed'].append({'item': item})

    print json.dumps(data, indent=4, ensure_ascii=False)

    with open('data.json', 'w') as outfile:
        json.dump(data, outfile)

def parse_description(content):
    content = content.replace('<p>\n\t&nbsp;</p>', '').replace('\n', '').replace('\t', '')

    items = []
    parsed_html = BeautifulSoup(content, 'html.parser')

    paragraphs = parsed_html.find_all('p')
    for p in paragraphs:
        item = OrderedDict([('type', 'text')])
        item['content'] = p.text
        items.append(item)

    images = parsed_html.find_all('img')
    for img in images:
        if img.parent.name == 'div':
            item = OrderedDict([('type', 'image')])
            item['content'] = img['src']
            items.append(item)

    links = parsed_html.find_all('a')
    links_array = []
    for link in links:
        if link.parent.name == 'li':
            links_array.append(link['href'])

    if links_array:
        item = OrderedDict([('type', 'links')])
        item['content'] = links_array
        items.append(item)

    return items

main()
