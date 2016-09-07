#coding:utf-8
"""
浏览器渲染页面后,集中下载页面到本地;
从本地文件中解析图片,然后下载
"""
from selenium import webdriver
import re,os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
class downloadHTML():
    def __init__(self):
        #这里需要配置路径
        """
        self.driver = webdriver.Chrome()
        self.htmldir = os.path.join(os.path.dirname(__file__),'html')
          """
        chromeOptions = webdriver.ChromeOptions()
        prefs = {"profile.managed_default_content_settings.images": 2}
        chromeOptions.add_experimental_option("prefs", prefs)
        self.driver = webdriver.Chrome(chrome_options=chromeOptions)
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
        self.driver.get(url)
        return self.driver.page_source

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

    #下载详情页面
    def download(self,url,content):
        filename = url.split('/')[-1]
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
        for i in range(84,564):
            if i > 1:
                url = url + '&page=%s'%i
            content = self.get_page(url)
            links = self.parse_listpage(content)
            total += len(links)
            for link in links:
                content_detail = self.get_page(link)
                self.download(link,content_detail)
                count += 1
                print '当前总链接数%s,已下载链接数%s'%(total,count)
if __name__ == '__main__':
    test = downloadHTML()
    test.run()





