# -*- coding:UTF-8 -*-
import random

import requests, re, time
from bs4 import BeautifulSoup

"""
类说明:下载《一七小说》网小说
Parameters:
    无
Returns:
    无
Modify:
    2019-02-28
"""


class downloader(object):
    def __init__(self):
        # https://wap.33yqxs.com/
        # https://www.1qxs.com/list/64130.html
        self.server = 'https://www.1qxs.com/xs/64130/'
        self.target = 'https://www.1qxs.com/list/64130.html'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
        }
        self.names = []  # 存放章节名
        self.urls = []  # 存放章节链接
        self.nums = 0  # 章节数
        self.fails = []
        self.proxies = ['http://121.13.252.60:41564', 'http://210.5.10.87:53281', 'http://117.94.120.236:9000', 'http://183.236.232.160:8080', 'http://112.14.47.6:52024', 'http://117.114.149.66:55443', 'http://222.74.73.202:42055', 'http://116.9.163.205:58080', 'http://117.41.38.18:9000', 'http://61.216.185.88:60808', 'http://210.5.10.87:53281', 'http://121.13.252.62:41564', 'http://112.14.47.6:52024', 'http://117.114.149.66:55443', 'http://116.9.163.205:58080', 'http://117.41.38.19:9000', 'http://27.42.168.46:55481', 'http://61.216.156.222:60808', 'http://61.216.185.88:60808', 'http://121.13.252.58:41564', 'http://121.13.252.60:41564', 'http://210.5.10.87:53281', 'http://117.41.38.18:9000', 'http://183.236.232.160:8080', 'http://112.14.47.6:52024', 'http://222.74.73.202:42055', 'http://202.109.157.66:9000', 'http://27.42.168.46:55481', 'http://121.13.252.61:41564']

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
        req = requests.get(url=self.target, headers=self.headers)
        html = req.text
        div_bf = BeautifulSoup(html, "html5lib")
        ul = div_bf.find_all('ul')
        p_bf = BeautifulSoup(str(ul[0]), "html5lib")
        p = p_bf.find_all('p')
        self.nums = len(p[131:318])
        count = 132
        for each in p[131:318]:
            self.names.append(each.string)
            str_count = str(count)
            self.urls.append(self.server + str_count + '.html')
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
        html = conn_contents(self.proxies, target)
        if html:
            bf = BeautifulSoup(html, "html5lib")
            texts = bf.find_all('div', class_='content')
            texts = str(texts[0])

            pattern = re.compile('.*?</p>')
            conts = re.findall(pattern, texts)

            title = bf.find('h1')
            title = str(title)
            pagePattern = re.compile('\/\d\)')
            numPattern = re.compile('\d')
            pageTotal = re.findall(pagePattern, title)
            pageTotal = re.findall(numPattern, pageTotal[0])
            pageTotal = int(pageTotal[0]) - 1
            print('已下载： ', title, 1)
            time.sleep(random.randint(11, 20))
            targetP = target.split('.html')
            if pageTotal > 0:
                for ind in range(pageTotal):
                    page_num = ind + 2
                    url_p = targetP[0] + '/' + str(page_num) + '.html'
                    html_p = conn_contents(self.proxies, url_p)
                    if html_p:
                        bfp = BeautifulSoup(html_p, "html5lib")
                        text_p = bfp.find_all('div', class_='content')
                        text_p = str(text_p[0])
                        cont_p = re.findall(pattern, text_p)
                        conts = conts + cont_p[1:]
                        print('已下载： ', title, ind + 2)
                        time.sleep(random.randint(11, 20))
                    else:
                        self.fails.append(url_p)
                        print('下载失败：', title, ind + 2)
                        print(url_p)
            for i in range(len(conts)):
                conts[i] = conts[i].replace('<p>', '')  # 去掉<p>
                conts[i] = conts[i].replace('</p>', '\n')  # 去掉</p>

            return conts[1:]
        else:
            self.fails.append(target)
            print('下载失败', target)
            return []


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

    # my_headers = {
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
    # }
    # test_url = 'https://www.1qxs.com/xs/64130/132.html'
    # proxies = ['http://27.42.168.46:55481', 'http://27.42.168.46:55481']
    # req = requests.get(url=test_url, proxies={'http': proxies[0]}, headers=my_headers)
    # req.encoding = req.apparent_encoding  # 因为网站头部没有指定编码，因此需要requests自己去判断
    # html = req.text
    # bf = BeautifulSoup(html, "html5lib")
    # title = bf.find('h1')
    # title = str(title)
    # # print(html)
    # title = '<h1>卷二 第131章 屠夫楼宁(1/4)</h1>'
    # pagePattern = re.compile('\/\d\)')
    # numPattern = re.compile('\d')
    # pageTotal = re.findall(pagePattern, title)
    # pageTotal = re.findall(numPattern, pageTotal[0])
    # pageTotal = int(pageTotal[0]) - 1
    # print(pageTotal)
    # for ind in range(pageTotal):
    #     pageNum = ind + 2
    #     print(pageNum)
    #
    # texts = bf.find_all('div', class_='content')
    # texts = str(texts[0])
    #
    # pattern = re.compile('.*?</p>')
    # conts = re.findall(pattern, texts)
    # for i in range(len(conts)):
    #     conts[i] = conts[i].replace('<p>', '')  # 去掉<p>
    #     conts[i] = conts[i].replace('</p>', '\n')  # 去掉</p>
    #
    # print(conts)

    dl = downloader()
    dl.get_download_url()
    for i in range(dl.nums):
        dl.writer(dl.names[i], '这太子不做也罢.txt', dl.get_contents(dl.urls[i]))
    print('下载完成!')
    print('下载失败链接')
    print(dl.fails)

