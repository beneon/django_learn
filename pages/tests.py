from django.test import TestCase
from django.contrib.auth import get_user_model
from django.test import SimpleTestCase
from django.urls import reverse
from faker import Faker
# Create your tests here.

class HomePageTests(SimpleTestCase):

    def test_home_page_status_code(self):
        res = self.client.get('/')
        self.assertEqual(res.status_code, 200)

    def test_view_url_by_name(self):
        res = self.client.get(reverse('home'))
        self.assertEqual(res.status_code,200)
        self.assertTemplateUsed(res,'home.html')


class SignupPageTests(TestCase):
    fk = Faker('zh_CN')
    profile = fk.profile()

    def test_signup_page_status_code(self):
        res = self.client.get('/users/signup')