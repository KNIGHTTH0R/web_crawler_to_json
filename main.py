#!/usr/bin/python
# -*- coding: utf-8 -*-

from webcrawler import WebCrawler

def main():
    url = 'http://revistaautoesporte.globo.com/rss/ultimas/feed.xml'
    crawler = WebCrawler(url)
    data = crawler.build_data()

    crawler.data_to_file(data)
    print crawler.dump_data(data)

main()
