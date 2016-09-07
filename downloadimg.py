#coding:utf-8
"""
获取本地文件列表;
从本地缓存中解析图片地址;
requests模块下载图片;
"""
import lxml,re,os
from requests import get

class DownloadImage():
    #初始化
    def __init__(self):
        pass
        self.imgdir = os.path.join(os.path.dirname(__file__),'img')
        self.htmldir = os.path.join(os.path.dirname(__file__),'html')

    #创建文件夹
    def makeDIR(self):
        if not os.path.exists(self.imgdir):
            os.makedirs(self.imgdir)
            print '文件夹%s创建完毕!'%(self.imgdir)
        else:
            print '文件夹%s已存在'%self.imgdir

    def parse_detail(self,content):
        title = self.parse_detail_title(content)
        imgs = self.parse_detail_imgs(content)
        return {'title': title,
                'imgs': imgs}

    # 获取详情页图片链接
    def parse_detail_imgs(self, content):
        pattern = re.compile('<img src="(http://\S+)"')
        result = pattern.findall(content)
        if result:
            print '页面发现图片%s张' % len(result)
            return result

    # 获取详情页标题
    def parse_detail_title(self, content):
        pass
        pattern = re.compile('class="fl">(.*)</h1>')
        result = pattern.findall(content)
        if result:
            return result[0]

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

    # 批量下载
    def save_info(self, imgs):
        # 按照名称创建文件夹
        folder = os.path.join(self.imgdir, imgs['title'])
        if not os.path.exists(folder):
            # 创建多层文件夹
            os.makedirs(folder)
            print '文件夹%s已创建' % (folder)
        # 下载文件
        urls = imgs['imgs']
        total = len(urls)
        count = 0
        for img in urls:
            self.download_img(folder, img)
            count += 1
            print '本页图片%s张,已下载%s张' % (total, count)

    def run(self):
        pass
        #获取文件列表
        files = os.listdir(self.htmldir)
        for file in files:
            #print file
            if 'html' in file:
                #获取完整路径
                filepath = os.path.join(self.htmldir,file)
                #打开文件
                with open(filepath,'r') as f:
                    content = f.read()
                #获取
                imgs = self.parse_detail(content)
                #下载图片
                self.save_info(imgs)

if __name__ == '__main__':
    test = DownloadImage()
    test.run()
