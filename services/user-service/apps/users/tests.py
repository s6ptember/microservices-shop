from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import UserProfile
import json

User = get_user_model()


class UserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            first_name='John',
            last_name='Doe',
            password='testpass123'
        )

    def test_user_creation(self):
        """Test user creation with email as username field"""
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertEqual(self.user.username, 'testuser')
        self.assertTrue(self.user.check_password('testpass123'))
        self.assertTrue(self.user.is_active)
        self.assertFalse(self.user.is_staff)

    def test_user_string_representation(self):
        """Test user string representation"""
        self.assertEqual(str(self.user), 'testuser')


class UserProfileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            first_name='John',
            last_name='Doe',
            password='testpass123'
        )
        self.profile = UserProfile.objects.create(
            user=self.user,
            phone='+1234567890',
            address='123 Test St',
            date_of_birth='1990-01-01'
        )

    def test_profile_creation(self):
        """Test user profile creation"""
        self.assertEqual(self.profile.user, self.user)
        self.assertEqual(self.profile.phone, '+1234567890')
        self.assertEqual(self.profile.address, '123 Test St')
        self.assertEqual(str(self.profile.date_of_birth), '1990-01-01')

    def test_profile_string_representation(self):
        """Test profile string representation"""
        expected = f"Profile of {self.user.email}"
        self.assertEqual(str(self.profile), expected)


class UserRegistrationTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.registration_url = reverse('register')

    def test_user_registration_success(self):
        """Test successful user registration"""
        data = {
            'email': 'newuser@example.com',
            'username': 'newuser',
            'first_name': 'Jane',
            'last_name': 'Smith',
            'password': 'strongpass123',
            'password_confirm': 'strongpass123'
        }
        response = self.client.post(self.registration_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)

        user = User.objects.get(email='newuser@example.com')
        self.assertEqual(user.username, 'newuser')
        self.assertTrue(hasattr(user, 'profile'))

    def test_user_registration_password_mismatch(self):
        """Test registration with password mismatch"""
        data = {
            'email': 'test@example.com',
            'username': 'testuser',
            'first_name': 'John',
            'last_name': 'Doe',
            'password': 'password123',
            'password_confirm': 'different123'
        }
        response = self.client.post(self.registration_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)

    def test_user_registration_duplicate_email(self):
        """Test registration with duplicate email"""
        User.objects.create_user(
            email='existing@example.com',
            username='existing',
            password='pass123'
        )

        data = {
            'email': 'existing@example.com',
            'username': 'newuser',
            'first_name': 'John',
            'last_name': 'Doe',
            'password': 'password123',
            'password_confirm': 'password123'
        }
        response = self.client.post(self.registration_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserAuthenticationTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.login_url = reverse('login')
        self.user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpass123'
        )

    def test_login_success(self):
        """Test successful login"""
        data = {
            'email': 'test@example.com',
            'password': 'testpass123'
        }
        response = self.client.post(self.login_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertIn('user', response.data)

    def test_login_invalid_credentials(self):
        """Test login with invalid credentials"""
        data = {
            'email': 'test@example.com',
            'password': 'wrongpass'
        }
        response = self.client.post(self.login_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UserProfileTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpass123'
        )
        self.profile = UserProfile.objects.create(user=self.user)
        self.profile_url = reverse('profile')
        self.profile_update_url = reverse('profile-update')

    def test_get_profile_authenticated(self):
        """Test getting user profile when authenticated"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.profile_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.user.id)

    def test_get_profile_unauthenticated(self):
        """Test getting profile without authentication"""
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_profile(self):
        """Test updating user profile"""
        self.client.force_authenticate(user=self.user)
        data = {
            'phone': '+1234567890',
            'address': '123 New St',
            'date_of_birth': '1990-05-15'
        }
        response = self.client.put(self.profile_update_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.phone, '+1234567890')