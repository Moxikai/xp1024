#coding:utf-8
from requests import session,get,post
from selenium import webdriver
import re
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class zipai():
    #初始化驱动
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.page_content = ''
        self.imgdir = os.path.join(os.path.dirname(__file__),'IMG')
        self.htmldir = os.path.join(os.path.dirname(__file__),'HTML')

    #渲染网页
    def get_page(self,url):
        self.driver.get(url)
        return self.driver.page_source


    #获取列表页链接
    def parse_topics(self,content):
        pattern = re.compile('htm_data/\d{1,}/\d{1,}/\d{1,}\.html')
        # 设置集合,过滤重复链接
        links = set()
        result = pattern.findall(content)
        for i in result:
            if i not in links:
                i = 'http://r3.gcsitl.live/pw/' + i
                links.add(i)
        return links


    #获取详情页图片链接
    def parse_detail_imgs(self,content):
        pattern = re.compile('<img src="(http://\S+)"')
        result = pattern.findall(content)
        if result:
            print '页面发现图片%s张' % len(result)
            return result


    #获取详情页标题
    def parse_detail_title(self,content):
        pass
        pattern = re.compile('class="fl">(.*)</h1>')
        result = pattern.findall(content)
        if result:
            return result[0]


    #获取详情页面信息
    def parse_detail(self,content):
        title = self.parse_detail_title(content)
        imgs = self.parse_detail_imgs(content)
        return {'title':title,
                'imgs':imgs}

    #保存详情页面文件到本地
    def save_html(self,url,content):
        pass

    #下载图片
    def download_img(self,folder,img):
        #获取原文件名称
        filename = img.split('/')[-1]
        filepath = os.path.join(folder,filename)
        #判断文件是否已下载
        if not os.path.exists(filepath):
            #通过requests模块下载
            r = get(img)
            with open(filepath,'wb') as code:
                code.write(r.content)
        else:
            print '文件已下载'


    #批量下载
    def save_info(self,imgs):
        #按照名称创建文件夹
        folder = os.path.join(self.imgdir,imgs['title'])
        if not os.path.exists(folder):
            #创建多层文件夹
            os.makedirs(folder)
            print '文件夹%s已创建'%(folder)
        #下载文件
        urls = imgs['imgs']
        total = len(urls)
        count = 0
        for img in urls:
            self.download_img(folder,img)
            count += 1
            print '本页图片%s张,已下载%s张'%(total,count)


    def run(self):
        #图片首页
        url = 'http://r3.gcsitl.live/pw/thread.php?fid=15'
        for page in xrange(1,563):
            if page > 1:
                url = url +'page=%s'%page
            #获取列表内容
            content = self.get_page(url)
            #获取列表页内容
            links = self.parse_topics(content)
            #获取详情页面
            for link in links:
                print link
                #检测是否存在本地版本
                filename = link.split('/')[-1]
                filepath = os.path.join(self.htmldir,filename)
                if not os.path.exists(filepath):
                    content_detail = self.get_page(link)
                    with open(filepath,'w') as f:
                        f.write(content_detail)
                else:
                    with open(filepath,'r') as f:
                        content_detail = f.read()
                imgs = self.parse_detail(content_detail)
                # 下载图片
                self.save_info(imgs)
if __name__ == '__main__':
    test = zipai()
    test.run()



