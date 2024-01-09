from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException

from django.test import LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

import time

MAX_WAIT = 5

class NewVisitorTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        
        while True:
            try:
                table = self.browser.find_element(value="id_list_table")
                rows = table.find_elements("tag name", "tr")
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException):
                if time.time() - start_time > MAX_WAIT:
                    raise
                time.sleep(0.5)
            
    def test_can_start_a_todo_list(self):
        # 사용자는 To-Do 웹 사이트에 방문한다.
        self.browser.get(self.live_server_url)

        # To-Do 웹 사이트의 타이틀 헤더엔 "To-Do" 가 포함 되어 있다.
        self.assertIn("To-Do", self.browser.title)
        header_text = self.browser.find_element("tag name", "h1").text
        self.assertIn("To-Do Lists", header_text)
 
        # 사용자는 작업을 추가하기로 한다.
        input_box = self.browser.find_element(value="id_new_item")
        self.assertEqual(input_box.get_attribute("placeholder"), "작업 아이템 입력")
        
        # "공작 깃털 사기" 라는 텍스트 상자에 추가한다.
        input_box.send_keys("공작 깃털 사기")
        # 엔터키를 치면 페이지가 갱신되고 작업 목록에 '1: 공작 깃털 사기' 아이템이 추가된다.
        input_box.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: 공작 깃털 사기")
        
        # 추가 아이템을 입력할 수 있는 여분의 텍스트 상자가 존재한다.
        input_box = self.browser.find_element(value="id_new_item")
        # 이번엔 "공작 깃털을 이용해 그물 만들기"라고 텍스트 상자에 입력하고 엔터키를 친다.
        input_box.send_keys("공작 깃털을 이용해 그물 만들기")
        input_box.send_keys(Keys.ENTER)

        # 페이지는 다시 갱신되고 두 개의 작업 목록이 존재한다.
        self.wait_for_row_in_list_table("1: 공작 깃털 사기")
        self.wait_for_row_in_list_table("2: 공작 깃털을 이용해 그물 만들기")

    def test_multiple_users_can_starts_lists_at_different_urls(self):

        # 에디스(첫 번째 사용자)가 to-do list를 생성하고 사용한다.

        self.browser.get(self.live_server_url)

        inputbox = self.browser.find_element("id", "id_new_item")
        inputbox.send_keys("공작 깃털 사기")
        inputbox.send_keys(Keys.ENTER)

        self.wait_for_row_in_list_table("1: 공작 깃털 사기")

        # 에디스의 to-do list가 고유의 URL을 갖는지 확인한다.
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, "/lists/.+")


        ## 새로운 사용자 세션을 위해 브라우저의 쿠키를 삭제
        self.browser.delete_all_cookies()


        # 새로운 사용자 프랜시스가 홈페이지에 방문한다.
        self.browser.get(self.live_server_url)

        # 이전 사용자인 에디스의 작업 목록이 나타나지 않는 것을 확인한다.
        page_text = self.browser.find_element("tag name", "body").text
        self.assertNotIn("공작 깃털 사기", page_text)

        # 프랜시스도 새로운 작업 목록을 생성하고 작업 Item을 추가한다.
        inputbox = self.browser.find_element("id", "id_new_item")
        inputbox.send_keys("우유 사기")
        inputbox.send_keys(Keys.ENTER)

        self.wait_for_row_in_list_table("1: 우유 사기")

        # 프랜시스의 to-do list가 고유한 URL을 갖는지 확인한다.
        francis_list_url = self.browser.current_url

        self.assertRegex(francis_list_url, "/lists/.+")
        self.assertNotEqual(francis_list_url, edith_list_url)

        # 다시 프랜시스가 보고 있는 페이지에 에디스의 작업 목록이 없는 지 확인한다.
        page_text = self.browser.find_element("tag name", "body").text
        self.assertNotIn("공작 깃털 사기", page_text)
        self.assertIn("우유 사기", page_text)


    def test_layout_and_styling(self):
        # 에디스는 메인 페이지를 방문한다. 접속된 웹 브라우저의 크기는 1024 X768 이다.
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        # 그녀는 입력 상자가 가운데 배치된 것을 본다. (offset = 10px)
        inputbox = self.browser.find_element("id", "id_new_item")
        inputbox.send_keys("testings")
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: testings")

        inputbox = self.browser.find_element("id", "id_new_item")
        self.assertAlmostEqual(inputbox.location['x'] + inputbox.size["width"]/2, 512, delta=10)

