import os
import sys
import urllib
import requests
import re
from lxml import etree
reload(sys)
sys.setdefaultencoding('utf-8')


def StringListSave(save_path, filename, slist):
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    path = save_path+"/"+filename+".txt"
    with open(path, "w+") as fp:
        for s in slist:
            fp.write("%s\t\t%s\n" % (s[0].encode("utf8").decode('utf-8'), s[1].encode("utf8").decode('utf-8')))

def LeftList(save_path, filename, list):
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    path = save_path+"/"+filename+".txt"
    with open(path, "w+") as fp:
        for s in list:
            fp.write("%s\t\t%s\t\t%s\t\t%s\n" % (s[0].encode("utf8").decode('utf-8'), 
                  s[1].encode("utf8").decode('utf-8'), s[2].encode("utf8").decode('utf-8'),
                  s[3].encode("utf8").decode('utf-8')))

def RightList(save_path, filename, list2):
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    path = save_path+"/"+filename+".txt"
    with open(path, "w+") as fp:
        for s in list2:
            fp.write("%s\t\t%s\t\t%s\n" % (s[0].encode("utf8").decode('utf-8'), 
                  s[1].encode("utf8").decode('utf-8'), s[2].encode("utf8").decode('utf-8')))
              

def Page_Info(myPage):
    '''Regex'''
    # get list subtitles
    mypage_Info = re.findall(r'<div class="titleBar" id=".*?"><h2>(.*?)</h2><div class="more"><a href="(.*?)">.*?</a></div></div>', myPage, re.S)
    return mypage_Info


def Left_Page_Info(left):
    '''Regex(slowly) or Xpath(fast)'''
    # 1 hour: div[2] | 24 hours: div[3] | one week: div[4]
    dom = etree.HTML(left)
    content_field = dom.xpath('//div[@class="area-half left"]/div/div[2]')[0]
    new_titles = content_field.xpath('//tr/td/a/text()')
    new_hits = content_field.xpath('//tr/td[2]/text()')
    new_ranks = content_field.xpath('//tr/td[3]/img/@src')
    new_urls = content_field.xpath('//tr/td/a/@href')
    # print(new_ranks)
    if  len(new_ranks) == 0: 
        # print("left null")
         return zip(new_titles, new_hits, new_urls)
    else:
        # print("left")
         return zip(new_titles, new_hits, new_ranks, new_urls)

def Right_Page_Info(right):
    '''Regex(slowly) or Xpath(fast)'''
    # 1 hour: div[2] | 24 hours: div[3] | one week: div[4]
    content_field2 = etree.HTML(right)
    new_titles2 = content_field2.xpath('//body/div[4]/div[3]/div/div[2]/table/tr/td/a/text()')
    new_hits2 = content_field2.xpath('//body/div[4]/div[3]/div/div[2]/table/tr/td[2]/text()')
    new_urls2 = content_field2.xpath('//body/div[4]/div[3]/div/div[2]/table/tr/td/a/@href')
    # print("right")
    return zip(new_titles2, new_hits2, new_urls2)

def Spider(url):
    print("loading ", url)
    myPage = requests.get(url).content.decode("gbk")
    myPageResults = Page_Info(myPage)
    save_path = u"data"
    filename = u"0_rank"
    StringListSave(save_path, filename, myPageResults)
     
    i = 1
    j = 1
    for item, url in myPageResults:
        print("loading ", url)
        left= requests.get(url).content.decode("gbk")
        right= requests.get(url).content.decode("gbk")
        leftPageResults = Left_Page_Info(left)
        rightPageResults = Right_Page_Info(right)
        filename1 = str(i)+"_"+item + "_hits"
        if len(leftPageResults[0]) < 4:
           RightList(save_path, filename1, leftPageResults[0:10])
        else:
           LeftList(save_path, filename1, leftPageResults[0:10])
            # leftPageResults = Right_Page_Info(left)
            # RightList(save_path, filename1, leftPageResults)
        filename2 = str(j)+"_"+item + "_BBS"
        RightList(save_path, filename2, rightPageResults[0:10])
        i += 1
        j += 1

if __name__ == '__main__':
    print("start")
    start_url = "http://news.163.com/rank/"
    Spider(start_url)
    print("end")