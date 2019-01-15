# coding=utf-8
# author:ss

from core.base_page import Page


class CoursewarePage(Page):
    this_courseware = ('xpath', '//*[@id="app"]/div[2]/div[1]/ul[2]/li/a')
    catalog_btn = ('xpath', '//*[@id="toc-button"]')
    catalog_detail = ('xpath', '//*[@id="toc-container"]/ul/li[1]/ul')
    exa_6 = ('xpath', '//*[@id="toc-container"]/ul/li[1]/ul/li[6]')
    ask_ques_btn = ('xpath', '//*[@id="app"]/div[2]/div[1]/ul[4]/li[2]/a')
    random_open_mic = ('xpath', '//*[@id="app"]/div[2]/div[1]/ul[4]/li[1]/a')

    def ask_sample_question(self):
        self.click(self.this_courseware)
        self.click(self.catalog_btn)
        # self.click(self.exa_6)
        self.select_list(u"例6", self.catalog_detail, type_="text")
        if self.get_attribute(self.ask_ques_btn, 'class') == "icon_ask_question":
            self.click(self.ask_ques_btn)

    def random_open_microphone(self):
        self.click(self.random_open_mic)