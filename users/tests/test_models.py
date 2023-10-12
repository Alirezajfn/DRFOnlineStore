from django.contrib.auth import get_user_model
from django.test import TestCase


class UserManagerTests(TestCase):

    def test_create_user(self):
        user = get_user_model().objects.create_user(
            username="username",
            email="test@test.com",
            password="password"
        )
        self.assertEquals(user.username, "username")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_user_with_empty_username_fails(self):
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                username="",
                email="test@test.com",
                password="password"
            )

    def test_create_staff_user(self):
        staff_user = get_user_model().objects.create_staff_user(
            username="username",
            email="test@test.com",
            password="password"
        )
        self.assertEquals(staff_user.username, "username")
        self.assertTrue(staff_user.is_active)
        self.assertTrue(staff_user.is_staff)
        self.assertFalse(staff_user.is_superuser)

    def test_create_superuser(self):
        superuser = get_user_model().objects.create_superuser(
            username="username",
            email="test@test.com",
            password="password"
        )
        self.assertEquals(superuser.username, "username")
        self.assertTrue(superuser.is_active)
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)
