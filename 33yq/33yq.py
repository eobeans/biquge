# -*- coding:UTF-8 -*-
import requests,re
from bs4 import BeautifulSoup
import random

"""
类说明:下载《33言情》网小说
Parameters:
    无
Returns:
    无
Modify:
    2019-02-28
"""
class downloader(object):
    def __init__(self):
        self.server = 'https://www.33yq.org/'
        self.target = 'https://www.33yq.org/read/139668/'
        self.names = []            #存放章节名
        self.urls = []            #存放章节链接
        self.nums = 0            #章节数

    """
    函数说明:获取下载链接
    Parameters:
        无
    Returns:
        无
    Modify:
        2019-02-28
    """
    def get_download_url(self):
        my_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
        }
        req = requests.get(url=self.target, headers=my_headers)
        html = req.text
        div_bf = BeautifulSoup(html, "html5lib")
        ul = div_bf.find_all('dl')
        p_bf = BeautifulSoup(str(ul[0]), "html5lib")
        p = p_bf.find_all('p')
        self.nums = len(p[131:])
        count = 132
        for each in p[131:]:
            self.names.append(each.string)
            self.urls.append(self.server + count + '.html')
            count += 1

    """
    函数说明:获取章节内容
    Parameters:
        target - 下载连接(string)
    Returns:
        texts - 章节内容(string)
    Modify:
        2019-02-28
    """
    def get_contents(self, target):
        req = requests.get(url=target)
        req.encoding = req.apparent_encoding  # 因为网站头部没有指定编码，因此需要requests自己去判断
        html = req.text
        bf = BeautifulSoup(html, "html5lib")
        texts = bf.find_all('div', id='chaptercontent')
        texts = str(texts[0])

        pattern = re.compile('.*?<br/>')  # 选出所有以<br/>为结尾的
        conts = re.findall(pattern, texts)

        # conts[0] = conts[0].lstrip()
        # conts[0] = '　　' + conts[0]  # 第一行行首会有多余的空格

        pagePattern = re.compile('\d页]')
        pageTotal = re.findall(pagePattern, texts)
        pageTotal = int(pageTotal[0][0]) - 1
        targetP = target.split('.html')
        if pageTotal > 0:
            for ind in range(pageTotal):
                pageNum = ind + 2
                urlP = targetP[0] + '_' + str(pageNum) + '.html'
                # print(urlP)
                reqP = requests.get(url=urlP)
                reqP.encoding = reqP.apparent_encoding
                htmlP = reqP.text
                bfp = BeautifulSoup(htmlP, "html5lib")
                textP = bfp.find_all('div', id='chaptercontent')
                textP = str(textP[0])
                contP = re.findall(pattern, textP)
                conts = conts + contP

        for i in range(len(conts)):
            conts[i] = conts[i].replace('<br/>', '\n')  # 去掉<br/>

        return conts


    """
    函数说明:将爬取的文章内容写入文件
    Parameters:
        name - 章节名称(string)
        path - 当前路径下,小说保存名称(string)
        text - 章节内容(string)
    Returns:
        无
    Modify:
        2019-02-28
    """
    def writer(self, name, path, text):
        write_flag = True
        with open(path, 'a', encoding='utf-8') as f:
            f.write(name + '\n')
            f.writelines(text)
            f.write('\n\n')


def conn_contents(proxies, target):
    my_headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
    }
    proxy_num = len(proxies) - 1
    proxy_random_ind = random.randint(0, proxy_num)
    try:
        req = requests.get(url=target, timeout=5, headers=my_headers)
        req.encoding = req.apparent_encoding  # 因为网站头部没有指定编码，因此需要requests自己去判断
        if req.status_code == 200:
            html = req.text
            print('正在正常下载...')
            return html
        else:
            try:
                req = requests.get(url=target, timeout=5, proxies={'http': proxies[proxy_random_ind]}, headers=my_headers)
                req.encoding = req.apparent_encoding
                if req.status_code == 200:
                    html = req.text
                    print('正在使用代理下载...')
                    return html
                else:
                    return False
            except:
                return False
    except:
        return False

if __name__ == '__main__':

    dl = downloader()
    dl.get_download_url()
    for i in range(dl.nums):
        dl.writer(dl.names[i], '../xs/苟在仙界成大佬.txt', dl.get_contents(dl.urls[i]))
    print('下载完成!')
    print('下载失败链接')
    print(dl.fails)
