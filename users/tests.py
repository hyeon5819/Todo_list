from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

# Create your tests here.


class UserRegistrationAPIViewTestCase(APITestCase):
    def test_registration(self):
        url = reverse("user_view")
