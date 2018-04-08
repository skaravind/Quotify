from bs4 import BeautifulSoup as bfs
import requests
import random

def quotify(word):
    word_list = list(word.split(' '))
    if len(word_list) <= 2:
        pass
    else:
        word = word_list[-1]
    page = requests.get('https://www.brainyquote.com/search_results?q='+word)
    soup = bfs(page.text, 'html.parser')
    try:
        word = word.lower()
        quotelist = soup.find(id='quotesList')
        quotes = quotelist.find_all(title='view quote')
        authors = quotelist.find_all(title='view author')
        choice = int(len(quotes)*(random.random())) - 1
        quote = quotes[choice].contents[0]
        author = authors[choice].contents[0]
        if len(word_list)<=2 and (word not in quote):
           return quotify(word_list[-1])
        first = quote[:quote.lower().find(word)]
        keyword = quote[quote.lower().find(word):quote.lower().find(word)+len(word)]
        second = quote[quote.lower().find(word)+len(word):]
        result = [first,keyword,second,author]
        #print('"%s"\n-"%s"'%(result['quote'],result['author']))
    except Exception as e:
        print(str(e))
        result = 0

    return result
