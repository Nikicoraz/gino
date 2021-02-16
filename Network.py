import urllib.request

class AppURLopener(urllib.request.FancyURLopener):
    version = 'Mozilla/5.0'

def get_html(url):
    opener = AppURLopener()
    req = opener.open(url)
    return req.read().decode()

def get_request(url):
    opener = AppURLopener()
    return opener.open(url)
