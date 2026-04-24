from rest_framework.test         import APITestCase
from rest_framework              import status
from django.urls                 import reverse
from django.contrib.auth         import get_user_model
from decimal                     import Decimal
import core.tests.fixtures_views as fixtures
User = get_user_model()

"""
Abstract tests
"""
class ProtectedEndpointTestMixin:
    url = None

    def test_unathorized_access(self):
        self.client.force_authenticate(user = None)

        response = self.client.get(self.url)

        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

        self.client.force_authenticate(user = self.user)

class CreateEndpointTestMixin:
    url = None
    dummy_payload = { 'dummy_field': 'dummy_value' }

    def test_list_endpoint(self):
        self.client.force_authenticate(user = self.user)

        response = self.client.get(self.url)

        self.assertEqual(status.HTTP_405_METHOD_NOT_ALLOWED, response.status_code)

    def test_put_endpoint(self):
        self.client.force_authenticate(user = self.user)

        response = self.client.put(self.url, self.dummy_payload, format = 'json')

        self.assertEqual(status.HTTP_405_METHOD_NOT_ALLOWED, response.status_code)

    def test_patch_endpoint(self):
        self.client.force_authenticate(user = self.user)

        response = self.client.patch(self.url, self.dummy_payload, format = 'json')

        self.assertEqual(status.HTTP_405_METHOD_NOT_ALLOWED, response.status_code)

    def test_delete_endpoint(self):
        self.client.force_authenticate(user = self.user)

        response = self.client.delete(self.url)

        self.assertEqual(status.HTTP_405_METHOD_NOT_ALLOWED, response.status_code)

class ListEndpointTestMixin:
    url = None
    dummy_payload = { 'dummy_field': 'dummy_value' }

    def test_post_endpoint(self):
        self.client.force_authenticate(user = self.user)

        response = self.client.post(self.url, self.dummy_payload, format = 'json')

        self.assertEqual(status.HTTP_405_METHOD_NOT_ALLOWED, response.status_code)

    def test_put_endpoint(self):
        self.client.force_authenticate(user = self.user)

        response = self.client.put(self.url, self.dummy_payload, format = 'json')

        self.assertEqual(status.HTTP_405_METHOD_NOT_ALLOWED, response.status_code)

    def test_patch_endpoint(self):
        self.client.force_authenticate(user = self.user)

        response = self.client.patch(self.url, self.dummy_payload, format = 'json')

        self.assertEqual(status.HTTP_405_METHOD_NOT_ALLOWED, response.status_code)

    def test_delete_endpoint(self):
        self.client.force_authenticate(user = self.user)

        response = self.client.delete(self.url)

        self.assertEqual(status.HTTP_405_METHOD_NOT_ALLOWED, response.status_code)



"""
CustomUser-based view tests
"""
class RegisterViewTests(APITestCase):
    def setUp(self):
        self.url = reverse('register')

    def test_register_valid_payload(self):
        payload = fixtures.get_valid_register_payload()

        response = self.client.post(self.url, payload, format = 'json')

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertTrue(User.objects.filter(username = payload['username']).exists())

    def test_register_password_mismatch(self):
        payload = fixtures.get_password_mismatch_register_payload()

        response = self.client.post(self.url, payload, format = 'json')

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertFalse(User.objects.filter(username = payload['username']).exists())

    def test_register_invalid_age(self):
        payload = fixtures.get_invalid_age_register_payload()

        response = self.client.post(self.url, payload, format = 'json')

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertFalse(User.objects.filter(username = payload['username']).exists())

class UserProfileViewTests(ProtectedEndpointTestMixin, APITestCase):
    def setUp(self):
        self.register_url = reverse('register')
        self.url = reverse('user-profile')
        self.client.post(self.register_url, fixtures.get_valid_register_payload(), format = 'json')
        self.user = User.objects.get(username = fixtures.get_valid_register_payload()['username'])

    def test_get_user_profile(self):
        self.client.force_authenticate(user = self.user)

        response = self.client.get(self.url)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(self.user.username, response.data['username'])
        self.assertEqual(self.user.email, response.data['email'])

    def test_patch_user_profile(self):
        self.client.force_authenticate(user = self.user)

        patch_payload = fixtures.get_valid_calorie_overwrite_profile_payload()

        response = self.client.patch(self.url, patch_payload, format = 'json')
        
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(patch_payload['target_calories'], Decimal(response.data['target_calories']))

    def test_patch_user_profile_invalid_calories(self):
        self.client.force_authenticate(user = self.user)

        patch_payload = fixtures.get_invalid_calorie_overwrite_profile_payload()

        response = self.client.patch(self.url, patch_payload, format = 'json')
        
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_patch_user_profile_immutable_field(self):
        self.client.force_authenticate(user = self.user)

        patch_payload = fixtures.get_immutable_field_overwrite_profile_payload()

        response = self.client.patch(self.url, patch_payload, format = 'json')
        
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertNotEqual(patch_payload['username'], response.data['username'])
        self.assertEqual(self.user.username, response.data['username'])

"""
HealthLog-based view tests
"""
class HealthLogListViewTests(ProtectedEndpointTestMixin, APITestCase):
    def setUp(self):
        self.register_url = reverse('register')
        self.url = reverse('health-log-list')
        self.client.post(self.register_url, fixtures.get_valid_register_payload(), format = 'json')
        self.user = User.objects.get(username = fixtures.get_valid_register_payload()['username'])

    def test_get_health_logs(self):
        self.client.force_authenticate(user = self.user)

        response = self.client.get(self.url)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertIsInstance(response.data, list)

    def test_create_valid_health_log(self):
        self.client.force_authenticate(user = self.user)

        payload = fixtures.get_valid_health_log_payload()

        response = self.client.post(self.url, payload, format = 'json')

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(payload['date'], response.data['date'])

    def test_create_empty_health_log(self):
        self.client.force_authenticate(user = self.user)

        payload = fixtures.get_empty_health_log_payload()

        response = self.client.post(self.url, payload, format = 'json')

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_create_future_date_health_log(self):
        self.client.force_authenticate(user = self.user)

        payload = fixtures.get_future_date_health_log_payload()

        response = self.client.post(self.url, payload, format = 'json')

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_create_duplicate_date_health_log(self):
        self.client.force_authenticate(user = self.user)

        payload = fixtures.get_valid_health_log_payload()

        response1 = self.client.post(self.url, payload, format = 'json')
        self.assertEqual(status.HTTP_201_CREATED, response1.status_code)

        response2 = self.client.post(self.url, payload, format = 'json')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response2.status_code)

    def test_create_invalid_health_log(self):
        self.client.force_authenticate(user = self.user)

        payload = fixtures.get_invalid_health_log_payload()

        response = self.client.post(self.url, payload, format = 'json')

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

class HealthLogDetailViewTests(ProtectedEndpointTestMixin, APITestCase):
    def setUp(self):
        self.register_url = reverse('register')
        self.list_url = reverse('health-log-list')
        self.client.post(self.register_url, fixtures.get_valid_register_payload(), format = 'json')
        self.user = User.objects.get(username = fixtures.get_valid_register_payload()['username'])
        self.client.force_authenticate(user = self.user)
        payload = fixtures.get_valid_health_log_payload()
        response = self.client.post(self.list_url, payload, format = 'json')
        self.health_log_id = response.data['id']
        self.url = reverse('health-log-detail', kwargs = { 'pk': self.health_log_id })

    def test_get_health_log_detail(self):
        response = self.client.get(self.url)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(self.health_log_id, response.data['id'])

    def test_get_health_log_detail_not_found(self):
        invalid_id = 9999
        url = reverse('health-log-detail', kwargs = { 'pk': invalid_id })

        response = self.client.get(url)

        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_patch_health_log_detail(self):
        patch_payload = fixtures.get_valid_health_log_update_payload()

        response = self.client.patch(self.url, patch_payload, format = 'json')

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        for key in patch_payload:
            self.assertEqual(str(patch_payload[key]), str(response.data[key]))

    def test_patch_health_log_detail_invalid_data(self):
        patch_payload = fixtures.get_invalid_health_log_update_payload()

        response = self.client.patch(self.url, patch_payload, format = 'json')

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

class HealthLogByDateViewTests(ProtectedEndpointTestMixin, APITestCase):
    def setUp(self):
        self.register_url = reverse('register')
        self.list_url = reverse('health-log-list')
        self.client.post(self.register_url, fixtures.get_valid_register_payload(), format = 'json')
        self.user = User.objects.get(username = fixtures.get_valid_register_payload()['username'])
        self.client.force_authenticate(user = self.user)
        payload = fixtures.get_valid_health_log_payload()
        self.client.post(self.list_url, payload, format = 'json')
        self.date_str = payload['date']
        self.url = reverse('health-log-by-date', kwargs = { 'date': self.date_str })

    def test_get_health_log_by_date(self):
        response = self.client.get(self.url)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(self.date_str, response.data['date'])

    def test_get_health_log_by_date_not_found(self):
        invalid_date_str = '1900-01-01'
        url = reverse('health-log-by-date', kwargs = { 'date': invalid_date_str })

        response = self.client.get(url)

        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

"""
Food-related view tests
"""
class FoodItemListViewTests(ProtectedEndpointTestMixin, APITestCase):
    def setUp(self):
        self.register_url = reverse('register')
        self.url = reverse('food-item-list')
        self.client.post(self.register_url, fixtures.get_valid_register_payload(), format = 'json')
        self.user = User.objects.get(username = fixtures.get_valid_register_payload()['username'])
    
    def test_get_food_items(self):
        self.client.force_authenticate(user = self.user)

        response = self.client.get(self.url)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertIsInstance(response.data, list)

    def test_create_food_item(self):
        self.client.force_authenticate(user = self.user)

        payload = fixtures.get_valid_food_item_payload()

        response = self.client.post(self.url, payload, format = 'json')

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(response.data['name'], payload['name'])

    def test_create_invalid_food_item(self):
        self.client.force_authenticate(user = self.user)

        payload = fixtures.get_invalid_food_item_payload()

        response = self.client.post(self.url, payload, format = 'json')

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_create_too_high_nutrient_food_item(self):
        self.client.force_authenticate(user = self.user)

        payload = fixtures.get_too_high_nutrient_food_item_payload()

        response = self.client.post(self.url, payload, format = 'json')

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_create_missing_name_food_item(self):
        self.client.force_authenticate(user = self.user)

        payload = fixtures.get_missing_name_food_item_payload()

        response = self.client.post(self.url, payload, format = 'json')

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_create_missing_calorie_food_item(self):
        self.client.force_authenticate(user = self.user)

        payload = fixtures.get_missing_calorie_food_item_payload()

        response = self.client.post(self.url, payload, format = 'json')

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_create_duplicate_name_food_item(self):
        self.client.force_authenticate(user = self.user)

        payload = fixtures.get_valid_food_item_payload()

        response1 = self.client.post(self.url, payload, format = 'json')
        self.assertEqual(status.HTTP_201_CREATED, response1.status_code)

        response2 = self.client.post(self.url, payload, format = 'json')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response2.status_code)

class FoodItemDetailViewTests(ProtectedEndpointTestMixin, APITestCase):
    def setUp(self):
        self.register_url = reverse('register')
        self.list_url = reverse('food-item-list')
        self.client.post(self.register_url, fixtures.get_valid_register_payload(), format = 'json')
        self.user = User.objects.get(username = fixtures.get_valid_register_payload()['username'])
        self.client.force_authenticate(user = self.user)
        payload = fixtures.get_valid_food_item_payload()
        response = self.client.post(self.list_url, payload, format = 'json')
        self.food_item_id = response.data['id']
        self.url = reverse('food-item-detail', kwargs = { 'pk': self.food_item_id })

    def test_get_food_item_detail(self):
        response = self.client.get(self.url)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(self.food_item_id, response.data['id'])

    def test_get_food_item_detail_not_found(self):
        invalid_id = 9999
        url = reverse('food-item-detail', kwargs = { 'pk': invalid_id })

        response = self.client.get(url)

        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
