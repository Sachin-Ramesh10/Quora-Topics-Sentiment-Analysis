import requests
from bs4 import BeautifulSoup


def get_answers(ques, link):
      ans = ''
      a = []
      url = link
      print(url)
      k = url.rsplit('/', 1)[-1]
      print(k)
      r = requests.get(url)
      html_content = r.text
      soup = BeautifulSoup(html_content, 'lxml')
      p = soup.find_all('p')
      print(len(p))
      if len(p) >= 2:
         for i in range(1, len(p)):
            ans = ans + soup.find_all('p')[i].text
         print(ans)
         write_data(ques, k, ans)

      else:
         q = soup.find_all('span')
         for i in q:
            if i.has_attr('class'):
               if 'rendered_qtext' in i['class']:
                  a.append(i.text)
         print(a[1:])
         write_data(ques, k, a[1:])

import csv

def write_data(a, b, c):
    with open('Quora.csv', 'a', newline='', encoding= 'utf-8') as csvfile:
        fieldnames = ['Question', 'user', 'answer']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow({'Question': a, 'user': b, 'answer': c})