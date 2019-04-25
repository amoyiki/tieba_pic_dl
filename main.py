# -*- coding:utf-8 -*-
"""
百度贴吧贴子中图片一键下载
@author amoyiki
@date 2019/04/13
"""
from pathlib import Path
from tkinter import *
from tkinter import scrolledtext
from tkinter.ttk import Combobox

import site_factory


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
        self.textare = scrolledtext.ScrolledText(self, bg='white', height=20)
        self.textare.pack(fill=BOTH, side=TOP, expand=True)
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
        # 下拉
        self.select_label = Label(
            self.fm3,
            text='网站选择',
            font=('微软雅黑', 16), fg="white", bg='black',
            width=10
        )
        self.site_select = Combobox(self.fm3)
        self.site_select['values'] = ('tieba', 'weibo', 'bilibili',)  # 设置下拉列表的值
        self.site_select.pack(side=LEFT, fill=X, padx=30)
        self.site_select.current(0)
        self.site_select.bind("<<ComboboxSelected>>", self.choose_func)

        # button
        self.btn = Button(self.fm3, text='下载', width=5, command=self.start_download)
        self.btn.pack(side=RIGHT, fill=X, padx=15)
        self.fm3.pack(side=TOP)
        # self.fm2 = Frame(self, bg='black')

    def choose_func(self, *args):
        """
        下拉触发事件
        :return:
        """
        print(self.site_select.get())

    def start_download(self):
        input_text = self.input.get()
        site_name = self.site_select.get()
        analysis = getattr(site_factory, site_name)
        analysis(site_name, input_text, self)

    def _check_folder(self, sub_name):
        sub_name = re.sub('[\/:*?"<>|]', '', sub_name)
        img_folder = Path('img/{}'.format(sub_name))
        if img_folder and img_folder.is_dir():
            pass
        else:
            img_folder.mkdir(parents=True)
        return "{}/{}".format(Path.cwd(), 'img/{}'.format(sub_name))


if __name__ == '__main__':
    app = Application()
    app.mainloop()
