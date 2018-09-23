import requests
from lxml import html  
import json
import requests
import json
from dateutil import parser as dateparser
from time import sleep
import re

def get_products(product = "sprite"):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9) Gecko/2008051206 Firefox/3.0'}
    amazon_request = requests.post('https://www.amazon.com/s?k={}'.format(product), headers)
    if 'robot' in amazon_request.text:
        print('Product query failure: bot detected')
    return amazon_request.text

def parse_asins(items):
    #items.count('asin')
    unparsed_asins = [m.start() for m in re.finditer('asin', items)]
    #print(len(unparsed_asins))
    asins = []
    for a in range(len(unparsed_asins)):
        asin = items[unparsed_asins[a]+3:unparsed_asins[a]+18]
        #print(asin, end = ':\t')
        _asin = asin.split('=')
        if len(_asin) > 1:
            _asin = _asin[1].split('"')
        else:
            continue
        if len(_asin) > 1:
            _asin = _asin[1].split('&')[0]
        else:
            _asin = _asin[0].split('&')[0]
        asin = _asin.split(',')[0]
        #print(asin)
        prog = re.compile("[A-Z][0-9]+[A-Z]*.*")
        if prog.match(asin) is not None:
            asins.append(asin)
            #print(asin, end='')
        #print('')
    return asins

def get_product_reviews(asin):
    amazon_url  = 'http://www.amazon.com/dp/'+asin
    # Add some recent user agent to prevent amazon from blocking the request 
    # Find some chrome user agent strings  here https://udger.com/resources/ua-list/browser-detail?browser=Chrome
    headers = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9) Gecko/2008051206 Firefox/3.0'}
    page = requests.post(amazon_url,headers = headers,verify=False)
    if 'robot' in page.text:
        print('Product query failure: bot detected during review scraping')
    if 'data-hook="review-collapsed"' in page.text:
        _reviews = [m.start() for m in re.finditer('data-hook="review-collapsed"', page.text)]
        a, b, reviews = 114, 10000, []
        for r in range(len(_reviews)):
            reviews.append(page.text[_reviews[r]+a:min(_reviews[r]+(a+b), len(page.text))].split("</div>")[0])
        return reviews
    return None

def get_salience(comment):
    _url = 'https://language.googleapis.com/v1/documents:analyzeEntities?key=AIzaSyDHHCAG-BhRFaUxq2NRz2LG0tPiVNB4bos'
    _data = '{{\'document\': {{\'type\': \'PLAIN_TEXT\', \'content\': \'{}\'}}, \'encodingType\': \'UTF8\'}}'.format(comment.encode("utf-8").decode("utf-8"))
    r = requests.post(_url, data = _data)
    return r.json()

def get_sentiment(comment):
    perspective_url = 'https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key=AIzaSyDHHCAG-BhRFaUxq2NRz2LG0tPiVNB4bos'
    perspective_data = '{{comment: {{text: "{}"}}, languages: ["en"], requestedAttributes: {{TOXICITY:{{}}}}}}'.format(comment.encode("utf-8").decode("ascii","ignore"))
    r = requests.post(perspective_url, data = perspective_data)
    return r.json()

def extract_single_review_sentiment(product, item, review):
    #SANDWHICHONEAREYOU
    #I hope you hate me as much as i do
    return get_sentiment(get_product_reviews(parse_asins(get_products(product))[item])[review])

def get_product_sentiment(product, product_count):
    items = get_products(product)
    asins = parse_asins(items)
    item_reviews = []
    for asin in asins[:product_count]:
        #This is likely to get filtered for excessive querying
        item_reviews.append(get_product_reviews(asin))
    return item_reviews
    '''salience = []
    for item in item_reviews:
        for review in item:
            salience.append((get_sentiment(review), get_salience(review)))
    return salience'''
    
#items = get_products("sprite")
#asins = parse_asins(items)
#reviews = get_product_reviews(asins[1])
#sentiment = get_sentiment(reviews[1])
data = get_product_sentiment("soylent", 2)
data_string = ''
for row in data:
    for datum in row:
        data_string += datum