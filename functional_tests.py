from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest

class NewVisitorTesT(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # 사용자는 To-Do 웹 사이트에 방문한다.
        self.browser.get("http://localhost:8000")

        # To-Do 웹 사이트의 타이틀 헤더엔 "To-Do" 가 포함 되어 있다.
        self.assertIn("To-Do", self.browser.title)
        header_text = self.browser.find_element("css selector", "h1").text
        self.assertIn("To-Do Lists", header_text)
 
        # 사용자는 작업을 추가하기로 한다.
        input_box = self.browser.find_element(value="id_new_item")
        self.assertEqual(input_box.get_attribute("placeholder"), "작업 아이템 입력")
        
        # "공작 깃털 사기" 라는 텍스트 상자에 추가한다.
        input_box.send_keys("공작 깃털 사기")
        
        # 엔터키를 치면 페이지가 갱신되고 작업 목록에 '1: 공작 깃털 사기' 아이템이 추가된다.
        input_box.send_keys(Keys.ENTER)
        
        table = self.browser.find_element(value="id_list_table")
        rows = table.find_elements("css selector", "tr")
        self.assertTrue(any(row.text == "1: 공작 깃털 사기" for row in rows), "신규 작업이 테이블에 추가되지 않음.")
        
        # 추가 아이템을 입력할 수 있는 여분의 텍스트 상자가 존재한다.
        # 이번엔 "공작 깃털을 이용해 그물 만들기"라고 텍스트 상자에 입력하고 엔터키를 친다.
        self.fail("Finish the test!")

        # 페이지는 다시 갱신되고 두 개의 작업 목록이 존재한다.
        # 사이트는 사용자에게 특정 URL을 생성해준다.
        # 이때 URL에 대한 설명도 함께 제공된다.

        # 해당 URL에 접속하면 사용자가 만든 작업 목록이 그대로 있는 것을 확인할 수 있다.

if __name__ == "__main__":
    unittest.main(warnings="ignore")