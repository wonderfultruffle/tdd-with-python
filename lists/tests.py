from django.test import TestCase
from django.urls import resolve

from lists.views import home_page
from lists.models import Item, List

# Create your tests here.
class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)
        
    # def test_home_page_returns_correct_html_old(self):
    #     request = HttpRequest()
    #     response = home_page(request)
    #
    #     # self.assertTrue(response.content.startswith(b"<html>"))
    #     # self.assertIn(b"<title>To-Do Lists</title>", response.content)
    #     # self.assertTrue(response.content.strip().endswith(b"</html>"))
    #     # 위 세줄은 다음의 두 줄로 대체한다.
    #     expected_html = render_to_string("lists/home.html")
    #     self.assertEqual(response.content.decode(), expected_html) # 기존의 문자열을 직접 사용하는 테스트는 상수를 테스트하는 것과 다를 바 없다.
    #                                                                # 단위 테스트는 로직의 흐름, 제어, 설정 등을 테스트하는 것이 목적
    #                                                                # 상수를 테스트하는 것은 이러한 목적과 연관이 없다.
    #                                                                # 따라서 기존의 문자열을 render_to_string()로 대체하고 이를 응답 html과 비교하는 테스트를 수행하여
    #                                                                # 상수가 아닌 '구현 결과물'을 테스트하도록 하는 것이 더 의미있고 바람직하다.
    # ===> Django의 TestClient를 사용하지 않고 Test
    #      위 함수는 아래의 TestClient를 사용하는 'test_home_page_returns_correct_html()'로 대체한다.(최신 문서 기준)
    def test_home_page_returns_correct_html(self): # substitute for 'test_home_page_returns_correct_html_ole()'
        response = self.client.get("/")
        self.assertTemplateUsed(response, "lists/home.html")

    # def test_home_page_can_save_a_POST_request(self):
    #     response = self.client.post("/", data={"item_text": "신규 작업 아이템"})
    #
    #     self.assertEqual(Item.objects.count(), 1)
    #     new_item = Item.objects.first()
    #     self.assertEqual(new_item.text, "신규 작업 아이템")

    # def test_home_page_redirects_after_POST(self):
    #     response = self.client.post('/', data={"item_text":"신규 작업 아이템"})
    #
    #     # self.assertContains(response, "신규 작업 아이템")
    #     # self.assertTemplateUsed(response, "lists/home.html") # 'POST 요청을 처리한 후에는 반드시 Redirect 하라.' -> 아래 Code로 대체
    #     # self.assertEqual(response.status_code, 302)
    #     # self.assertEqual(response["location"], '/')
    #     self.assertRedirects(response, '/lists/the-only-list-in-the-world/') # 위 두줄을 현재 줄로 대체.(Django 최신 버전 기능)

    # def test_home_page_only_saves_items_when_it_necessary(self):
    #     response = self.client.get("/")
    #
    #     self.assertEqual(Item.objects.count(), 0)

    # def test_home_page_display_all_list_items(self): => ListViewTest의 test_display_all_items() 로 대체
    #     Item.objects.create(text="신규 작업 목록 1")
    #     Item.objects.create(text="신규 작업 목록 2")
    #
    #     response = self.client.get('/')
    #
    #     for item in Item.objects.all():
    #         self.assertContains(response, item.text)

class ListItemModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        mylist = List()
        mylist.save()

        first_item = Item()
        first_item.text = "첫 번째 아이템"
        first_item.list = mylist
        first_item.save()

        second_item = Item()
        second_item.text = "두 번째 아이템"
        second_item.list = mylist
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        saved_list = List.objects.get()
        self.assertEqual(saved_list, mylist)

        first_saved_item = saved_items[0]
        self.assertEqual(first_saved_item.text, "첫 번째 아이템")
        self.assertEqual(first_saved_item.list, mylist)

        second_saved_item = saved_items[1]
        self.assertEqual(second_saved_item.text, "두 번째 아이템")
        self.assertEqual(second_saved_item.list, mylist)

class ListViewTest(TestCase):
    def test_use_list_template(self):
        mylist = List.objects.create()
        response = self.client.get(f"/lists/{mylist.id}/")
        self.assertTemplateUsed(response, "lists/list.html")

    def test_displays_only_items_for_that_list(self):
        correct_list = List.objects.create()
        Item.objects.create(text="신규 아이템 1", list=correct_list)
        Item.objects.create(text="신규 아이템 2", list=correct_list)

        other_list = List.objects.create()
        Item.objects.create(text="다른 목록 아이템 1", list=other_list)
        Item.objects.create(text="다른 목록 아이템 2", list=other_list)

        response = self.client.get(f"/lists/{correct_list.id}/")

        self.assertContains(response, "신규 아이템 1")
        self.assertContains(response, "신규 아이템 2")
        self.assertNotContains(response, "다른 목록 아이템 1")
        self.assertNotContains(response, "다른 목록 아이템 2")


class NewListTest(TestCase):

    def test_can_save_a_POST_request(self):
        self.client.post("/lists/new", data={"item_text": "신규 작업 아이템"})
        self.assertEqual(Item.objects.count(), 1)

        new_item = Item.objects.first()
        self.assertEqual(new_item.text, "신규 작업 아이템")

    def test_redirect_after_POST(self):
        response = self.client.post("/lists/new", data={"item_text": "신규 작업 아이템"})

        new_list = List.objects.first()
        self.assertRedirects(response, f"/lists/{new_list.id}/")

