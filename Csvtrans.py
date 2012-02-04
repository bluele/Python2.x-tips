# -*- coding: utf-8 -*-
import os
import sys
import re
import csv
import shutil

# for py2exe
reload(sys)
sys.setdefaultencoding('UTF-8')

__usage__ = '''
第一引数に変換対象のファイル、第二引数に変換テーブルを記述したCSVファイルのパスを指定します
$ python Csvtrans.py "<table>" "<target-directory>" "<extension>"
$ python setup.py py2exe -packages encodings
'''

class Csvtrans(object):
    
    def __init__(self):
        pass
    
    def create(self, table):
        '''
        @summary: 
            変換テーブル作成メソッド            
        '''
        #csv_dialectを作成
        csv.register_dialect('escaped', escapechar='\\', doublequote=True, quoting=csv.QUOTE_MINIMAL)
        try:
            self.table_enc = guessEncoding(file(table,'r').read())
            self.table = [(x,y) for x,y in csv.reader(file(table,'r'),dialect='escaped')]
        except IOError:
            print 'except: Cannot open "%s"' % table
            raise
        except ValueError:
            print u"変換テーブルの形式が不正です。"
            raise
        
    def flush(self):
        for row in self.table:
            print row
# 対象のファイルを変換テーブルで変換する targetには対象のファイルパス
    def convert(self, target):
        '''
        @summary: 
            元データの読み込みを行います
        '''
        try:
            f = file(target, 'r')
            data = f.read()
        except IOError:
            print 'except: Cannot open "%s"' % target
            return False
        finally:
            f.close()
        
        data_enc = guessEncoding(data)
        data = data.decode(data_enc, 'strict')
   
        #バックアップファイルの作成
        try:
            shutil.copyfile(target,target + '~')
        except:
            print u"ディレクトリにバックアップを作成できません。"
            return False

        #変換後のファイルを新規作成        
        try:
            f = file(target, 'w')
        except :
            print "%sを編集できません。" % target
            print 'except: Cannot open "%s"' % target
            return False

        #変換処理
        try:        
            for x,y in self.table:
                data = data.replace(x.decode(self.table_enc, 'strict'), y.decode(self.table_enc, 'strict'))
            f.write(data.encode(data_enc))
        except:
            #変換中の例外はrollbackする
            try:
                shutil.rename(target + '~', target)
            except:
                print "%sが破損しました。バックアップファイルを参照してください。" % target
                raise
        finally:
            f.close()
        

# 引数に指定したテキストの文字コードを推測する        
def guessEncoding(text):
    enclist = ['utf-8','shift-jis','euc-jp']
    for enc in enclist:
        try:
            text.decode(enc)
            return enc
        except:
            pass
    return None
    
def getFiles(path,ext):
    pats = []
    for x in ext.split(' '):
        pats.append('(\.' + x.lstrip('.') + ')$')
    repat = re.compile( ('|').join(pats) )
    for file in os.walk(path).next()[2]:#ファイルのみ抽出
        if(repat.search(file) is None):
            pass
        else:
            yield os.path.join(path, file)

if __name__ == '__main__':
    argv = sys.argv[1:]
    if len(argv) < 3:
        USAGE = 'USAGE:\n    $ python Csvtrans.py "<table>" "<target-directory>" "<extension>"'
        raise Exception(USAGE)
    else:
        table = os.path.join(os.getcwd(), argv[0])
        if(os.path.exists(table) == False):
            raise Exception("ERROR: directory '%s' is not existed.") % table
        # print u"[table]\n" + table.decode('cp932')
        target = os.path.join(os.getcwd(), argv[1])
        if(os.path.exists(target) == False):
            raise Exception("ERROR: directory '%s' is not existed.") % target
        # print u"\n[target-directory]\n" + target.decode('cp932')
        e = argv[2]
        if(e == ""):
            raise ("ERROR: You must specify the extension list.")
    
    obj = Csvtrans()
    obj.create(table)
    
    #条件に一致したファイルのパスを順に取り出す
    for x in getFiles(target, e):
        print "\n\n[start]\n%s\n" % x
        obj.convert(x)
        print "[end]\n"

    # obj.flush()




    
