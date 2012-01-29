# -*- coding: utf-8 -*-

import sys

class OuterClass(object):

    def __init__(self, x):
        self.x = x

    def call_inner(self):
        self.InnerClass().access_by_outer()

    def access_by_inner(self):
        return self.x

    class InnerClass(object):

        def __init__(self):
            print sys._getframe(1).f_locals
            self.outer = sys._getframe(1).f_locals["self"]

        def access_by_outer(self):
            print dir(self.outer)
            print self.outer.access_by_inner()


def main():
    outer = OuterClass("test")
    outer.call_inner()

if __name__ == '__main__':
    main()

        

