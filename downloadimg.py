#coding:utf-8
"""
获取本地文件列表;
从本地缓存中解析图片地址;
requests模块下载图片;
"""
import lxml,re,os
from requests import get
from lxml import etree
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
class DownloadImage():
    #初始化
    def __init__(self):
        pass
        self.imgdir = os.path.join(os.path.dirname(__file__),'img')
        self.htmldir = os.path.join(os.path.dirname(__file__),'html')
        #保存任务进度信息
        self.infoPath = os.path.join(self.htmldir,'info.txt')
    #创建文件夹
    def makeDIR(self):
        if not os.path.exists(self.imgdir):
            os.makedirs(self.imgdir)
            print '文件夹%s创建完毕!'%(self.imgdir)
        else:
            print '文件夹%s已存在'%self.imgdir

    #更新方法
    def parse_detail(self,content):
        html = etree.HTML(content,parser=etree.HTMLParser(encoding='utf-8'))
        titles = html.xpath('//h1[@id="subject_tpc"]/text()')
        imgs = html.xpath('//div[@id="read_tpc"]/img/@src')
        if titles and imgs:
            return {'title':titles[0],'imgs':imgs}
        else:
            return False

    #下载单张图片
    def download_img(self, folder, img):
        # 获取原文件名称
        filename = img.split('/')[-1]
        filepath = os.path.join(folder, filename)
        # 判断文件是否已下载
        if not os.path.exists(filepath):
            # 通过requests模块下载
            r = get(img)
            with open(filepath, 'wb') as code:
                code.write(r.content)
        else:
            print '文件已下载'


    def download_imgs(self, imgs):
        # 按照名称创建文件夹
        folder = os.path.join(self.imgdir, imgs['title'])
        if not os.path.exists(folder):
            # 创建多层文件夹
            os.makedirs(folder)
            print '文件夹%s已创建' % (folder)
        else:
            return True
        # 下载文件
        urls = imgs['imgs']
        if urls:
            total = len(urls)
            count = 0
            for img in urls:
                self.download_img(folder, img)
                count += 1
                print '本页图片%s张,已下载%s张' % (total, count)
            return True

    #保存任务进度
    def save_info(self,html):
        with open(self.infoPath,'a') as f:
            html = [i + '\n' for i in html]
            f.writelines(html)


    #载入进度
    def load_info(self):
        with open(self.infoPath,'r') as f:
            return [item.strip() for item in f.readlines()]

    #统一文件命名
    def rename_(self):
        files = os.listdir(self.htmldir)
        count = 0
        for file in files:
            if 'tid' in file:
                pattern = re.compile('\d{5,}')
                filename = pattern.findall(file)[0] +'.html'
                oldname = os.path.join(self.htmldir,file)
                newname = os.path.join(self.htmldir,filename)
                #重命名
                os.renames(oldname,newname)
                count += 1
                print '已经重命名文件%s个'%count

    def run(self):
        #提取文件列表
        files = os.listdir(self.htmldir)
        #载入上次进度
        if os.path.exists(self.infoPath):
            lists = self.load_info()
        else:
            lists =[]
        for file in files:
            #排除已完成文件及无关文件
            if 'html' in file and file not in lists:
                #获取完整路径
                filepath = os.path.join(self.htmldir,file)
                #打开文件
                print '当前文件名:%s'%filepath
                with open(filepath,'r') as f:
                    content = f.read()
                #获取
                imgs = self.parse_detail(content)
                #下载图片
                if imgs:
                    if self.download_imgs(imgs):
                        self.save_info([file])


if __name__ == '__main__':
    test = DownloadImage()
    test.run()


