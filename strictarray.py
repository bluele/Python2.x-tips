# -*- coding: utf-8 -*-

'''
@summary: 
    staticな型のList
    c/apiで実装したい　型を制限することで高速化とメモリ節減を図りたい
'''

class StrictArray(list):
    '''
    @todo: decoratorにしてもいいかも
    @param: otype: <type>
    '''
    def __init__(self, otype):
        if not isinstance(otype, type):
            otype = type(otype)
        self.otype = otype
    
    def __setitem__(self, value):
        self._is_type(value)
        list.__setitem__(self, value)
        
    def append(self, value):
        self._is_type(value)
        list.append(self, value)
    
    def _is_type(self, value):
        ''' decoratorにしてもいいかもしれない'''
        print "hook"
        if self.otype is not type(value):
            print self.otype
            print type(value)
            raise TypeError("Value '%s' is not match %s." % (str(value), self.otype))
        
def test():
    s = StrictArray(str)
    s.append("jun")
    s.append("kimura")
    s.append(u"noriko")
    
if __name__ == '__main__':
    test()
        
