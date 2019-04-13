# -*- coding:utf-8 -*-
"""
百度贴吧贴子中图片一键下载
@author amoyiki
@date 2019/04/13
"""
from pathlib import Path
from tkinter import *

import requests
from bs4 import BeautifulSoup


class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master, bg='black')
        self.pack(expand=YES, fill=BOTH)
        self.window_init()
        self.create_widgets()

    def window_init(self):
        self.master.title('贴吧图片一键下载')
        self.master.bg = 'black'
        width, height = self.master.maxsize()
        self.master.geometry('{}x{}'.format(width // 2, height // 2))

    def create_widgets(self):
        # top
        self.fm1 = Frame(self, bg='black')
        self.title_label = Label(
            self.fm1,
            text='贴吧图片下载',
            font=('微软雅黑', 16), fg="white", bg='black',
            width=30
        )
        self.title_label.pack(side=TOP)
        self.fm1.pack(side=TOP)
        # mid
        self.textare = Text(self, bg='white', height=20)
        self.textare.pack(fill='x', pady=20, side=TOP)
        # bottom
        self.fm3 = Frame(self, bg='black')
        self.btn_label = Label(
            self.fm3,
            text='地址',
            font=('微软雅黑', 16), fg="white", bg='black',
            width=10
        )
        self.btn_label.pack(side=LEFT, fill=X, padx=1)
        self.input = Entry(self.fm3, width=60)
        self.input.pack(side=LEFT)
        # button
        self.btn = Button(self.fm3, text='下载', width=5, command=self.start_download)
        self.btn.pack(side=RIGHT, fill=X, padx=15)
        self.fm3.pack(side=TOP)
        # self.fm2 = Frame(self, bg='black')

    def start_download(self):
        url = self.input.get()
        res = requests.get(url, timeout=5)
        soup = BeautifulSoup(res.text, 'html.parser')
        pn = soup.select(".l_reply_num ")[0].select('.red')[1].text
        title = soup.select(".core_title_txt ")[0].text
        self.textare.insert('insert', '开始下载... \n')
        self.textare.update()
        sub_folder = self._check_folder(title)
        print(sub_folder)
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
                        self.textare.insert('insert', '{} 下载成功!\n'.format(hd_ref))
                        self.textare.update()
        self.textare.insert('insert', '图片下载完毕!\n')

    def _check_folder(self, sub_name):
        img_folder = Path('img/{}'.format(sub_name))
        if img_folder and img_folder.is_dir():
            pass
        else:
            img_folder.mkdir(parents=True)
        return "{}/{}".format(Path.cwd(), 'img/{}'.format(sub_name))


if __name__ == '__main__':
    app = Application()
    app.mainloop()
