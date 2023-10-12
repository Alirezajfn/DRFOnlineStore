from django.contrib.auth import get_user_model
from django.urls import reverse
from model_bakery import baker
from rest_framework import status
from rest_framework.test import APITestCase


class UserCreateTests(APITestCase):

    def setUp(self) -> None:
        self.dummy_verified_email = 'verified@test.com'
        self.username = 'test_user'
        self.correct_password = 'test_password'
        self.url = reverse('users:user-list')

    def test_with_mismatching_password_and_confirm_password(self):
        data = {
            'username': self.username,
            'email': self.dummy_verified_email,
            'password': self.correct_password,
            'confirm_password': 'wrong_password'
        }

        response = self.client.post(self.url, data=data)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(get_user_model().objects.count(), 0)

    def test_create_user_successfully(self):
        data = {
            'username': self.username,
            'email': self.dummy_verified_email,
            'password': self.correct_password,
            'confirm_password': self.correct_password
        }

        response = self.client.post(self.url, data=data)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(get_user_model().objects.count(), 1)
        self.assertEquals(get_user_model().objects.first().username, self.username)
        self.assertEquals(get_user_model().objects.first().email, self.dummy_verified_email)
        self.assertTrue(get_user_model().objects.first().check_password(self.correct_password))

    def test_with_existing_username_fails(self):
        baker.make(get_user_model(), username=self.username)
        data = {
            'username': self.username,
            'email': self.dummy_verified_email,
            'password': self.correct_password,
            'confirm_password': self.correct_password
        }

        response = self.client.post(self.url, data=data)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(get_user_model().objects.count(), 1)

    def test_with_existing_email_fails(self):
        baker.make(get_user_model(), email=self.dummy_verified_email)
        data = {
            'username': self.username,
            'email': self.dummy_verified_email,
            'password': self.correct_password,
            'confirm_password': self.correct_password
        }

        response = self.client.post(self.url, data=data)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(get_user_model().objects.count(), 1)

    def test_with_weak_password(self):
        data = {
            'username': self.username,
            'email': self.dummy_verified_email,
            'password': '123',
            'confirm_password': '123'
        }

        response = self.client.post(self.url, data=data)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(get_user_model().objects.count(), 0)


class UserRetrieveUpdateTests(APITestCase):

    def setUp(self):
        self.user = baker.make(get_user_model())
        self.client.force_login(self.user)

        baker.make(get_user_model())
        baker.make(get_user_model())
        baker.make(get_user_model())

    def test_retrieve_someone_else_data_gets_is_not_possible(self):
        another_user = baker.make(get_user_model())

        url = reverse('users:user-detail', args=[another_user.username])

        response = self.client.get(url)
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_someone_else_data_gets_is_not_possible(self):
        another_user = baker.make(get_user_model())

        url = reverse('users:user-detail', args=[another_user.username])
        data = {
            'first_name': 'new_first_name'
        }

        response = self.client.get(url)
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)
        another_user.refresh_from_db()
        self.assertNotEqual(another_user.first_name, data['first_name'])

    def test_retrieve_user_with_not_being_authenticated_is_not_possible(self):
        self.client.logout()

        url = reverse('users:user-list')

        response = self.client.get(url)
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_user_with_not_being_authenticated_is_not_possible(self):
        self.client.logout()

        url = reverse('users:user-detail', args=[self.user.username])
        data = {
            'first_name': 'new_first_name'
        }

        response = self.client.patch(url)
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.user.refresh_from_db()
        self.assertNotEqual(self.user.first_name, data['first_name'])

    def test_update_user_data_successfully(self):
        url = reverse('users:user-detail', args=[self.user.username])
        data = {
            'first_name': 'new_first_name_new'
        }

        response = self.client.patch(url, data)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, data['first_name'])

    def test_update_username_with_existing_username(self):
        existing_user = baker.make(get_user_model(), username='test')

        url = reverse('users:user-detail', args=[self.user.username])
        data = {
            'username': existing_user.username
        }

        response = self.client.patch(url, data)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.user.refresh_from_db()
        self.assertNotEqual(self.user.username, existing_user.username)

    def test_update_username_successfully(self):
        url = reverse('users:user-detail', args=[self.user.username])
        data = {
            'username': 'new_username'
        }

        response = self.client.patch(url, data)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, data['username'])
