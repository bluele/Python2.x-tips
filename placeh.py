# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        Pyplaceholder
# Purpose:
#
# Author:      jun kimura
#
# Created:     02/11/2011
# Copyright:   (c) jun kimura 2011
# Licence:     free
#-------------------------------------------------------------------------------

def place_holder(query, key, escape, *args):
    if len(key) > 1:
        raise Exception("You should specify 'key' not unicode or char.")

    if isinstance(args[0], tuple) or isinstance(args[0], list):
        words = args[0]
    else:
        words = args
    import re
    # pattern for placeholder's key
    pattern = re.compile(r'(^|[^\\])\%s' % key)

    for word in words:
        query = pattern.sub(r'\1' + escape(word), query, 1)

    if pattern.search(query):
        raise Exception("The number of Argument is not worth.")

    # delete escape charcter
    return re.sub(r'\\\%s' % key, key, query)

if __name__ == '__main__':
    def escape(query):
        return query.upper()
    print place_holder(u"??insert into table 日本語?iwen values(?)", u'?', escape, ("first", 'second', 'third', 'forth'))
    