# -*- coding:UTF-8 -*-
import requests
from lxml import etree
import time

# 获取快代理首页的代理
def get_proxy_list(num = 1):
    page_size = num
    payload = {}
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
        'Accept': 'application/json, text/javascript, */*; q=0.01',
    }
    type_dct = {
        "HTTP": "http://",
        "HTTPS": "https://"
    }
    res = []
    page_index = 0
    for index in range(page_size):
        page_index += 1
        url = "https://www.kuaidaili.com/free/inha/" + str(page_index)
        response = requests.request("GET", url, headers=headers, data=payload)
        response.encoding = response.apparent_encoding
        _ = etree.HTML(response.text)
        data_list = _.xpath("//tbody/tr")
        for data in data_list:
            ip = data.xpath("./td[1]/text()")[0]
            port = data.xpath("./td[2]/text()")[0]
            type = data.xpath("./td[4]/text()")[0]
            res.append(type_dct[type] + ip + ':' + port)
        time.sleep(3)
    return res

# 测试代理
def check(proxy):
    href = 'https://www.1qxs.com/'
    if 'https' in proxy:
        proxies = {'https': proxy}
    else:
        proxies = {'http': proxy}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4396.0 Safari/537.36'
    }
    try:
        r = requests.get(href, proxies=proxies, timeout=3, headers=headers)
        if r.status_code == 200:
            return True
    except:
        return False

if __name__ == '__main__':
    proxies = get_proxy_list(3)
    print(proxies)
    ind = 1
    nums = len(proxies)
    proxy_list = []
    for p in proxies:
        print('\r', '正在测试：  %.3f%%' % float(ind / nums * 100), end='', flush=True)
        if(check(p)):
            proxy_list.append(p)
        ind += 1
    print('\r', proxy_list)

