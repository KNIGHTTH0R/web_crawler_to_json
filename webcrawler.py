#!/usr/bin/python
# -*- coding: utf-8 -*-

import feedparser
import json
from collections import OrderedDict
from bs4 import BeautifulSoup

class WebCrawler:
    def __init__(self, url):
        self.url  = url

    def build_data(self):
        feed = self.__parse_url()

        data = {'feed': []}
        for post in feed.entries:
            item = OrderedDict()
            item['title']       = post.title
            item['link']        = post.link
            item['description'] = self.__parse_description(post.description)

            data['feed'].append({'item': item})

        return data

    def dump_data(self, data):
        return json.dumps(data, indent=4, ensure_ascii=False)

    def data_to_file(self, data):
        with open('data.json', 'w') as outfile:
            json.dump(data, outfile)

    def __parse_url(self):
        return feedparser.parse(self.url)

    def __parse_description(self, description):
        description = description.replace('<p>\n\t&nbsp;</p>', '').replace('\n', '').replace('\t', '')

        items = []
        parsed_html = BeautifulSoup(description, 'html.parser')

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
