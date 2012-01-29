# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        deferredurl
# Author:      jun kimura
# Created:     02/11/2011
# Copyright:   (c) jun kimura 2011
# Licence:     free
#-------------------------------------------------------------------------------
USAGE = '''
>>> from deferredurl import DeferredUrl
>>> deferred = DeferredUrl()
>>> deferred.set("http://www.google.co.jp")
>>> # Any Process...
>>> content = deferred.get('http://www.google.co.jp')
/* OR */ content = deferred['http://www.google.co.jp']
'''

from threading import Thread, Event
import urllib2

class DeferredUrl(list):
    
    def __init__(self, max_thread=2, timeout=20):
        # event for thread max
        #self.ev_thread = Event()
        self.max_thread = max_thread
        self.pool = []
        self.timeout = timeout
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
        self.pool.append(th)
        th.daemon = True
        th.start()
        
    def get(self, url):
        self.urllist[url]['event'].wait()
        return self.urllist[url]['content']()
        
    def _worker(self, url, ev):
        try:
            content = urllib2.urlopen(url, timeout=self.timeout)
        except Exception, err:
            self.urllist[url]['content'] = lambda:err_handler(err)
        else:
            self.urllist[url]['content'] = lambda:content.read()
        finally:
            ev.set()
        
    __getitem__ = get
            
def err_handler(err):
    raise Exception(err)
            
