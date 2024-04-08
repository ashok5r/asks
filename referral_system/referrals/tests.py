from django.test import TestCase
from django.contrib.auth.models import User
from django.test import TestCase, Client
from rest_framework import status
from .models import UserProfile

# Create your tests here.
class UserRegistrationTestCase(TestCase):
    def test_user_registration(self):
        client = Client()
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpassword',
            'name': 'Test User',
            'referral_code': 'ABC123'
        }
        response = client.post('/api/register/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue('user_id' in response.data)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'testuser')

class UserDetailsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        self.client = Client()
        self.client.force_login(self.user)

    def test_user_details(self):
        response = self.client.get('/api/user/details/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testuser')

class ReferralsTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='testuser1', email='test1@example.com', password='testpassword1')
        self.user2 = User.objects.create_user(username='testuser2', email='test2@example.com', password='testpassword2')
        self.user3 = User.objects.create_user(username='testuser3', email='test3@example.com', password='testpassword3')
        self.user_profile1 = UserProfile.objects.create(user=self.user1, name='Test User 1', referral_code='ABC123')
        self.user_profile2 = UserProfile.objects.create(user=self.user2, name='Test User 2', referral_code='ABC123')
        self.client = Client()
        self.client.force_login(self.user1)

    def test_referrals(self):
        response = self.client.get('/api/referrals/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)