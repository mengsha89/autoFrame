# coding=utf-8
# author:ss

import time
from selenium.webdriver.common.action_chains import ActionChains
from core.browser import Browser
from utils.log import *


class Page(Browser):
    def __init__(self, browser_type='chrome'):
        super(Page, self).__init__(browser_type=browser_type)

    def wait(self, seconds=3):
        self.driver.implicitly_wait(seconds)

    def js(self, script, *args):
        self.driver.execute_script(script, *args)

    def move_to(self, element):
        ActionChains(self.driver).move_to_element(element).perform()

    def get_element(self, *loc):

        by, value = loc
        by = by.lower()

        if by == "id":
            element = self.driver.find_element_by_id(value)
        elif by == "name":
            element = self.driver.find_element_by_name(value)
        elif by == "class":
            element = self.driver.find_element_by_class_name(value)
        elif by == "link_text":
            element = self.driver.find_element_by_link_text(value)
        elif by == "xpath":
            element = self.driver.find_element_by_xpath(value)
        elif by == "css":
            element = self.driver.find_element_by_css_selector(value)
        else:
            raise NameError("Please enter the correct targeting elements,'id','name','class','link_text','xpaht','css'.")
        return element

    def get_elements(self, *loc):

        by, value = loc
        by = by.lower()

        if by == "id":
            elements = self.driver.find_elements_by_id(value)
        elif by == "name":
            elements = self.driver.find_elements_by_name(value)
        elif by == "class":
            elements = self.driver.find_elements_by_class_name(value)
        elif by == "link_text":
            elements = self.driver.find_elements_by_link_text(value)
        elif by == "xpath":
            elements = self.driver.find_elements_by_xpath(value)
        elif by == "css":
            elements = self.driver.find_elements_by_css_selector(value)
        else:
            raise NameError("Please enter the correct targeting elements,'id','name','class','link_text','xpaht','css'.")
        return elements

    def select_list(self, value, list_loc, attr='title', sele="/li[%d]", type_='attr'):
        """

        :param value:
        :param list_loc:
        :param attr:
        :param sele:
        :param type_: attr属性，text文本
        :return:
        """
        eles = self.get_elements(list_loc)
        eles_num = len(eles)
        by, val = list_loc
        if eles_num == 1:
            val = val + "/li"
            select_loc = by, val
            self.click(select_loc)
        for i in range(len(eles)):
            val = val + sele % i
            select_loc = by, val
            if type_ == "attr":
                text = self.get_attribute(select_loc, attr)
                if text == value:
                    self.click(select_loc)
            elif type_ == "text":
                text = self.get_text(select_loc)
                if text == value:
                    self.click(select_loc)

    def type(self, loc, text):
        self.get_element(*loc).send_keys(text)

    def click(self, loc):
        self.get_element(*loc).click()

    def right_click(self, loc):
        el = self.get_element(*loc)
        ActionChains(self.driver).context_click(el).perform()

    def move_to_element(self, loc):
        el = self.get_element(*loc)
        ActionChains(self.driver).move_to_element(el).perform()

    def double_click(self, loc):

        el = self.get_element(*loc)
        ActionChains(self.driver).double_click(el).perform()

    def drag_and_drop(self, el_ele, ta_ele):
        """
        Usage:
        driver.drag_and_drop("id->kw","id->su")
        """
        element = self.get_element(*el_ele)
        target = self.get_element(*ta_ele)
        ActionChains(self.driver).drag_and_drop(element, target).perform()

    def click_text(self, text):
        """
        Usage:
        driver.click_text("新闻")
        """
        self.driver.find_element_by_partial_link_text(text).click()

    def submit(self, loc):
        self.get_element(*loc).submit()

    def get_attribute(self, loc, attribute):
        """
        Usage:
        driver.get_attribute(("id","su"),"href")
        """
        el = self.get_element(*loc)
        attr = el.get_attribute(attribute)
        return attr

    def get_text(self, loc):
        text = self.get_element(*loc).text
        return text

    def accept_alert(self):
        """
        Usage:
        driver.accept_alert()
        """
        self.driver.switch_to.alert.accept()

    def dismiss_alert(self):
        """
        Usage:
        driver.dismiss_alert()
        """
        self.driver.switch_to.alert.dismiss()

    def switch_to_frame(self, css):
        iframe_el = self.get_element(css)
        self.driver.switch_to.frame(iframe_el)

    def switch_to_frame_out(self):
        """
        Usage:
        driver.switch_to_frame_out()
        """
        self.driver.switch_to.default_content()

    def open_new_window(self, loc):
        """
        Open the new window and switch the handle to the newly opened window.

        """
        original_windows = self.driver.current_window_handle
        self.click(loc)
        all_handles = self.driver.window_handles
        for handle in all_handles:
            if handle != original_windows:
                self.driver.switch_to.window(handle)

    def into_new_window(self):
        """
        Usage:
        dirver.into_new_window()
        """
        all_handle = self.driver.window_handles
        flag = 0
        while len(all_handle) < 2:
            time.sleep(1)
            all_handle = self.driver.window_handles
            flag += 1
            if flag == 5:
                break
        self.driver.switch_to.window(all_handle[-1])

    def switch_to_window(self, partial_url='', partial_title=''):
        """
        切换窗口
            如果窗口数<3,不需要传入参数，切换到当前窗口外的窗口；
            如果窗口数>=3，则需要传入参数来确定要跳转到哪个窗口
        """
        logger.info("开始切换窗口！")
        all_windows = self.driver.window_handles
        if len(all_windows) == 1:
            logger.warn('只有1个window!')
        elif len(all_windows) == 2:
            other_window = all_windows[1 - all_windows.index(self.current_window)]
            self.driver.switch_to.window(other_window)
        else:
            for window in all_windows:
                self.driver.switch_to.window(window)
                if partial_url in self.driver.current_url or partial_title in self.driver.title:
                    break
        logger.debug(self.driver.current_url, self.driver.title)

    def switch_to_alert(self):
        return self.driver.switch_to.alert

