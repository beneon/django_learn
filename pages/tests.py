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
        res = self.client.get('/users/signup/')
        self.assertEqual(res.status_code, 200)

    def test_view_url_by_name(self):
        res = self.client.get(reverse('signup'))
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'signup.html')

    def test_signup_process(self):
        new_user = get_user_model().objects.create_user(
            self.profile['username'],
            self.profile['mail']
        )
        self.assertEqual(
            get_user_model().objects.all().count(),1
        )
        user_id1 = get_user_model().objects.get(id=1)
        self.assertEqual(user_id1.username, self.profile['username'])
        self.assertEqual(user_id1.email, self.profile['mail'])
