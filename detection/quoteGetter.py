from bs4 import BeautifulSoup as bfs
import requests
import random

def quotify(word):
    page = requests.get('https://www.brainyquote.com/search_results?q='+word)
    soup = bfs(page.text, 'html.parser')
    try:
        quotelist = soup.find(id='quotesList')
        words_list = list(word.split(' '))
        quotes = quotelist.find_all(title='view quote')
        authors = quotelist.find_all(title='view author')
        choice = int(len(quotes)*(random.random()))
        quote = quotes[choice].contents[0]
        author = authors[choice].contents[0]
        for word in words_list:
            first = quote[:quote.lower().find(word)]
            keyword = quote[quote.lower().find(word):quote.lower().find(word)+len(word)]
            second = quote[quote.lower().find(word)+len(word):]
            result = [first,keyword,second,author]
            break
        #print('"%s"\n-"%s"'%(result['quote'],result['author']))
    except:
        result = 0

    return result
