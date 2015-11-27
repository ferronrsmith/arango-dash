#!/usr/local/bin/python
import getopt
import os
import re
import sqlite3
from sys import argv
import sys
from bs4 import BeautifulSoup


def main(argv):
    try:
        opts, args = getopt.getopt(argv, "ht:", ["docType="])
    except getopt.GetoptError:
        print "arango_dash.py -t <docType>"
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print "arango_dash.py -t <docType>"
            sys.exit()
        elif opt in ("-t", "-docType"):

            db = sqlite3.connect(arg + '.docset/Contents/Resources/docSet.dsidx')
            cur = db.cursor()

            folder = 'docs.arangodb.com'

            try:
                cur.execute('DROP TABLE searchIndex;')
            except:
                pass
            cur.execute('CREATE TABLE searchIndex(id INTEGER PRIMARY KEY, name TEXT, type TEXT, path TEXT);')
            cur.execute('CREATE UNIQUE INDEX anchor ON searchIndex (name, type, path);')

            docpath = arg + '.docset/Contents/Resources/Documents/' + folder

            page = open(os.path.join(docpath, 'index.html')).read()
            soup = BeautifulSoup(page)

            any = re.compile('.*')
            for tag in soup.find_all('a', {'href': any}):
                name = re.sub("\n\s+", " ", tag.text.strip())
                if len(name) > 0:
                    path = re.sub("(\./)", "", tag.attrs['href'])
                    path = folder + "/" + path
                    if path.split('#')[0] not in ('index.html', 'biblio.html', 'bookindex.html'):
                        cur.execute('INSERT OR IGNORE INTO searchIndex(name, type, path) VALUES (?,?,?)',
                                    (name, 'Guide', path))
                        print 'name: %s, path: %s' % (name, path)

            db.commit()
            db.close()


if __name__ == "__main__":
    main(argv[1:])
