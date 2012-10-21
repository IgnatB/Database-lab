import urllib.request
import re
import codecs as c
from PIL import Image, ImageTk
import webbrowser

def load_content_imdb (moviesName, moviesYear): 
    url_imdb_search = r'http://www.imdb.com/find?q=' + moviesName + '&s=all'
    #print(url_imdb_search)
    try:
        resp = urllib.request.urlopen(url_imdb_search)
    except:
        return (-1,0,0)
    #print(resp.geturl())
    page=resp.read()
    resp.close()
    try:
        utfpage = c.decode(page)
    except:
        return (0,0,0)
    mYear = str(moviesYear)
    parselist = ['<table>.*?<tr>.*?<a.*?href="(/title/[^"]*?)".*?' + moviesName + '.*?' + mYear + '.*?</tr>.*?</table>',
                 '<a[^>]*?href="(/title/[^"]*?)".*?' + moviesName + '.*?' + mYear,
                 '<a[^>]*?href="(/title/[^"]*?)".*?' + mYear + '.*?' + moviesName,
                 'Media from.*?<a[^>]*?href="(/title/[^"]*?)".*?' + mYear]
    movie_url = 0            
    for parse in parselist:
        #print(parse)
        p = re.compile(parse, re.MULTILINE | re.DOTALL)
        m = p.search(utfpage)
        if m:
            movie_url = m.group(1)
            break
    if movie_url == 0:
        return (0,0,0)
    url_imdb_find = r'http://www.imdb.com' + movie_url
    #print(url_imdb_find)
    try:
        resp = urllib.request.urlopen(url_imdb_find)
    except:
        return (0,0,0)
    page=resp.read()
    resp.close()
    try:
        utfpage = c.decode(page)
    except:
        return (0,0,0)
    p = re.compile('id="img_primary".*?<img[^>]*?src="(.*?)"',re.MULTILINE | re.DOTALL)
    m = p.search(utfpage)
    if m:
        img_url = m.group(1)
    else:
        img_url = 1
    p = re.compile('<p itemprop="description">\t*?(.*?)\t*?</p>',re.MULTILINE | re.DOTALL)
    m = p.search(utfpage)
    if m:
        description = m.group(1)
    else:
        description = 0
    p = re.compile('<div class="titlePageSprite star-box-giga-star">.*?([\d\.]+).*?</div>',re.MULTILINE | re.DOTALL)
    m = p.search(utfpage)
    if m:
        rating = m.group(1)
    else:
        rating = 0
    return (img_url, description, rating)



