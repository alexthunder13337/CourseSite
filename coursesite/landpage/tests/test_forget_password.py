from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.http import QueryDict
from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from landpage.views import forgot_password
import json
from landpage.models import LandpageTeamMember
from landpage.models import LandpageCoursePreview
from registrar.models import Course
from registrar.models import Student
from registrar.models import Teacher


TEST_USER_EMAIL = "test@fakemail.ru"
TEST_USER_USERNAME = "fakeuser"
TEST_USER_PASSWORD = "fakepass"


class ForgotPasswordTest(TestCase):
    def tearDown(self):
        courses = Course.objects.all()
        for course in courses:
            course.delete()
        User.objects.get(email=TEST_USER_EMAIL).delete()
    
    def setUp(self):
        User.objects.create_user(
            email=TEST_USER_EMAIL,
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        user = User.objects.get(email=TEST_USER_EMAIL)
        teacher = Teacher.objects.create(user=user)
        student = Student.objects.create(user=user)
        course = Course.objects.create(
            id=1,
            title="TEST COURSE",
            sub_title="About...",
            category="",
            teacher=teacher,
        )


    def test_url_resolves_to_forgot_password_page(self):
        found = resolve('/forgot_password');
        self.assertEqual(found.func,forgot_password.forgot_password_page)

    def test_forgot_password_page_returns_correct_html(self):
        parameters = {"course_id":1}
        client = Client()
        response = client.post(
            '/forgot_password',
            data=parameters,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Забыл пароль',response.content)
