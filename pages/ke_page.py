# coding=utf-8
# author:ss


from core.base_page import Page


class KePage(Page):
    ke = ('xpath', '//*[@id="header-left-list"]/div[2]/div/a')
    all_class = ('xpath', '//*[@id="app"]/div[2]/div[2]/div[1]/div[2]/div/ul')
    lesson_list = ('xpath', '//*[@id="app"]/div[2]/div[2]/div[1]/div[2]/div/div/div[2]/div[2]/div/ul')
    lesson_1 = ('xpath', '//*[@id="app"]/div[2]/div[2]/div[1]/div[2]/div/div/div[2]/div[2]/div/ul/li[1]/a')

    def enter_ke_page(self):
        self.click(self.ke)
        self.select_list(u"高斯数学初一思维突破(人教版)（测试使用）", self.all_class, type_="text", sele="/li[%d]/a/div[1]/div")
        self.click(self.lesson_1)
