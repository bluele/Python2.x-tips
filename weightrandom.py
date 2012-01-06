# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        weightrandom
# Purpose:
#
# Author:      jun kimura
#
# Created:     03/12/2011
# Copyright:   (c) jun kimura 2011
# Licence:     free
#-------------------------------------------------------------------------------
#!/usr/bin/env python

from random import uniform

def watch_line(callback, n):
    result = {"test1":0, "test2":0, "test3":0}
    for x in xrange(n):
        result[callback()] += 1
    print result


class weight_random(object):

    def __init__(self, obj=[]):
        self.obj = obj

    def add(self, item):
        self.obj.append(item)

    def choice(self, *args, **kw):
        sw = 0
        for x in self.obj: sw += x["weight"]
        val = uniform(0, sw)
        for y in self.obj:
            if val < y["weight"]:
                break
            val -= y["weight"]
        if y.has_key("args") and y:
            return y["callback"](y["args"])
        return y["callback"](*args, **kw)


def main():
    def changed1(a,b,c=12):
        return a + b + c

    def changed2(a,b,c):
        return a * b * c

    wr = weight_random(
    (
    {'weight':0.000001, 'callback':changed1},
    {'weight':0.000002, 'callback':changed2},
    {'weight':0.00003, 'callback':changed2},
    ))
    print wr.choice(100, 13, 14)
    #watch_line(lambda:wr.choice("test"), 10000)

if __name__ == '__main__':
    main()
