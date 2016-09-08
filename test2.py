#coding:utf-8
"""
浏览器渲染页面后,集中下载页面到本地;
从本地文件中解析图片,然后下载
"""
from selenium import webdriver
import re,os
import sys
from lxml import etree
from time import sleep
reload(sys)
sys.setdefaultencoding('utf-8')
class downloadHTML():
    def __init__(self):
        #这里需要配置路径
        """
        self.driver = webdriver.Chrome()
        self.htmldir = os.path.join(os.path.dirname(__file__),'html')
          """
        self.chromeOptions = webdriver.ChromeOptions()
        prefs = {"profile.managed_default_content_settings.images": 2}
        self.chromeOptions.add_experimental_option("prefs", prefs)
        self.driver = webdriver.Chrome(chrome_options=self.chromeOptions)
        self.htmldir = os.path.join(os.path.dirname(__file__), 'html')

    #创建文件夹
    def makeDIR(self):
        if os.path.exists(self.htmldir):
            print '文件夹%s已存在'%self.htmldir
        else:
            os.makedirs(self.htmldir)
            print '文件夹%s创建完毕'%self.htmldir

    #渲染页面
    def get_page(self,url):
        try:
            self.driver.get(url)
            return self.driver.page_source
        except Exception as e:
            print e
            print '当前网页出错!休息10秒'
            sleep(10)
            self.driver = webdriver.Chrome(chrome_options=self.chromeOptions)
            #调用自身
            self.get_page(url)

    #获取列表页
    def parse_listpage(self,content):
        pattern = re.compile('htm_data/\d{1,}/\d{1,}/\d{1,}\.html')
        # 设置集合,过滤重复链接
        links = set()
        result = pattern.findall(content)
        for i in result:
            if i not in links:
                i = 'http://r3.gcsitl.live/pw/' + i
                links.add(i)
        return links
    #获取列表页2
    def parse_listpage2(self,content):
        html = etree.HTML(content,parser=etree.HTMLParser(encoding='utf-8'))
        links = html.xpath('//h3/a/@href')
        return ['http://r3.gcsitl.live/pw/'+link for link in links if links is not None]


    #下载详情页面
    def download(self,url,content):
        filename = url.split('/')[-1]
        #临时情况,重命名
        if 'tid' in filename:
            pass
            pattern = re.compile('\d{5,}')
            tid = pattern.findall(filename)[0]
            filename = tid + '.html'
        filepath = os.path.join(self.htmldir,filename)
        with open(filepath,'w') as f:
            f.write(content)
        print '页面%s保存到文件%s完毕'%(url,filepath)

    def run(self):
        #创建文件夹
        self.makeDIR()
        url = 'http://r3.gcsitl.live/pw/thread.php?fid=15'
        total = 0
        count = 0
        for i in range(325,564):
            if i > 1:
                url = 'http://r3.gcsitl.live/pw/thread.php?fid=15&page=%s'%i
            content = self.get_page(url)
            links = self.parse_listpage2(content)
            total += len(links)
            for link in links:
                content_detail = self.get_page(link)
                self.download(link,content_detail)
                count += 1
                print '当前总链接数%s,已下载链接数%s'%(total,count)
                #链接达到3000倍数时,重启服务
                if count % 2000 == 0:
                    self.driver.quit()
                    print '链接数达到2000倍数,浏览器10秒后重启'
                    sleep(10)
                    self.driver = webdriver.Chrome(chrome_options=self.chromeOptions)


if __name__ == '__main__':
    test = downloadHTML()
    test.run()





