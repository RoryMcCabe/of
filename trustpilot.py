# -*- coding: utf-8 -*-
"""
Created on Fri May 31 12:07:03 2019

@author: McCabeR
"""

import requests, re, pandas as pd, numpy as np, wordcloud
from collections import Counter
from bs4 import BeautifulSoup
from datetime import datetime
from dateutil import parser
import matplotlib.pyplot as plt

url1 = 'https://uk.trustpilot.com/review/www.edfenergy.com' #?page=144
url2 = 'http://2.python-requests.org/en/v1.0.0/api/'
url3 = 'https://www.google.co.uk/'
url4 = 'https://en.wikipedia.org/wiki/Wiki'
r2 = requests.get(url2)
print(r2.status_code)
r4 = requests.get(url4)
print(r4.status_code)
r3 = requests.get(url3)
print(r3.status_code)
r1 = requests.get(url1) # 2:50 on Fri 7/6/19
edf = r1.text

result = re.findall('class', edf)
keyword = 'class'
before_keyword, keyword, after_keyword = edf.partition(keyword)
before_keyword
keyword
after_keyword

soup = BeautifulSoup(edf, 'html.parser')
comment = soup.find_all('p', class_ = "review-content__text")
print(len(comment)) # 20
print(comment[0])

reviews = pd.DataFrame(index=range(20), columns=['rating', 'comment'])
comment = soup.find_all('div', class_ = "star-rating")
#print(len(comment)) # 20
#print(comment[0])
#for i in range(22): print(comment[i])
#str(comment)[25:38]
before_keyword, keyword, after_keyword = str(comment).partition('star-rating--medium')
reviews.rating[0] = before_keyword[-2:-1]
for i in range(19):
    before_keyword, keyword, after_keyword = after_keyword.partition('star-rating--medium')
    reviews.rating[i+1] = before_keyword[-2:-1]
comment = soup.find_all('p', class_ = "review-content__text")
reviews.comment[0] = str(comment[0])
for i in range(19):
    reviews.comment[i+1] = str(comment[i+1])

text = reviews.comment[0]
for char in '-.,/\n(){}[]<>"=0123456789_': text=text.replace(char,' ')
word_list = text.lower().split()
Counter(word_list).most_common(10)

##### ##### ##### #####

Company = 'www.edfenergy.com'#britishgas.co.uk'
Top = 20

pages=1
url = "https://uk.trustpilot.com/review/" + Company + "?page=" + str(pages)
edf = pd.Series(index=range(1)) # hard-wired ...
bgas = pd.Series(index=range(1)) # hard-wired ...
while True:
    page = requests.get(url)
    edf[pages-1]=page.text
    if requests.head(url).status_code != 200:
        break
    pages = pages+1
    url = "https://uk.trustpilot.com/review/" + Company + "?page=" + str(pages)
# 84 sec for 0 to 151 EDF pages

pages=151-1 # 154 312 # needed in office for now, last page may be repeat of first
reviews = pd.DataFrame(index=range(pages*20), columns=['rating', 'comment', 'timestamp'])
for i in range(pages):
    soup = BeautifulSoup(edf[i], 'html.parser')
    star = soup.find_all('div', class_ = "star-rating")
    comment = soup.find_all('p', class_ = "review-content__text")
    before_keyword, keyword, after_keyword = str(star).partition('star-rating--medium')
    reviews.rating[i*20] = before_keyword[-2:-1]
    reviews.comment[i*20] = str(comment[0])
    header = soup.find_all('div', class_ = "review-content-header")
    reviews.timestamp[i*20] = parser.parse(str(header[0])[1046:1056])
    for j in range(19):
        before_keyword, keyword, after_keyword = after_keyword.partition('star-rating--medium')
        if before_keyword[-2:-1] in ['1','2','3','4','5']:
            reviews.rating[i*20+j+1] = before_keyword[-2:-1]
            reviews.comment[i*20+j+1] = str(comment[j+1])
            reviews.timestamp[i*20+j+1] = parser.parse(str(header[j+1])[1046:1056])
        else:
            reviews.rating[i*20+j+1] = 'out of range'
            reviews.comment[i*20+j+1] = 'not applicable'
            reviews.timestamp[i*20+j+1] = datetime.strptime("1900-01-01", "%Y-%m-%d")

reviews=reviews[reviews.rating != 'out of range']
tot=len(reviews)

sum(reviews.rating=='1')*100/sum(reviews.rating!='out of range') # 928 =  30.7 to 30.8 %
sum(reviews.rating=='2')*100/sum(reviews.rating!='out of range') # 125  =  4.1 to  4.2 %
sum(reviews.rating=='3')*100/sum(reviews.rating!='out of range') # 85 =    2.8 to  2.8 %
sum(reviews.rating=='4')*100/sum(reviews.rating!='out of range') # 216 =   7.2 to  7.2 %
sum(reviews.rating=='5')*100/sum(reviews.rating!='out of range') # 1657 = 54.9 to 55.0 %
reviews.rating.unique() # 7 -> 5 and oor BG: 266 oor and 279 on = nan
#sum(reviews.rating=='>') # 1 @ 2991
#sum(reviews.rating=='') # 8 @ 2992-2999
sum(reviews.rating=='out of range') # 9 @ 2991-2999 to 2
sum(reviews.rating!='out of range') # 3011 to 3078

text1, text2, text3, text4, text5 = '','','','',''
for i in range(tot):
    if reviews.rating[i]=='1': text1 = text1 + reviews.comment[i]
    if reviews.rating[i]=='2': text2 = text2 + reviews.comment[i]
    if reviews.rating[i]=='3': text3 = text3 + reviews.comment[i]
    if reviews.rating[i]=='4': text4 = text4 + reviews.comment[i]
    if reviews.rating[i]=='5': text5 = text5 + reviews.comment[i]
for char in '-.,/\n(){}[]<>"=0123456789_!#$%&*+:;?@^`¬~|':
    text1 = text1.replace(char,' ')
    text2 = text2.replace(char,' ')
    text3 = text3.replace(char,' ')
    text4 = text4.replace(char,' ')
    text5 = text5.replace(char,' ')
len(text1.lower().split()) # 115,910 to 115,737 Note: more words in '1' feedback
len(text2.lower().split()) # 15,177
len(text3.lower().split()) # 6,502
len(text4.lower().split()) # 12,072
len(text5.lower().split()) # 74,665
 
Counter(text1.lower().split()).most_common(Top)
Counter(text2.lower().split()).most_common(Top)
Counter(text3.lower().split()).most_common(Top)
Counter(text4.lower().split()).most_common(Top)
Counter(text5.lower().split()).most_common(Top)

dropwords = ('to', 'i', 'the', 'and', 'a', 'br', 'p', 'they', 'my', 'of', 'have', 'for', 'with', 'in', 'was', 'on', 'me', 'that', 'it', 'this', 'not', 'them', 'is', 'you', 'had', 'be', 'as', 'are', 'no', 'so', 'from', 'we', 'but', 'an', 'when', 'will', 'then', 'their', 'would', 'get', 'if', 'just', 'at', 'by', 'or', 'review', 'text', 'content', 'class', 'been', 'all', 'now', 'do', 'after', 'out', 'told', 'one', 'over', 'which', 'has', 'what', 'even', 'am', 'your', 'about', 'can', 'where', 'there', 'could', 'more', 'were')
words1 = [word for word in text1.lower().split() if word.isalpha()] # remove 2504 ~ 2.16 %
words11 = [w for w in words1 if not w in dropwords]
most1 = Counter(words11)
most1.most_common(20)
words2 = [word for word in text2.lower().split() if word.isalpha()] # remove 2504 ~ 2.16 %
words22 = [w for w in words2 if not w in dropwords]
most2 = Counter(words22)
most2.most_common(20)
words3 = [word for word in text3.lower().split() if word.isalpha()] # remove 2504 ~ 2.16 %
words33 = [w for w in words3 if not w in dropwords]
most3 = Counter(words33)
most3.most_common(20)
words4 = [word for word in text4.lower().split() if word.isalpha()] # remove 2504 ~ 2.16 %
words44 = [w for w in words4 if not w in dropwords]
most4 = Counter(words44)
most4.most_common(20)
words5 = [word for word in text5.lower().split() if word.isalpha()] # remove 2504 ~ 2.16 %
words55 = [w for w in words5 if not w in dropwords]
most5 = Counter(words55)
most5.most_common(20)

(most1 - most2).most_common(20) # and +
(most1 & most2).most_common(20) # and |

#diff = pd.Series(index=range(pages*20))
#for i in range(pages*20): diff[i] = (datetime.now() - reviews.timestamp[i]).days
def qdate(qd):
    c1, c2, c3, c4, c5 = 0, 0, 0, 0, 0
    for i in range(tot):
        if reviews.timestamp[i] < datetime.strptime(qd,"%Y-%m-%d"): break
        else:
            if reviews.rating[i] == '1': c1 +=1
            elif reviews.rating[i] == '2': c2 +=1
            elif reviews.rating[i] == '3': c3 +=1
            elif reviews.rating[i] == '4': c4 +=1
            elif reviews.rating[i] == '5': c5 +=1
    return(c1, c2, c3, c4, c5)

#reviews.timestamp.unique()
min(reviews.timestamp)
qdate("2019-06-14") # 0 1 0 0 21
qdate("2019-06-01") # 8 4 2 4 181
qdate("2019-05-01") # 44 10 8 20 461
qdate("2019-01-01") # 272 50 48 102 1289
qdate("2018-01-01") # 637 71 53 119 1340
qdate("2010-05-20") # 927 124 85 216 1638
qdate("1800-05-20") # 928 125 85 216 1657

level = 5 # 1 to 5
bar = pd.Series(index=range(12))
bar[0] = qdate("2018-01-01")[level-1] - qdate("2018-02-01")[level-1]
bar[1] = qdate("2018-02-01")[level-1] - qdate("2018-03-01")[level-1]
bar[2] = qdate("2018-03-01")[level-1] - qdate("2018-04-01")[level-1]
bar[3] = qdate("2018-04-01")[level-1] - qdate("2018-05-01")[level-1]
bar[4] = qdate("2018-05-01")[level-1] - qdate("2018-06-01")[level-1]
bar[5] = qdate("2018-06-01")[level-1] - qdate("2018-07-01")[level-1]
bar[6] = qdate("2018-07-01")[level-1] - qdate("2018-08-01")[level-1]
bar[7] = qdate("2018-08-01")[level-1] - qdate("2018-09-01")[level-1]
bar[8] = qdate("2018-09-01")[level-1] - qdate("2018-10-01")[level-1]
bar[9] = qdate("2018-10-01")[level-1] - qdate("2018-11-01")[level-1]
bar[10] = qdate("2018-11-01")[level-1] - qdate("2018-12-01")[level-1]
bar[11] = qdate("2018-12-01")[level-1] - qdate("2019-01-01")[level-1]
bar

plt.bar(np.arange(12), bar)
plt.ylabel('Number of ' + str(level) + ' star ratings')
plt.title('2018 variance in ' + str(level) + ' star ratings')
plt.xticks(np.arange(12), ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'))
plt.show()

bar2 = pd.Series(index=range(10))
bar2[0] = qdate("2018-01-01")[level-1] - qdate("2019-01-01")[level-1]
bar2[1] = qdate("2017-01-01")[level-1] - qdate("2018-01-01")[level-1]
bar2[2] = qdate("2016-01-01")[level-1] - qdate("2017-01-01")[level-1]
bar2[3] = qdate("2015-01-01")[level-1] - qdate("2016-01-01")[level-1]
bar2[4] = qdate("2014-01-01")[level-1] - qdate("2015-01-01")[level-1]
bar2[5] = qdate("2013-01-01")[level-1] - qdate("2014-01-01")[level-1]
bar2[6] = qdate("2012-01-01")[level-1] - qdate("2013-01-01")[level-1]
bar2[7] = qdate("2011-01-01")[level-1] - qdate("2012-01-01")[level-1]
bar2[8] = qdate("2010-01-01")[level-1] - qdate("2011-01-01")[level-1]
bar2[9] = qdate("2009-01-01")[level-1] - qdate("2010-01-01")[level-1]
bar2

plt.bar(np.arange(10), bar2)
plt.ylabel('Number of ' + str(level) + ' star ratings')
plt.title('Yearly variance in ' + str(level) + ' star ratings')
plt.xticks(np.arange(10), ('2018', '2017', '2016', '2015', '2014', '2013', '2012', '2011', '2010', '2009'))
plt.show()

def keyplot(keyword):
    y=pd.Series(index=range(5))
    y[0]=Counter(words11)[keyword]
    y[1]=Counter(words22)[keyword]
    y[2]=Counter(words33)[keyword]
    y[3]=Counter(words44)[keyword]
    y[4]=Counter(words55)[keyword]
    x=['1star', '2star', '3star', '4star', '5star']
    plt.plot(x,y)
    plt.xlabel("Star Ratings")
    plt.ylabel("Frequency")
    plt.title("Plot of keyword '" + keyword + "' frequency per star rating")
    plt.show()
    
keyplot('excellent')
keyplot('bad') # interesting u plot
keyplot('great')
keyplot('helpful')
keyplot('easy')

# cmd: pip install wordcloud ... collecting ... retrying x 5 ... 
# could not find a version that satisfies the requirement ... no matching distribution
# cmd: git clone https://github.com/amueller/word_cloud.git ... cloning ... 
# unable to access ... failed to connect port 443 ... timed out
# cmd: cd word_cloud
# cmd: pip install .
# cmd: conda install -c conda-forge wordcloud ... solving ...
# http connection failed ... timeout

wordcloud = wordcloud.WordCloud(width = 800, height = 800, background_color ='white', min_font_size = 10).generate(str(words55))
plt.figure(figsize = (8, 8), facecolor = None) 
plt.imshow(wordcloud) 
plt.axis("off") 
plt.tight_layout(pad = 0) 
plt.show()

if level == 1: two_words = [' '.join(ws) for ws in zip(words11, words11[1:])]
if level == 2: two_words = [' '.join(ws) for ws in zip(words22, words22[1:])]
if level == 3: two_words = [' '.join(ws) for ws in zip(words33, words33[1:])]
if level == 4: two_words = [' '.join(ws) for ws in zip(words44, words44[1:])]
if level == 5: two_words = [' '.join(ws) for ws in zip(words55, words55[1:])]
wordscount = {w:f for w, f in Counter(two_words).most_common() if f > 1}
dict(list(wordscount.items())[0:Top])

##### ##### ##### #####

stripped = re.sub('<[^<]+?>', '', edf)
print(stripped)
print("Last modified: " + r1.headers['last-modified'])
print("Content type: " + r1.headers['content-type'])
print("Content length: " + r1.headers['content-length'])

r = requests.post(url1, data={'page': 2})
print(r.status_code)

r1.json().get('hasMore')

r1.json
r1.headers

uh = urlopen(url3)
data = uh.read()
#data.encode('utf-8').strip()
print ('Retrieved',len(data),'characters')
import json
js = json.loads(data.decode("utf-8"))

s = requests.Session()
response = s.post(url4)
orderList = []
resp_json = response.json()
orderList.append(resp_json["orderItems"])
while resp_json.get('hasMore') == True:
    response = s.get(url1.format(resp_json['nextPageUrl']))
    resp_json = response.json()
    orderList.append(resp_json["orderItems"])

##### ##### ##### #####

tp1 = requests.get('https://uk.trustpilot.com/review/www.edfenergy.com')
tp2 = requests.get('https://uk.trustpilot.com/review/www.edfenergy.com?page=2')
tp3 = requests.get('https://uk.trustpilot.com/review/www.edfenergy.com?page=3')
tp4 = requests.get('https://uk.trustpilot.com/review/www.edfenergy.com?page=4')
tp5 = requests.get('https://uk.trustpilot.com/review/www.edfenergy.com?page=5')

print(r1.status_code) # 200
print(edf.index('edf')) # 4536
print(edf[4536:4539]) # edf
print(edf.count('edf')) # 64
print(edf.count('bad')) # 25
print(edf.count('excellent')) # 16
print(r1.request.body) # none
print(edf.count('headline')) # 26
print(edf.count('reviewRating')) # 20
print(edf.count('ratingValue')) # 21
print(edf.count('reviewCount')) # 6
print(edf.count('datePublished')) # 20
print(edf.count('reviewBody')) # 20

print(edf[edf.index('og:title')+19:edf.index('og:title')+42], edf[edf.index('og:title')+48:edf.index('og:title')+53], edf[edf.index('og:title')+64:edf.index('og:title')+87])
print(edf[edf.index('hear what')+10:edf.index('hear what')+25])
print(edf[edf.index(',"name":')+9:edf.index(',"name":')+22])
print(edf[edf.index(',"ratingValue":')+16:edf.index(',"ratingValue":')+19])
print(edf[edf.index(',"reviewCount":')+16:edf.index(',"reviewCount":')+20])

print(edf[edf.index(',"headline":')+12:edf.index(',"headline":')+32]) # values change
print(edf[edf.index(',"reviewBody":')+14:edf.index(',"reviewBody":')+215]) # values change

s = 'hear what'
result = re.findall(s, edf)
result2 = re.search(r'rated(.*?)quot', edf)
result3 = re.findall(r'content(.*?)Trustpilot', edf)
result3[2]
#result3 = re.search(r'(?m)^\Content.*(?:\r?\n(?!\>.*)*', edf)
#(?<=@\(posedge).*?(\!\(\$isunknown\(.*?\)\)).*?\|->
len(result)
print(result[0])
print(result[1])
print(result2.group(0))
print(result2.group(1)) # string between rated and quot


#from lxml import html
#tree = html.fromstring(r1.content)
#links = tree.xpath('//link[@rel="next"]/text()')

soup = BeautifulSoup(edf, 'html.parser')
soup

text = soup.text
for char in '-.,/\n(){}[]': text=text.replace(char,' ')
word_list = text.lower().split()
Counter(word_list).most_common()[0:10]



str(soup)
soup.title
print(soup.title)
soup.title.text
soup.p
rev1=soup.p.text
print(soup.prettify())
print(soup.get_text())
soup.find_all('a')
for link in soup.find_all('a'): print(link.get('href'))
soup.title.name
t=soup.title.string
soup.title.parent.name
soup.p['class']
soup.a
soup.b
soup.find_all('a')
soup.find(id="headline")
soup.head
soup.head.contents # list [0] to [33]
soup.head.contents[17].contents # 19 21 25 27 33
soup.head.contents[17].string
bod=soup.body
soup.body.a
soup.body.b
len(soup.contents) # 4 = 0 1 2... 3
soup.contents[0]
for string in soup.strings: print(repr(string))
soup.find_all(['a', 'b']) # either
for tag in soup.find_all(re.compile("^h")): print(tag.name) # remove caret for contains
for tag in soup.find_all(True): print(tag.name)
soup.find_all("title")
soup.find_all("p", "title")
soup.find_all("a") # equiv to soup("a")
soup.find_all(id="link2")
soup.find(string=re.compile("ratingValue")) # 16099 char Nav string
ti=soup.find(string=re.compile("title")) # 8231 char Nav string
soup.find_all(href=re.compile("user-guidelines"))
soup.find_all(id=True) # 21 ResultSet

soup.find_all(string="ratingValue")
soup.find_all(string=["Tillie", "Elsie", "Lacie"])
rating=soup.find_all(string=re.compile(',"ratingValue":'))
def is_the_only_string_within_a_tag(s):
    """Return True if this string is the only child of its parent tag."""
    return (s == s.parent.string)
soup.find_all(string=is_the_only_string_within_a_tag, limit=2) # 366 and find() equiv to limit=1
from bs4 import SoupStrainer
only_a_tags = SoupStrainer("a")

json_data = r1.json()
for k,v in json_data.items():
    print(k + ':' + v)

print(r2.text)
print(r4.text)
print(r3.text)
print(edf)

from urllib.request import urlretrieve, urlopen
urlretrieve(url4, 'testurl1.csv')
html = urlopen(url1)

r=requests.get('https://api.github.com/')

from requests.adapters import HTTPAdapter
s = requests.Session()
s.mount('http://', HTTPAdapter(max_retries=15))
s.mount('https://', HTTPAdapter(max_retries=15))
requests.adapters.DEFAULT_RETRIES = 5

import http.client #httplib
con = http.client.HTTPSConnection('www.google.com', port=8443)
con.request("GET", "/")
res = con.getresponse()
print(res.read())