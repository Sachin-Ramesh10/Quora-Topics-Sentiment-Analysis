from queue import Queue
from spider import *

PROJECT_NAME = 'Kashmir_Conflict_AllQuestions'
HOMEPAGE = 'https://www.quora.com/topic/Kashmir-Conflict/all_questions'
DOMAIN_NAME = get_domain_name(HOMEPAGE)
QUEUE_FILE = PROJECT_NAME + '/queue.txt'
CRAWLED_FILE = PROJECT_NAME + '/crawled.txt'
queue = Queue()
Spider(PROJECT_NAME, HOMEPAGE, DOMAIN_NAME)

def crawl():
    queued_links = file_to_set(QUEUE_FILE)
    if len(queued_links) > 0:
        print(str(len(queued_links)) + ' links in the queue')

crawl()
