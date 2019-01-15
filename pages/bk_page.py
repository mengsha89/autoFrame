# coding=utf-8
# author:ss

from core.base_page import Page


class PrepareLessonPage(Page):
    dt_entrance_btn = ('xpath', '//*[@id="app"]/div[2]/div[4]/div/a')

    def enter_datiqi(self):
        self.open_new_window(self.dt_entrance_btn)
