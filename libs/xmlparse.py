# -*- coding: utf-8 -*-
import re

class xmlparse:
    
    def __init__(self, xmlstr):
        self.xmlstr = xmlstr
        self.xmldom = self.__convet2utf8()
    
    def __convet2utf8(self):
        headstr = self.__get_head()
        xmldomstr = self.xmlstr.replace(headstr, '')
        if 'gbk' in headstr:
            xmldomstr = xmldomstr.decode('gbk').encode('utf-8')
        elif 'gb2312' in headstr:
            xmldomstr = self.xmlstr.decode('gb2312').encode('utf-8')
        return xmldomstr
    
    def __get_head(self):
        headpat = r'<\?xml.*\?>'
        headpatobj = re.compile(headpat)
        headregobj = headpatobj.match(self.xmlstr)  
        if headregobj:
            headstr = headregobj.group()
            return headstr
        else:
            return ''
    
    def parse(self, key):
        temppat = '<%s>(.*?)</%s>' % (key, key)
        xmlnode = re.findall(temppat, self.xmldom)
        if xmlnode:
            return xmlnode[0]
        return None

    def __getattr__(self, key):
        return self.parse(key)


if __name__ == "__main__":
    print ''
