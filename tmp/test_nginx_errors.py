#! coding: utf-8
import urllib

uri = 'http://localhost/test space'
print urllib.urlopen(uri).read()