"""
不同网站的解析及下载方式
"""
import re
from tkinter import END
from lxml import etree

import requests
from bs4 import BeautifulSoup


def tieba(site_name, url, frame):
    """
    贴吧下载图片
    :return:
    """
    res = requests.get(url, timeout=5)
    soup = BeautifulSoup(res.text, 'html.parser')
    pn = soup.select(".l_reply_num ")[0].select('.red')[1].text
    title = soup.select(".core_title_txt ")[0].text
    frame.textare.insert(END, '开始从 {} 下载... \n'.format(site_name))
    frame.textare.update()
    sub_folder = frame._check_folder(title)
    for p in range(1, int(pn) + 1):  # pagecount +1 总页数+1
        page = requests.get(url + '?pn=' + str(p)).text
        doc = BeautifulSoup(page, 'html.parser')
        for el in doc.select('img.BDE_Image'):
            name = el['src'].split('/')[6]
            hd_re = re.compile("(http://imgsrc.baidu.com/forum)/.*?/sign=.*?/(.*?.jpg)")
            hd_url_tuple = hd_re.search(el['src']).groups()
            hd_ref = '{}/pic/item/{}'.format(*hd_url_tuple)
            # 替换为高清图片地址
            with open('{}/{}'.format(sub_folder, name), 'wb') as f:
                ret = requests.get(hd_ref)
                if ret.status_code == 200:
                    f.write(requests.get(hd_ref).content)
                    frame.textare.insert(END, '{} 下载成功!\n'.format(hd_ref))
                    frame.textare.update()
    frame.textare.insert(END, '图片下载完毕!\n')
    frame.textare.update()


def weibo(site_name, wid, frame):
    res = requests.get("https://m.weibo.cn/detail/{}".format(wid), timeout=5)
    pic_pattern = re.compile('"url": "(https://.+/large/.+)"')
    title_pattern = re.compile('"text": "(.+)",')
    title_area = title_pattern.findall(res.text)[0]
    title_soup = BeautifulSoup(title_area, 'html.parser')
    title = title_soup.text.strip().replace(" ", "").replace("#", "").replace("@", "").replace("：", "")
    frame.textare.insert(END, '开始从 {} 下载... \n'.format(site_name))
    frame.textare.update()
    pic_list = pic_pattern.findall(res.text)
    sub_folder = frame._check_folder(title)
    for path in pic_list:
        pic_name = path.split('/')[-1]
        with open(r'{}/{}'.format(sub_folder, pic_name), 'wb') as f:
            ret = requests.get(path)
            if ret.status_code == 200:
                f.write(requests.get(path).content)
                frame.textare.insert(END, '{} 下载成功!\n'.format(path))
                frame.textare.update()
    frame.textare.insert(END, '图片下载完毕!\n')
    frame.textare.update()
