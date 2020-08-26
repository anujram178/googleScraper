import urllib
import requests
from bs4 import BeautifulSoup
import re

class Search:
    def __init__(self):
        pass
    def scrapeResults(self, query):
        # desktop user-agent
        USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
        # mobile user-agent
        MOBILE_USER_AGENT = "Mozilla/5.0 (Linux; Android 7.0; SM-G930V Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.125 Mobile Safari/537.36"

        query = query.replace(' ', '+')
        URL = f"https://google.com/search?q={query}"

        headers = {"user-agent": USER_AGENT}
        resp = requests.get(URL, headers=headers)

        if resp.status_code == 200:
            soup = BeautifulSoup(resp.content, "html.parser")
            results = []
            for g in soup.find_all('div', class_='r'):
                anchors = g.find_all('a')
                if anchors:
                    link = anchors[0]['href']
                    title = g.find('h3').text
                    item = {
                        "title": title,
                        "link": link
                    }
                    results.append(item)
            return results

    def getLeftover(self, url):
        indexOfLastPeriod = url.rfind('.')
        domainName = re.findall('^([\w\-]+)', url[indexOfLastPeriod+1:])
        domainName = domainName[0]
        leftover = re.sub(domainName,"",url[indexOfLastPeriod+1:],count=1)
        return leftover.lower()

    def removeHomeFromLeftover(self, leftover):
        if 'home' in leftover:
            if '/' == leftover[0]:
                leftover = re.sub("/","", leftover, count = 1)
            leftover = re.sub("home","",leftover,count=1)
        return leftover


    def findUrl(self, results):
        urlDict = {}
        resultsSeen = 0
        for result in results:
            if 'wikipedia' in result['link']:
                urlDict['exists'] = False
                return urlDict
            else:
                leftover = self.getLeftover(result['link'])
                leftover = self.removeHomeFromLeftover(leftover)
                if leftover == '' or leftover == '/':
                    urlDict['exists'] = True
                    urlDict['link'] = result['link']
                    return urlDict
                else:
                    pass
            resultsSeen += 1
            if resultsSeen == 4:
                urlDict['exists'] == False
                return urlDict      




# print(removeHomeFromLeftover(getLeftover('https://www.hamptoncountysc.org/439/Varnville')))
# print(removeHomeFromLeftover(getLeftover('http://www.varnvillesc.org/page/government')))

# query =  "town of varnville sc"
# results = scrapeResults(query)

# urlDict = findUrl(results)      ''' urlDict has 2 keys:
#                                 'exists' which is either 0 if url exists otherwise -1;
#                                 'link' which containts the url of the website'''

# if urlDict['exists'] == True:
#     print(urlDict['link'])

# for result in results:
#     print(result['title'], ":\n", result['link'])



