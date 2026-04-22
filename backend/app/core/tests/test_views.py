from rest_framework.test         import APITestCase
from rest_framework              import status
from django.urls                 import reverse
from django.contrib.auth         import get_user_model
from decimal                     import Decimal
from django.utils                import timezone
from datetime                    import timedelta
import core.tests.fixtures_views as fixtures

User = get_user_model()

class RegisterViewTests(APITestCase):
    def setUp(self):
        self.url = reverse('register')

    def test_register_valid_payload(self):
        payload = fixtures.get_valid_register_payload()

        response = self.client.post(self.url, payload, format = 'json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username = payload['username']).exists())

    def test_register_password_mismatch(self):
        payload = fixtures.get_password_mismatch_register_payload()

        response = self.client.post(self.url, payload, format = 'json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(User.objects.filter(username = payload['username']).exists())

    def test_register_invalid_age(self):
        payload = fixtures.get_invalid_age_register_payload()

        response = self.client.post(self.url, payload, format = 'json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(User.objects.filter(username = payload['username']).exists())

class UserProfileViewTests(APITestCase):
    def setUp(self):
        self.register_url = reverse('register')
        self.url = reverse('user-profile')
        self.client.post(self.register_url, fixtures.get_valid_register_payload(), format = 'json')
        self.user = User.objects.get(username = fixtures.get_valid_register_payload()['username'])

    def test_get_user_profile(self):
        self.client.force_authenticate(user = self.user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user.username, response.data['username'])
        self.assertEqual(self.user.email, response.data['email'])

    def test_unathorized_access(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_patch_user_profile(self):
        self.client.force_authenticate(user = self.user)

        patch_payload = fixtures.get_valid_calorie_overwrite_profile_payload()

        response = self.client.patch(self.url, patch_payload, format = 'json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(patch_payload['target_calories'], Decimal(response.data['target_calories']))

    def test_patch_user_profile_invalid_calories(self):
        self.client.force_authenticate(user = self.user)

        patch_payload = fixtures.get_invalid_calorie_overwrite_profile_payload()

        response = self.client.patch(self.url, patch_payload, format = 'json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_patch_user_profile_immutable_field(self):
        self.client.force_authenticate(user = self.user)

        patch_payload = fixtures.get_immutable_field_overwrite_profile_payload()

        response = self.client.patch(self.url, patch_payload, format = 'json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(patch_payload['username'], response.data['username'])
        self.assertEqual(self.user.username, response.data['username'])
