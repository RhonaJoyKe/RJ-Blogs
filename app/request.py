import urllib.request
import json
from .models import Quotes

base_url_quotes = None

def configure_request(app):
    global  base_url_quotes
    base_url_quotes = app.config['QUOTES_API_URL']
    

def get_quote():
    '''
    Function that gets the json response to our url request
    '''
    get_quote_url = 'http://quotes.stormconsultancy.co.uk/random.json'

  
    print(get_quote_url)
    with urllib.request.urlopen(get_quote_url) as url:
        get_quote_data = url.read()
        quote_response = json.loads(get_quote_data)

      

        if quote_response:
            author=quote_response['author']
            quote=quote_response['quote']
            url=quote_response['permalink']

        new_quote=Quotes(author,quote,url)
    return new_quote
#processing the source results
