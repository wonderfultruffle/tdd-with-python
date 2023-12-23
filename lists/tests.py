from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string

from lists.views import home_page

# Create your tests here.
class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)
        
    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        
        # self.assertTrue(response.content.startswith(b"<html>"))
        # self.assertIn(b"<title>To-Do Lists</title>", response.content)
        # self.assertTrue(response.content.strip().endswith(b"</html>"))
        # 위 세줄은 다음의 두 줄로 대체한다.
        expected_html = render_to_string("lists/home.html")
        self.assertEqual(response.content.decode(), expected_html) # 기존의 문자열을 직접 사용하는 테스트는 상수를 테스트하는 것과 다를 바 없다.
                                                                   # 단위 테스트는 로직의 흐름, 제어, 설정 등을 테스트하는 것이 목적
                                                                   # 상수를 테스트하는 것은 이러한 목적과 연관이 없다.
                                                                   # 따라서 기존의 문자열을 render_to_string()로 대체하고 이를 응답 html과 비교하는 테스트를 수행하여
                                                                   # 상수가 아닌 '구현 결과물'을 테스트하도록 하는 것이 더 의미있고 바람직하다.