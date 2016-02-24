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

        for html in page_group:
            page_sources  = requests.get(html)
            pagesource.append(page_sources.text)

        return pagesource

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
        print u'正在处理页面源代码………'
        kidsource = []
        for html in kidlink:
            kidsourcess = requests.get(html).text
            kidsources = kidsourcess
            kidsource.append(kidsources)
        return kidsource
#source用来生产具体资源
    def finallsource(self,kidsource):


        pic = []
        works = []
        times = []
        for html in kidsource:
            re_catworks = re.findall(r'</h3>\s*<h2\s*class=.*>\s*(.*)\s*', html)
            for i in re_catworks:
                work = i.replace('/', '')
                works.append(work)
        for html in kidsource:
            re_times = re.findall(r'</h3>\s*<h2\s*class=.*>\s*.*\s*</h2>\s*<p>\s*(.*)\s*', html)
            for i in re_times:
                time = i.replace('/', '')
                times.append(time)
        for html in kidsource:
            re_catpicture = re.findall(r'1440w, (/media/.*) 2000w', html)
            if re_catpicture == []:
                pic.append(' ')
            else:
                for i in re_catpicture:
                    links = 'http://www.moma.org' + str(i)
                    pic.append(links)
        source = []

        for workv in works:
            for picv in pic:
                for timev in times:
                    source.append([workv,picv,timev])
        n = 0

        while n <= 82:
            n = 0
            source.append([works[n],times[n],pic[n]])
            n = n + 1


        n = 0
        n <= len(times)
        for each in pic:
            if each == ' ':
                print u'无图像文件'
            else:
                print u'正在下载:' + each + '------>' + str(n)
                pic = requests.get(each)
                fp = open('/Users/messi/Pictures/moma/' +  str(n)  + u'--'  + times[n] + ' ' + u'[' + works[n] + u']' + '.jpg','wb')
                fp.write(pic.content)
                fp.close()
                n += 1

        

if __name__ == '__main__':

    url = 'http://www.moma.org/collection/artists/4243?locale=zh&page=1'
    moma = spider()
    index_links = moma.changepage(url,1)
    index_html = moma.pagesources(index_links)
    kid_html = moma.kidhtml(index_html)
    kid_link = moma.kidlink(kid_html)
    kid_code = moma.kidsource(kid_link)
    fin_src = moma.finallsource(kid_code)





