# coding=utf-8
# author:ss
from core.base_page import Page


class LecturePreparePage(Page):
    class_input = ('xpath', '/html/body/div[1]/div/div[2]/div[1]/div[1]/div/div[1]/input')
    class_list = ('xpath', '/html/body/div[5]/div/div[1]/ul')
    lesson_input = ('xpath', '/html/body/div[1]/div/div[2]/div[2]/div[1]/div/div[1]/input')
    lesson_list = ('xpath', '/html/body/div[5]/div/div[1]/ul')
    live_room_input = ('xpath', '/html/body/div[1]/div/div[2]/div[3]/div[1]/div/div[1]/input')
    live_room_list = ('xpath', '/html/body/div[5]/div/div[1]/ul')
    enter_btn = ('xpath', '/html/body/div[1]/div/div[2]/button')

    def __init__(self):
        super(LecturePreparePage, self).__init__(browser_type='chrome')

    def start_class(self):
        class_ = u"高斯数学初三能力强化(测试使用，请勿购买)"
        lesson = u"第1讲   几何图形初步-城市版-xa"
        live_room = u"亚静直播间二"
        self.click(self.class_input)
        self.select_list(class_, self.class_list)
        self.click(self.lesson_input)
        self.select_list(lesson, self.lesson_list)
        self.click(self.live_room_input)
        self.select_list(live_room, self.live_room_list)
        self.click(self.enter_btn)


