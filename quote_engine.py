import requests
import json
import time


def get_quote(lang):
    params = {
        'method': 'getQuote',
        'lang': lang,
        'format': 'json'
    }
    res = requests.get('http://api.forismatic.com/api/1.0/', params)
    json_text = json.loads(res.text)
    time.sleep(2)
    return json_text["quoteText"], json_text["quoteAuthor"]
