#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Alien'
__version__ = '1.0'
__doc__ = '''
Simple Wikipedia Crawler

A simple crawler for Wikipedia.
Given a page title it generates
a list of links found in that page and
crawls the first one.
'''

import wikipedia
import codecs
import Queue


class Crawler:
    def __init__(self):

        self.depth_counter = 0
        self.tested_pages = set()
        self.list_links = set()
        self.links_queue = Queue.Queue(0)


    def crawl(self, link, depth):

        if depth < self.depth_counter:
            return

        file_link = codecs.open(link.title() + ' links.txt', 'w', 'utf-8')

        for url in self.get_links(link):
            self.links_queue.put(url)
            print (link.title() + ' --> ' + url)
            file_link.write(link.title() + ' --> ' + url + '\n')

        self.depth_counter += 1

        try:
            self.crawl(self.links_queue._get(), depth)
        except (IOError, RuntimeError):
            print 'Some kind of error happened'

        except (wikipedia.DisambiguationError):
            print 'Disambiguation Error'
            print wikipedia.DisambiguationError.__unicode__()

        except (wikipedia.PageError):
            print wikipedia.PageError.__unicode__()
            self.crawl(self.links_queue._get(), depth)

    def get_links(self, wiki_page):

        if wiki_page.title() in self.tested_pages:
            raise IOError('Link already found')

        self.tested_pages.add(wiki_page.title())

        wiki_links = wikipedia.WikipediaPage(wiki_page.title()).links

        return wiki_links


def main():

    WikiCrawler = Crawler()

    input_wiki_page = raw_input('Which Wikipedia page should I start from? ')

    try:
        crawling_depth = int(raw_input('Tell me a number to let me know how deep the rabbit hole should I go. '))
    except ValueError:
        crawling_depth = 1

    try:

        WikiCrawler.crawl(input_wiki_page, crawling_depth)

    except KeyboardInterrupt:
        print 'Program stopped.'
    except StandardError:
        print 'End!'



if __name__ == '__main__':
    main()