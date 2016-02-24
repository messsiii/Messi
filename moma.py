#!/usr/bin/python
#-*_coding:utf8-*-
import re
import requests
#import sys
#import xlsxwriter
#reload(sys)
#sys.setdefaultencoding("utf-8")

class spider(object):
    def __init__(self):
        print u'开始爬取内容。。。'

#getsource用来获取首页源代码
    def getsource(self,url):
        html = requests.get(url)
        return html.text

#changepage用来生产首页不同页数的链接
    def changepage(self,url,total_page):
        now_page = int(re.search('page=(\d+)',url,re.S).group(1))
        page_group = []
        n = 1
        for i in range(now_page,total_page+1):
            link = re.sub('page=\d+','page=%s'%i,url,re.S)
            page_group.append(link)
        for s in page_group:
            print u'正在处理首页链接:  ' + str(s) + u'  ---->' + str(n)
            n += 1
        return page_group
#pagesource用来生产首页不同页面的源代码
    def pagesources(self,page_group):
        pagesource = []
#        n = 1
        for html in page_group:
            page_sources  = requests.get(html)
            pagesource.append(page_sources.text)
#        for i in pagesource:
#            print u'正在处理不同页面源代码:    ------>' + str(n) + i
#            n += 1
        return pagesource
#indexhtml用来保存首页源代码
#    def saveindex(self,momaindex):
#        f = open('momaindex.txt','a')
#        for input in momaindex:
#            f.write(input.encode('utf8'))
#        f.close()
#kidhtml用来生产首页不同页链接地址
    def kidhtml(self,indexhtml):
        kidhtml = []
        for inhtml in indexhtml:
            kid_html = re.findall('<a class="link--tile" href="(.*zh)">', inhtml)
            for i in kid_html:
                kidhtml.append(i)
        return kidhtml
#kidlink用来合成可访问子集链接地址
    def kidlink(self,kidhtml):
        kid_link = []
        n = 1
        for i in kidhtml:
            kidlink = 'http://www.moma.org' + i
            print u'正在合成链接:  '+ kidlink + u'  ---->' + str(n)
            n += 1
            kid_link.append(kidlink)
        return kid_link
#kidsource用来生产子级链接源代码
    def kidsource(self,kidlink):
        kidsource = []
        for html in kidlink:
            kidsourcess = requests.get(html).text
            kidsources = kidsourcess
            kidsource.append(kidsources)
        return kidsource
#source用来生产具体资源
    def finallsource(self,kidsource):

        pic = []
#        aut = []
#        works = []
#        times = []
        for html in kidsource:
            re_catpicture = re.findall(r'1440w, (/media/.*) 2000w', html)
            for i in re_catpicture:
                links = 'http://www.moma.org' + str(i)
                pic.append(links)
        n = 1
        for each in pic:
            print 'now downloading:' + each
            pic = requests.get(each)
            fp = open('/Users/messi/Pictures/moma/moma' + str(n) + '.jpg','wb')
            fp.write(pic.content)
            fp.close()
            n +=1
#        for html in kidsource:
#            re_catauthor = re.findall(r'<h3>(\s*<a\s*.*\s*.*\s*.*\s*.*\s*.*\s*.*\s*.*\s*.*\s*.*\s*.*\s*.*\s*.*\s*.*\s*.*\s*)</h2>',html)
#            aut.append(re_catauthor)
#        for html in kidsource:
#            re_catworks = re.findall(r'<h2 class=.*\s*(.*)\s*</h2>', html)
#            works.append(re_catworks)
#        for html in kidsource:
#            re_cattimes = re.findall(r'</h2>\s*<p>\s*(.*)\s*</p>', html)
#            times.append(re_cattimes)
        

if __name__ == '__main__':

    url = 'http://www.moma.org/collection?direction=fwd&locale=zh&page=1&with_images=true'
    moma = spider()
    index_links = moma.changepage(url,1121)
    index_html = moma.pagesources(index_links)
#    momaindexhtml = moma.saveindex(kid_html)
    kid_html = moma.kidhtml(index_html)
    kid_link = moma.kidlink(kid_html)
    kid_code = moma.kidsource(kid_link)
#    kid_source = moma.kidsource(kid_code)
#    print kid_source
#    print kid_link
    fin_src = moma.finallsource(kid_code)




