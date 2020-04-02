import argparse
import bs4
import graphviz as gv
import random
import requests
import re
import time
import yaml


class Crawler:

    douban_url = 'https://www.douban.com'

    def __init__(self, group_id, creds):
        self.group_id = group_id
        self.headers = creds['headers']
        self.cookies = creds['cookies']
        self.user_map = {}
        self.user_contacts = {}

    def getUserId(user_url):
        match = re.search('https://www.douban.com/people/(.*)/', user_url)
        if match:
            return match.group(1)
        return None

    def output_name(self):
        return 'output/' + self.group_id + '.gv'

    def crawlMembers(self):
        url = Crawler.douban_url + '/group/' + self.group_id + '/members'
        while url:
            print('Scraping page: ' + url)
            re = requests.get(url, cookies=self.cookies, headers=self.headers)
            soup = bs4.BeautifulSoup(re.content, 'html.parser')
            for user in soup.findAll('div', {'class': 'name'}):
                user_name = user.find('a').string
                user_url = user.find('a').get('href')
                user_id = Crawler.getUserId(user_url)
                if user_id:
                    self.user_map[user_id] = user_name
            # Break if it's the last page.
            if not soup.find(rel='next'):
                break
            url = soup.find(rel='next').get('href')
            time.sleep(0.5 * random.random())
        print('Done crawling all memebers: ')
        print(self.user_map)

    def crawlContacts(self):
        for user in self.user_map:
            url = Crawler.douban_url + '/people/' + user + '/contacts'
            print('Scraping contacts: ' + url)
            re = requests.get(url, cookies=self.cookies, headers=self.headers)
            soup = bs4.BeautifulSoup(re.content, 'html.parser')
            ct_list = []
            for ct in soup.findAll('a', {'class': 'nbg'}):
                ct_id = Crawler.getUserId(ct.get('href'))
                if ct_id in self.user_map:
                    ct_list.append(ct_id)
            self.user_contacts[user] = ct_list
        print('Done crawling all contacts: ')
        print(self.user_contacts)

    def buildGraph(self):
        graph = gv.Digraph(comment=self.group_id, format = 'svg')
        self.crawlMembers()
        self.crawlContacts()
        for user in self.user_map:
            graph.node(user, self.user_map[user])
        for user in self.user_contacts:
            for ct in self.user_contacts[user]:
                graph.edge(user, ct)
        print(graph.source)
        graph.render(self.output_name())

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('group_id', help='Group ID of the interesting group.')
    parser.add_argument('credentials', help='File containing douban credentials.')
    args = parser.parse_args()
    with open(args.credentials) as f:
        creds = yaml.load(f, Loader=yaml.FullLoader)
    crawler = Crawler(args.group_id, creds)
    crawler.buildGraph()

if __name__ == '__main__':
    main()
