# -*- coding: utf-8 -*-

'''
>>> from defferredurl import DefferredUrl
>>> defferred = DefferredUrl()
>>> defferred.set("http://www.google.co.jp")
>>> # Any Process...
>>> content = defferred.get('http://www.google.co.jp')
/* OR */ content = defferred['http://www.google.co.jp']
'''

from threading import Thread, Event
import urllib2

class DefferredUrl(list):
    
    def __init__(self):
        #self.pool = []
        self.ev = Event()
        self.urllist = {}
    
    def set(self, url):
        if self.urllist.has_key(url):
            return
        ev = Event()
        self.urllist[url] = {
                'event':ev,
                'content':None,
                }
        th = Thread(target=self._worker, args=(url, ev))
        #self.pool.append(th)
        th.daemon = True
        th.start()
        
    def get(self, url):
        self.urllist[url]['event'].wait()
        return self.urllist[url]['content']
        
    def _worker(self, url, ev):
        try:
            content = urllib2.urlopen(url)
        except:
            pass
        else:
            self.urllist[url]['content'] = content.read()
            ev.set()
        
    __getitem__ = get
            