from rest_framework.test         import APITestCase
from rest_framework              import status
from django.urls                 import reverse
from django.contrib.auth         import get_user_model
from decimal                     import Decimal
from core.models                 import FoodEntry, MuscleGroup, StrengthSet, CardioSet
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
        valid_register_payload = fixtures.get_valid_register_payload()
        self.client.post(self.register_url, valid_register_payload, format = 'json')
        self.user = User.objects.get(username = valid_register_payload['username'])
        self.client.force_authenticate(user = self.user)

        self.url = reverse('user-profile')

    def test_get_user_profile(self):
        response = self.client.get(self.url)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(self.user.username, response.data['username'])
        self.assertEqual(self.user.email, response.data['email'])

    def test_patch_user_profile(self):
        patch_payload = fixtures.get_valid_calorie_overwrite_profile_payload()

        response = self.client.patch(self.url, patch_payload, format = 'json')
        
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(patch_payload['target_calories'], Decimal(response.data['target_calories']))

    def test_patch_user_profile_invalid_calories(self):
        patch_payload = fixtures.get_invalid_calorie_overwrite_profile_payload()

        response = self.client.patch(self.url, patch_payload, format = 'json')
        
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_patch_user_profile_immutable_field(self):
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
        valid_register_payload = fixtures.get_valid_register_payload()
        self.client.post(self.register_url, valid_register_payload, format = 'json')
        self.user = User.objects.get(username = valid_register_payload['username'])
        self.client.force_authenticate(user = self.user)
        
        self.url = reverse('health-log-list')

    def test_get_health_logs(self):
        response = self.client.get(self.url)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertIsInstance(response.data, list)

    def test_create_valid_health_log(self):
        payload = fixtures.get_valid_health_log_payload()

        response = self.client.post(self.url, payload, format = 'json')

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(payload['date'], response.data['date'])

    def test_create_empty_health_log(self):
        payload = fixtures.get_empty_health_log_payload()

        response = self.client.post(self.url, payload, format = 'json')

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_create_future_date_health_log(self):
        payload = fixtures.get_future_date_health_log_payload()

        response = self.client.post(self.url, payload, format = 'json')

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_create_duplicate_date_health_log(self):
        payload = fixtures.get_valid_health_log_payload()

        response1 = self.client.post(self.url, payload, format = 'json')
        self.assertEqual(status.HTTP_201_CREATED, response1.status_code)

        response2 = self.client.post(self.url, payload, format = 'json')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response2.status_code)

    def test_create_invalid_health_log(self):
        payload = fixtures.get_invalid_health_log_payload()

        response = self.client.post(self.url, payload, format = 'json')

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

class HealthLogDetailViewTests(ProtectedEndpointTestMixin, APITestCase):
    def setUp(self):
        self.register_url = reverse('register')
        valid_register_payload = fixtures.get_valid_register_payload()
        self.client.post(self.register_url, valid_register_payload, format = 'json')
        self.user = User.objects.get(username = valid_register_payload['username'])
        self.client.force_authenticate(user = self.user)
        
        self.list_url = reverse('health-log-list')
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
        valid_register_payload = fixtures.get_valid_register_payload()
        self.client.post(self.register_url, valid_register_payload, format = 'json')
        self.user = User.objects.get(username = valid_register_payload['username'])
        self.client.force_authenticate(user = self.user)
        
        self.list_url = reverse('health-log-list')
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
        valid_register_payload = fixtures.get_valid_register_payload()
        self.client.post(self.register_url, valid_register_payload, format = 'json')
        self.user = User.objects.get(username = valid_register_payload['username'])
        self.client.force_authenticate(user = self.user)
        
        self.url = reverse('food-item-list')
    
    def test_get_food_items(self):
        response = self.client.get(self.url)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertIsInstance(response.data, list)

    def test_create_food_item(self):
        payload = fixtures.get_valid_food_item_payload()

        response = self.client.post(self.url, payload, format = 'json')

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(response.data['name'], payload['name'])

    def test_create_invalid_food_item(self):
        payload = fixtures.get_invalid_food_item_payload()

        response = self.client.post(self.url, payload, format = 'json')

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_create_too_high_nutrient_food_item(self):
        payload = fixtures.get_too_high_nutrient_food_item_payload()

        response = self.client.post(self.url, payload, format = 'json')

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_create_missing_name_food_item(self):
        payload = fixtures.get_missing_name_food_item_payload()

        response = self.client.post(self.url, payload, format = 'json')

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_create_missing_calorie_food_item(self):
        payload = fixtures.get_missing_calorie_food_item_payload()

        response = self.client.post(self.url, payload, format = 'json')

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_create_duplicate_name_food_item(self):
        payload = fixtures.get_valid_food_item_payload()

        response1 = self.client.post(self.url, payload, format = 'json')
        self.assertEqual(status.HTTP_201_CREATED, response1.status_code)

        response2 = self.client.post(self.url, payload, format = 'json')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response2.status_code)

class FoodItemDetailViewTests(ProtectedEndpointTestMixin, APITestCase):
    def setUp(self):
        self.register_url = reverse('register')
        valid_register_payload = fixtures.get_valid_register_payload()
        self.client.post(self.register_url, valid_register_payload, format = 'json')
        self.user = User.objects.get(username = valid_register_payload['username'])
        self.client.force_authenticate(user = self.user)

        self.list_url = reverse('food-item-list')
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

class FoodLogListViewTests(ProtectedEndpointTestMixin, APITestCase):
    def setUp(self):
        self.register_url = reverse('register')
        valid_register_payload = fixtures.get_valid_register_payload()
        self.client.post(self.register_url, valid_register_payload, format = 'json')
        self.user = User.objects.get(username = valid_register_payload['username'])
        self.client.force_authenticate(user = self.user)
        
        self.url = reverse('food-log-list')

    def test_get_food_logs(self):
        response = self.client.get(self.url)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertIsInstance(response.data, list)

    def test_create_valid_food_log(self):
        payload = fixtures.get_valid_food_log_payload()

        response = self.client.post(self.url, payload, format = 'json')

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(payload['date'], response.data['date'])

    def test_create_future_date_food_log(self):
        payload = fixtures.get_future_date_food_log_payload()

        response = self.client.post(self.url, payload, format = 'json')

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_create_duplicate_date_food_log(self):
        payload = fixtures.get_valid_food_log_payload()

        response1 = self.client.post(self.url, payload, format = 'json')
        self.assertEqual(status.HTTP_201_CREATED, response1.status_code)

        response2 = self.client.post(self.url, payload, format = 'json')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response2.status_code)

class FoodLogDetailViewTests(ProtectedEndpointTestMixin, APITestCase):
    def setUp(self):
        self.register_url = reverse('register')
        valid_register_payload = fixtures.get_valid_register_payload()
        self.client.post(self.register_url, valid_register_payload, format = 'json')
        self.user = User.objects.get(username = valid_register_payload['username'])
        self.client.force_authenticate(user = self.user)
        
        self.list_url = reverse('food-log-list')
        payload = fixtures.get_valid_food_log_payload()
        response = self.client.post(self.list_url, payload, format = 'json')
        self.food_log_id = response.data['id']
        self.url = reverse('food-log-detail', kwargs = { 'pk': self.food_log_id })

    def test_get_food_log_detail(self):
        response = self.client.get(self.url)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(self.food_log_id, response.data['id'])

    def test_get_food_log_detail_not_found(self):
        invalid_id = 9999
        url = reverse('food-log-detail', kwargs = { 'pk': invalid_id })

        response = self.client.get(url)

        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

class FoodLogByDateViewTests(ProtectedEndpointTestMixin, APITestCase):
    def setUp(self):
        self.register_url = reverse('register')
        valid_register_payload = fixtures.get_valid_register_payload()
        self.client.post(self.register_url, valid_register_payload, format = 'json')
        self.user = User.objects.get(username = valid_register_payload['username'])
        self.client.force_authenticate(user = self.user)
        
        self.list_url = reverse('food-log-list')
        payload = fixtures.get_valid_food_log_payload()
        self.client.post(self.list_url, payload, format = 'json')
        self.date_str = payload['date']
        self.url = reverse('food-log-by-date', kwargs = { 'date': self.date_str })

    def test_get_food_log_by_date(self):
        response = self.client.get(self.url)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(self.date_str, response.data['date'])

    def test_get_food_log_by_date_not_found(self):
        invalid_date_str = '1900-01-01'
        url = reverse('food-log-by-date', kwargs = { 'date': invalid_date_str })

        response = self.client.get(url)

        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

class FoodEntryListViewTests(ProtectedEndpointTestMixin, APITestCase):
    def setUp(self):
        self.register_url = reverse('register')
        valid_register_payload = fixtures.get_valid_register_payload()
        self.client.post(self.register_url, valid_register_payload, format = 'json')
        self.user = User.objects.get(username = valid_register_payload['username'])
        self.client.force_authenticate(user = self.user)

        self.food_item_list_url = reverse('food-item-list')
        food_item_payload = fixtures.get_valid_food_item_payload()
        response = self.client.post(self.food_item_list_url, food_item_payload, format = 'json')
        self.food_item_id = response.data['id']

        self.food_log_list_url = reverse('food-log-list')
        food_log_payload = fixtures.get_valid_food_log_payload()
        response = self.client.post(self.food_log_list_url, food_log_payload, format = 'json')
        self.food_log_id = response.data['id']

        self.url = reverse('food-entry-list', kwargs = { 'log_id': self.food_log_id })
        self.nonexistent_parent_log_url = reverse('food-entry-list', kwargs = { 'log_id': 9999 })
        self.food_log_detail_url = reverse('food-log-detail', kwargs = { 'pk': self.food_log_id })

    def test_get_food_entries(self):
        response = self.client.get(self.url)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertIsInstance(response.data, list)

    def test_create_food_entry(self):
        payload = fixtures.get_food_entry_payload(food_item_id = self.food_item_id)

        response = self.client.post(self.url, payload, format = 'json')

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(payload['meal_type'], response.data['meal_type'])

        parent_log = self.client.get(self.food_log_detail_url).data
        expected_breakfast_macros = fixtures.get_expected_breakfast_macros()
        self.assertEqual(expected_breakfast_macros, parent_log['breakfast_macros'])

    def test_create_invalid_quantity_food_entry(self):
        payload = fixtures.get_invalid_quantity_food_entry_payload(food_item_id = self.food_item_id)

        response = self.client.post(self.url, payload, format = 'json')

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_create_invalid_meal_type_food_entry(self):
        payload = fixtures.get_invalid_meal_type_food_entry_payload(food_item_id = self.food_item_id)

        response = self.client.post(self.url, payload, format = 'json')

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_create_nonexistent_parent_log_food_entry(self):
        payload = fixtures.get_food_entry_payload(food_item_id = self.food_item_id)

        response = self.client.post(self.nonexistent_parent_log_url, payload, format = 'json')

        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_create_no_food_item_food_entry(self):
        payload = fixtures.get_food_entry_payload(food_item_id = None)

        response = self.client.post(self.url, payload, format = 'json')

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

class FoodEntryDetailViewTests(ProtectedEndpointTestMixin, APITestCase):
    def setUp(self):
        self.register_url = reverse('register')
        valid_register_payload = fixtures.get_valid_register_payload()
        self.client.post(self.register_url, valid_register_payload, format = 'json')
        self.user = User.objects.get(username = valid_register_payload['username'])
        self.client.force_authenticate(user = self.user)

        self.food_item_list_url = reverse('food-item-list')
        food_item_payload = fixtures.get_valid_food_item_payload()
        response = self.client.post(self.food_item_list_url, food_item_payload, format = 'json')
        self.food_item_id = response.data['id']

        self.food_log_list_url = reverse('food-log-list')
        food_log_payload = fixtures.get_valid_food_log_payload()
        response = self.client.post(self.food_log_list_url, food_log_payload, format = 'json')
        self.food_log_id = response.data['id']

        food_entry_payload = fixtures.get_food_entry_payload(food_item_id = self.food_item_id)
        food_entry_list_url = reverse('food-entry-list', kwargs = { 'log_id': self.food_log_id })
        response = self.client.post(food_entry_list_url, food_entry_payload, format = 'json')
        self.food_entry_id = response.data['id']

        self.url = reverse('food-entry-detail', kwargs = { 'pk': self.food_entry_id })

    def test_get_food_entry_detail(self):
        response = self.client.get(self.url)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(self.food_entry_id, response.data['id'])

    def test_get_food_entry_detail_not_found(self):
        invalid_id = 9999
        url = reverse('food-entry-detail', kwargs = { 'pk': invalid_id })

        response = self.client.get(url)

        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_patch_food_entry_detail(self):
        patch_payload = fixtures.get_valid_food_entry_update_payload()

        response = self.client.patch(self.url, patch_payload, format = 'json')

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        for key in patch_payload:
            self.assertEqual(str(patch_payload[key]), str(response.data[key]))

    def test_patch_invalid_food_entry_detail(self):
        patch_payload = fixtures.get_invalid_food_entry_update_payload()

        response = self.client.patch(self.url, patch_payload, format = 'json')

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_delete_food_entry(self):
        response = self.client.delete(self.url)

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertFalse(FoodEntry.objects.filter(id = self.food_entry_id).exists())

"""
Strength-related view tests
"""
class MuscleGroupListViewTests(ProtectedEndpointTestMixin, APITestCase):
    def setUp(self):
        self.register_url = reverse('register')
        valid_register_payload = fixtures.get_valid_register_payload()
        self.client.post(self.register_url, valid_register_payload, format = 'json')
        self.user = User.objects.get(username = valid_register_payload['username'])
        self.client.force_authenticate(user = self.user)
        
        self.url = reverse('muscle-group-list')

    def test_get_muscle_groups(self):
        response = self.client.get(self.url)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertIsInstance(response.data, list)

class StrengthExerciseListViewTests(ProtectedEndpointTestMixin, APITestCase):
    def setUp(self):
        self.register_url = reverse('register')
        valid_register_payload = fixtures.get_valid_register_payload()
        self.client.post(self.register_url, valid_register_payload, format = 'json')
        self.user = User.objects.get(username = valid_register_payload['username'])
        self.client.force_authenticate(user = self.user)
        
        muscle_group_1_payload = fixtures.get_muscle_group_data(name = 'Muscle Group 1')
        muscle_group_2_payload = fixtures.get_muscle_group_data(name = 'Muscle Group 2')
        self.muscle_group_1 = MuscleGroup.objects.create(**muscle_group_1_payload)
        self.muscle_group_2 = MuscleGroup.objects.create(**muscle_group_2_payload)

        self.url = reverse('strength-exercise-list')

    def test_get_strength_exercises(self):
        response = self.client.get(self.url)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertIsInstance(response.data, list)

    def test_create_strength_exercise(self):
        payload = fixtures.get_valid_strength_exercise_payload(target_muscle_group_ids = [self.muscle_group_1.id, self.muscle_group_2.id])

        response = self.client.post(self.url, payload, format = 'json')

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(payload['name'], response.data['name'])
        for target_muscle_group in response.data['target_muscle_groups']:
            self.assertIn(target_muscle_group['id'], payload['target_muscle_group_ids'])

    def test_create_invalid_strength_exercise(self):
        payload = fixtures.get_invalid_strength_exercise_payload()

        response = self.client.post(self.url, payload, format = 'json')

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_create_strength_exercise_with_nonexistent_muscle_group(self):
        nonexistent_muscle_group_id = 9999
        payload = fixtures.get_valid_strength_exercise_payload(target_muscle_group_ids = [nonexistent_muscle_group_id])

        response = self.client.post(self.url, payload, format = 'json')

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_create_duplicate_strength_exercise(self):
        payload = fixtures.get_valid_strength_exercise_payload(target_muscle_group_ids = [self.muscle_group_1.id])

        response1 = self.client.post(self.url, payload, format = 'json')
        self.assertEqual(status.HTTP_201_CREATED, response1.status_code)

        response2 = self.client.post(self.url, payload, format = 'json')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response2.status_code)

class StrengthExerciseDetailViewTests(ProtectedEndpointTestMixin, APITestCase):
    def setUp(self):
        self.register_url = reverse('register')
        valid_register_payload = fixtures.get_valid_register_payload()
        self.client.post(self.register_url, valid_register_payload, format = 'json')
        self.user = User.objects.get(username = valid_register_payload['username'])
        self.client.force_authenticate(user = self.user)
        
        muscle_group_data = fixtures.get_muscle_group_data(name = 'Muscle Group 1')
        muscle_group = MuscleGroup.objects.create(**muscle_group_data)

        strength_exercise_payload = fixtures.get_valid_strength_exercise_payload(target_muscle_group_ids = [muscle_group.id])
        response = self.client.post(reverse('strength-exercise-list'), strength_exercise_payload, format = 'json')
        self.strength_exercise_id = response.data['id']

        self.url = reverse('strength-exercise-detail', kwargs = { 'pk': self.strength_exercise_id })

    def test_get_strength_exercise_detail(self):
        response = self.client.get(self.url)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(self.strength_exercise_id, response.data['id'])

    def test_get_strength_exercise_detail_not_found(self):
        invalid_id = 9999
        url = reverse('strength-exercise-detail', kwargs = { 'pk': invalid_id })

        response = self.client.get(url)

        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

class StrengthTrainingListViewTests(ProtectedEndpointTestMixin, APITestCase):
    def setUp(self):
        self.register_url = reverse('register')
        valid_register_payload = fixtures.get_valid_register_payload()
        self.client.post(self.register_url, valid_register_payload, format = 'json')
        self.user = User.objects.get(username = valid_register_payload['username'])
        self.client.force_authenticate(user = self.user)
        
        self.url = reverse('strength-training-list')

    def test_get_strength_trainings(self):
        response = self.client.get(self.url)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertIsInstance(response.data, list)

    def test_create_strength_training(self):
        payload = fixtures.get_valid_strength_training_payload()

        response = self.client.post(self.url, payload, format = 'json')

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(payload['date'], response.data['date'])

    def test_create_future_date_strength_training(self):
        payload = fixtures.get_future_date_strength_training_payload()

        response = self.client.post(self.url, payload, format = 'json')

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_create_duplicate_date_strength_training(self):
        payload = fixtures.get_valid_strength_training_payload()

        response1 = self.client.post(self.url, payload, format = 'json')
        self.assertEqual(status.HTTP_201_CREATED, response1.status_code)

        response2 = self.client.post(self.url, payload, format = 'json')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response2.status_code)

class StrengthTrainingDetailViewTests(ProtectedEndpointTestMixin, APITestCase):
    def setUp(self):
        self.register_url = reverse('register')
        valid_register_payload = fixtures.get_valid_register_payload()
        self.client.post(self.register_url, valid_register_payload, format = 'json')
        self.user = User.objects.get(username = valid_register_payload['username'])
        self.client.force_authenticate(user = self.user)
        
        self.list_url = reverse('strength-training-list')
        payload = fixtures.get_valid_strength_training_payload()
        response = self.client.post(self.list_url, payload, format = 'json')
        self.strength_training_id = response.data['id']
        self.url = reverse('strength-training-detail', kwargs = { 'pk': self.strength_training_id })

    def test_get_strength_training_detail(self):
        response = self.client.get(self.url)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(self.strength_training_id, response.data['id'])

    def test_get_strength_training_detail_not_found(self):
        invalid_id = 9999
        url = reverse('strength-training-detail', kwargs = { 'pk': invalid_id })

        response = self.client.get(url)

        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

class StrengthTrainingByDateViewTests(ProtectedEndpointTestMixin, APITestCase):
    def setUp(self):
        self.register_url = reverse('register')
        valid_register_payload = fixtures.get_valid_register_payload()
        self.client.post(self.register_url, valid_register_payload, format = 'json')
        self.user = User.objects.get(username = valid_register_payload['username'])
        self.client.force_authenticate(user = self.user)
        
        self.list_url = reverse('strength-training-list')
        payload = fixtures.get_valid_strength_training_payload()
        self.client.post(self.list_url, payload, format = 'json')
        self.date_str = payload['date']
        self.url = reverse('strength-training-by-date', kwargs = { 'date': self.date_str })

    def test_get_strength_training_by_date(self):
        response = self.client.get(self.url)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(self.date_str, response.data['date'])

    def test_get_strength_training_by_date_not_found(self):
        invalid_date_str = '1900-01-01'
        url = reverse('strength-training-by-date', kwargs = { 'date': invalid_date_str })

        response = self.client.get(url)

        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

class StrengthSetListViewTests(ProtectedEndpointTestMixin, APITestCase):
    def setUp(self):
        self.register_url = reverse('register')
        valid_register_payload = fixtures.get_valid_register_payload()
        self.client.post(self.register_url, valid_register_payload, format = 'json')
        self.user = User.objects.get(username = valid_register_payload['username'])
        self.client.force_authenticate(user = self.user)

        strength_training_payload = fixtures.get_valid_strength_training_payload()
        response = self.client.post(reverse('strength-training-list'), strength_training_payload, format = 'json')
        self.strength_training_id = response.data['id']

        strength_exercise_payload = fixtures.get_valid_strength_exercise_payload(target_muscle_group_ids = [])
        response = self.client.post(reverse('strength-exercise-list'), strength_exercise_payload, format = 'json')
        self.strength_exercise = response.data
        self.strength_exercise_id = response.data['id']

        self.url = reverse('strength-set-list', kwargs = { 'log_id': self.strength_training_id })
        self.nonexistent_parent_training_url = reverse('strength-set-list', kwargs = { 'log_id': 9999 })

    def test_get_strength_sets(self):
        response = self.client.get(self.url)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertIsInstance(response.data, list)

    def test_create_strength_set(self):
        payload = fixtures.get_valid_strength_set_payload(exercise_id = self.strength_exercise_id)

        response = self.client.post(self.url, payload, format = 'json')
        
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(self.strength_exercise, response.data['exercise'])

    def test_create_invalid_strength_set(self):
        payload = fixtures.get_invalid_strength_set_payload()

        response = self.client.post(self.url, payload, format = 'json')

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_create_nonexistent_exercise_strength_set(self):
        payload = fixtures.get_valid_strength_set_payload(exercise_id = None)

        response = self.client.post(self.nonexistent_parent_training_url, payload, format = 'json')

        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

class StrengthSetDetailViewTests(ProtectedEndpointTestMixin, APITestCase):
    def setUp(self):
        self.register_url = reverse('register')
        valid_register_payload = fixtures.get_valid_register_payload()
        self.client.post(self.register_url, valid_register_payload, format = 'json')
        self.user = User.objects.get(username = valid_register_payload['username'])
        self.client.force_authenticate(user = self.user)

        strength_training_payload = fixtures.get_valid_strength_training_payload()
        response = self.client.post(reverse('strength-training-list'), strength_training_payload, format = 'json')
        self.strength_training_id = response.data['id']

        strength_exercise_payload = fixtures.get_valid_strength_exercise_payload(target_muscle_group_ids = [])
        response = self.client.post(reverse('strength-exercise-list'), strength_exercise_payload, format = 'json')
        self.strength_exercise_id = response.data['id']

        strength_set_payload = fixtures.get_valid_strength_set_payload(exercise_id = self.strength_exercise_id)
        strength_set_list_url = reverse('strength-set-list', kwargs = { 'log_id': self.strength_training_id })
        response = self.client.post(strength_set_list_url, strength_set_payload, format = 'json')
        self.strength_set_id = response.data['id']

        self.url = reverse('strength-set-detail', kwargs = { 'pk': self.strength_set_id })

    def test_get_strength_set_detail(self):
        response = self.client.get(self.url)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(self.strength_set_id, response.data['id'])
    
    def test_get_strength_set_detail_not_found(self):
        invalid_id = 9999
        url = reverse('strength-set-detail', kwargs = { 'pk': invalid_id })

        response = self.client.get(url)

        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_patch_strength_set_detail(self):
        patch_payload = fixtures.get_valid_strength_set_update_payload()

        response = self.client.patch(self.url, patch_payload, format = 'json')

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        for key in patch_payload:
            self.assertEqual(str(patch_payload[key]), str(response.data[key]))

    def test_patch_invalid_strength_set_detail(self):
        patch_payload = fixtures.get_invalid_strength_set_update_payload()

        response = self.client.patch(self.url, patch_payload, format = 'json')

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_delete_strength_set(self):
        response = self.client.delete(self.url)

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertFalse(StrengthSet.objects.filter(id = self.strength_set_id).exists())

"""
Cardio-related view tests
"""
class CardioExerciseListViewTests(ProtectedEndpointTestMixin, APITestCase):
    def setUp(self):
        self.register_url = reverse('register')
        valid_register_payload = fixtures.get_valid_register_payload()
        self.client.post(self.register_url, valid_register_payload, format = 'json')
        self.user = User.objects.get(username = valid_register_payload['username'])
        self.client.force_authenticate(user = self.user)
        
        self.url = reverse('cardio-exercise-list')

    def test_get_cardio_exercises(self):
        response = self.client.get(self.url)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertIsInstance(response.data, list)

    def test_create_cardio_exercise(self):
        payload = fixtures.get_valid_cardio_exercise_payload()

        response = self.client.post(self.url, payload, format = 'json')

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(payload['name'], response.data['name'])

    def test_create_invalid_cardio_exercise(self):
        payload = fixtures.get_invalid_cardio_exercise_payload()

        response = self.client.post(self.url, payload, format = 'json')

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_create_duplicate_cardio_exercise(self):
        payload = fixtures.get_valid_cardio_exercise_payload()

        response1 = self.client.post(self.url, payload, format = 'json')
        self.assertEqual(status.HTTP_201_CREATED, response1.status_code)

        response2 = self.client.post(self.url, payload, format = 'json')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response2.status_code)

class CardioExerciseDetailViewTests(ProtectedEndpointTestMixin, APITestCase):
    def setUp(self):
        self.register_url = reverse('register')
        valid_register_payload = fixtures.get_valid_register_payload()
        self.client.post(self.register_url, valid_register_payload, format = 'json')
        self.user = User.objects.get(username = valid_register_payload['username'])
        self.client.force_authenticate(user = self.user)

        cardio_exercise_payload = fixtures.get_valid_cardio_exercise_payload()
        response = self.client.post(reverse('cardio-exercise-list'), cardio_exercise_payload, format = 'json')
        self.cardio_exercise_id = response.data['id']

        self.url = reverse('cardio-exercise-detail', kwargs = { 'pk': self.cardio_exercise_id })

    def test_get_cardio_exercise_detail(self):
        response = self.client.get(self.url)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(self.cardio_exercise_id, response.data['id'])

    def test_get_cardio_exercise_detail_not_found(self):
        invalid_id = 9999
        url = reverse('cardio-exercise-detail', kwargs = { 'pk': invalid_id })

        response = self.client.get(url)

        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

class CardioTrainingListViewTests(ProtectedEndpointTestMixin, APITestCase):
    def setUp(self):
        self.register_url = reverse('register')
        valid_register_payload = fixtures.get_valid_register_payload()
        self.client.post(self.register_url, valid_register_payload, format = 'json')
        self.user = User.objects.get(username = valid_register_payload['username'])
        self.client.force_authenticate(user = self.user)
        
        self.url = reverse('cardio-training-list')

    def test_get_cardio_trainings(self):
        response = self.client.get(self.url)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertIsInstance(response.data, list)

    def test_create_cardio_training(self):
        payload = fixtures.get_valid_cardio_training_payload()

        response = self.client.post(self.url, payload, format = 'json')

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(payload['date'], response.data['date'])

    def test_create_future_date_cardio_training(self):
        payload = fixtures.get_future_date_cardio_training_payload()

        response = self.client.post(self.url, payload, format = 'json')

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
    
    def test_create_duplicate_date_cardio_training(self):
        payload = fixtures.get_valid_cardio_training_payload()

        response1 = self.client.post(self.url, payload, format = 'json')
        self.assertEqual(status.HTTP_201_CREATED, response1.status_code)

        response2 = self.client.post(self.url, payload, format = 'json')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response2.status_code)

class CardioTrainingDetailViewTests(ProtectedEndpointTestMixin, APITestCase):
    def setUp(self):
        self.register_url = reverse('register')
        valid_register_payload = fixtures.get_valid_register_payload()
        self.client.post(self.register_url, valid_register_payload, format = 'json')
        self.user = User.objects.get(username = valid_register_payload['username'])
        self.client.force_authenticate(user = self.user)
        
        self.list_url = reverse('cardio-training-list')
        payload = fixtures.get_valid_cardio_training_payload()
        response = self.client.post(self.list_url, payload, format = 'json')
        self.cardio_training_id = response.data['id']
        self.url = reverse('cardio-training-detail', kwargs = { 'pk': self.cardio_training_id })

    def test_get_cardio_training_detail(self):
        response = self.client.get(self.url)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(self.cardio_training_id, response.data['id'])

    def test_get_cardio_training_detail_not_found(self):
        invalid_id = 9999
        url = reverse('cardio-training-detail', kwargs = { 'pk': invalid_id })

        response = self.client.get(url)

        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

class CardioTrainingByDateViewTests(ProtectedEndpointTestMixin, APITestCase):
    def setUp(self):
        self.register_url = reverse('register')
        valid_register_payload = fixtures.get_valid_register_payload()
        self.client.post(self.register_url, valid_register_payload, format = 'json')
        self.user = User.objects.get(username = valid_register_payload['username'])
        self.client.force_authenticate(user = self.user)
        
        self.list_url = reverse('cardio-training-list')
        payload = fixtures.get_valid_cardio_training_payload()
        self.client.post(self.list_url, payload, format = 'json')
        self.date_str = payload['date']
        self.url = reverse('cardio-training-by-date', kwargs = { 'date': self.date_str })

    def test_get_cardio_training_by_date(self):
        response = self.client.get(self.url)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(self.date_str, response.data['date'])

    def test_get_cardio_training_by_date_not_found(self):
        invalid_date_str = '1900-01-01'
        url = reverse('cardio-training-by-date', kwargs = { 'date': invalid_date_str })

        response = self.client.get(url)

        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

class CardioSetListViewTests(ProtectedEndpointTestMixin, APITestCase):
    def setUp(self):
        self.register_url = reverse('register')
        valid_register_payload = fixtures.get_valid_register_payload()
        self.client.post(self.register_url, valid_register_payload, format = 'json')
        self.user = User.objects.get(username = valid_register_payload['username'])
        self.client.force_authenticate(user = self.user)

        cardio_training_payload = fixtures.get_valid_cardio_training_payload()
        response = self.client.post(reverse('cardio-training-list'), cardio_training_payload, format = 'json')
        self.cardio_training_id = response.data['id']

        cardio_exercise_payload = fixtures.get_valid_cardio_exercise_payload()
        response = self.client.post(reverse('cardio-exercise-list'), cardio_exercise_payload, format = 'json')
        self.cardio_exercise_id = response.data['id']

        self.url = reverse('cardio-set-list', kwargs = { 'log_id': self.cardio_training_id })
        self.nonexistent_parent_training_url = reverse('cardio-set-list', kwargs = { 'log_id': 9999 })

    def test_get_cardio_sets(self):
        response = self.client.get(self.url)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertIsInstance(response.data, list)

    def test_create_cardio_set(self):
        payload = fixtures.get_valid_cardio_set_payload(exercise_id = self.cardio_exercise_id)

        response = self.client.post(self.url, payload, format = 'json')
        
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(self.cardio_exercise_id, response.data['exercise']['id'])

    def test_create_invalid_cardio_set(self):
        payload = fixtures.get_invalid_cardio_set_payload()

        response = self.client.post(self.url, payload, format = 'json')

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_create_nonexistent_exercise_cardio_set(self):
        payload = fixtures.get_valid_cardio_set_payload(exercise_id = None)

        response = self.client.post(self.nonexistent_parent_training_url, payload, format = 'json')

        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

class CardioSetDetailViewTests(ProtectedEndpointTestMixin, APITestCase):
    def setUp(self):
        self.register_url = reverse('register')
        valid_register_payload = fixtures.get_valid_register_payload()
        self.client.post(self.register_url, valid_register_payload, format = 'json')
        self.user = User.objects.get(username = valid_register_payload['username'])
        self.client.force_authenticate(user = self.user)

        cardio_training_payload = fixtures.get_valid_cardio_training_payload()
        response = self.client.post(reverse('cardio-training-list'), cardio_training_payload, format = 'json')
        self.cardio_training_id = response.data['id']

        cardio_exercise_payload = fixtures.get_valid_cardio_exercise_payload()
        response = self.client.post(reverse('cardio-exercise-list'), cardio_exercise_payload, format = 'json')
        self.cardio_exercise_id = response.data['id']

        cardio_set_payload = fixtures.get_valid_cardio_set_payload(exercise_id = self.cardio_exercise_id)
        cardio_set_list_url = reverse('cardio-set-list', kwargs = { 'log_id': self.cardio_training_id })
        response = self.client.post(cardio_set_list_url, cardio_set_payload, format = 'json')
        self.cardio_set_id = response.data['id']

        self.url = reverse('cardio-set-detail', kwargs = { 'pk': self.cardio_set_id })

    def test_get_cardio_set_detail(self):
        response = self.client.get(self.url)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(self.cardio_set_id, response.data['id'])

    def test_get_cardio_set_detail_not_found(self):
        invalid_id = 9999
        url = reverse('cardio-set-detail', kwargs = { 'pk': invalid_id })

        response = self.client.get(url)

        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_patch_cardio_set_detail(self):
        patch_payload = fixtures.get_valid_cardio_set_update_payload()

        response = self.client.patch(self.url, patch_payload, format = 'json')

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        for key in patch_payload:
            self.assertEqual(str(patch_payload[key]), str(response.data[key]))

    def test_patch_invalid_cardio_set_detail(self):
        patch_payload = fixtures.get_invalid_cardio_set_update_payload()

        response = self.client.patch(self.url, patch_payload, format = 'json')

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_delete_cardio_set(self):
        response = self.client.delete(self.url)

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertFalse(CardioSet.objects.filter(id = self.cardio_set_id).exists())
