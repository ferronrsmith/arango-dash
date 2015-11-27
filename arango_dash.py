#!/usr/local/bin/python

import os
import re
import sqlite3

from bs4 import BeautifulSoup

db = sqlite3.connect('arangodb.docset/Contents/Resources/docSet.dsidx')
cur = db.cursor()

try: cur.execute('DROP TABLE searchIndex;')
except: pass
cur.execute('CREATE TABLE searchIndex(id INTEGER PRIMARY KEY, name TEXT, type TEXT, path TEXT);')
cur.execute('CREATE UNIQUE INDEX anchor ON searchIndex (name, type, path);')

docpath = 'arangodb.docset/Contents/Resources/Documents/docs.arangodb.com'

page = open(os.path.join(docpath,'index.html')).read()
soup = BeautifulSoup(page)

any = re.compile('.*')
for tag in soup.find_all('a', {'href':any}):
    name = tag.text.strip()
    if len(name) > 0:
        path = tag.attrs['href'].strip()
        if path.split('#')[0] not in ('index.html', 'biblio.html', 'bookindex.html'):
            cur.execute('INSERT OR IGNORE INTO searchIndex(name, type, path) VALUES (?,?,?)', (name, 'func', path))
            print 'name: %s, path: %s' % (name, path)

db.commit()
db.close()