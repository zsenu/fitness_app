from   datetime                        import date
from   decimal                         import Decimal
from   django.test                     import TestCase
from   core.serializers                import UserSerializer, RegisterSerializer
from   core.serializers                import HealthLogSerializer
from   core.serializers                import FoodItemSerializer, FoodLogSerializer, FoodEntrySerializer
from   core.serializers                import MuscleGroupSerializer, StrengthExerciseSerializer, StrengthTrainingSerializer, StrengthSetSerializer
from   core.serializers                import CardioExerciseSerializer, CardioTrainingSerializer, CardioSetSerializer
import core.tests.fixtures_serializers as fixtures

"""
CustomUser-related serializer tests
"""
def create_custom_user(data):
    serializer = RegisterSerializer(data = data)
    if serializer.is_valid():
        return serializer.save()
    else:
        raise ValueError('Invalid data for creating CustomUser: {}'.format(serializer.errors))

class CustomUserSerializerTests(TestCase):
    def test_valid_registration_serializer(self):
        data = fixtures.get_valid_custom_user_data()
        serializer = RegisterSerializer(data = data)

        self.assertTrue(serializer.is_valid())
        self.assertEqual(data['username'],        serializer.validated_data['username'])
        self.assertEqual(data['email'],           serializer.validated_data['email'])
        self.assertEqual(data['gender'],          serializer.validated_data['gender'])
        self.assertEqual(data['birth_date'],      serializer.validated_data['birth_date'])
        self.assertEqual(data['height'],          serializer.validated_data['height'])
        self.assertEqual(data['starting_weight'], serializer.validated_data['starting_weight'])
        self.assertEqual(data['target_weight'],   serializer.validated_data['target_weight'])
        self.assertEqual(data['target_date'],     serializer.validated_data['target_date'])
        self.assertEqual(data['target_calories'], serializer.validated_data['target_calories'])
    
    def test_mismatched_password_registration_serializer(self):
        data = fixtures.get_mismatched_password_custom_user_data()
        serializer = RegisterSerializer(data = data)

        self.assertFalse(serializer.is_valid())
        self.assertIn('password', serializer.errors)

    def test_invalid_registration_serializer(self):
        data = fixtures.get_invalid_custom_user_data()
        serializer = RegisterSerializer(data = data)

        self.assertFalse(serializer.is_valid())
        self.assertIn('gender',          serializer.errors)
        self.assertIn('birth_date',      serializer.errors)
        self.assertIn('height',          serializer.errors)
        self.assertIn('starting_weight', serializer.errors)
        self.assertIn('activity_level',  serializer.errors)
        self.assertIn('target_weight',   serializer.errors)
        self.assertIn('target_date',     serializer.errors)
        self.assertIn('target_calories', serializer.errors)

    def test_valid_user_serializer(self):
        data = fixtures.get_valid_custom_user_data()
        user = create_custom_user(data)
        serializer = UserSerializer(user)

        self.assertEqual(data['username'],        serializer.data['username'])
        self.assertEqual(data['email'],           serializer.data['email'])
        self.assertEqual(data['gender'],          serializer.data['gender'])
        self.assertEqual(data['birth_date'],      date.fromisoformat(serializer.data['birth_date']))
        self.assertEqual(data['height'],          serializer.data['height'])
        self.assertEqual(data['starting_weight'], Decimal(serializer.data['starting_weight']))
        self.assertEqual(data['starting_weight'], Decimal(serializer.data['current_weight']))
        self.assertEqual(data['activity_level'],  serializer.data['activity_level'])
        self.assertEqual(data['target_weight'],   Decimal(serializer.data['target_weight']))
        self.assertEqual(data['target_date'],     date.fromisoformat(serializer.data['target_date']))
        self.assertEqual(data['target_calories'], Decimal(serializer.data['target_calories']))
        self.assertEqual(Decimal('2190.00'),      Decimal(serializer.data['bmr']))
        self.assertEqual(Decimal('2628.00'),      Decimal(serializer.data['tdee']))

"""
HealthLog-related serializer tests
"""
class HealthLogSerializerTests(TestCase):
    def _get_serializer_with_user(self, data):
        correct_custom_user = create_custom_user(fixtures.get_valid_custom_user_data())
        request_with_user   = type('Request', (object,), { 'user': correct_custom_user })
        return HealthLogSerializer(
            data = data,
            context = { 'request': request_with_user }
        )
    
    def test_valid_health_log_serializer(self):
        data = fixtures.get_valid_health_log_data()
        serializer = self._get_serializer_with_user(data)

        self.assertTrue(serializer.is_valid())
        self.assertEqual(data['date'],            serializer.validated_data['date'])
        self.assertEqual(data['bodyweight'],      Decimal(serializer.validated_data['bodyweight']))
        self.assertEqual(data['hours_slept'],     Decimal(serializer.validated_data['hours_slept']))
        self.assertEqual(data['liquid_consumed'], Decimal(serializer.validated_data['liquid_consumed']))

    def test_empty_health_log_serializer(self):
        data = fixtures.get_empty_health_log_data()
        serializer = self._get_serializer_with_user(data)

        self.assertFalse(serializer.is_valid())
        self.assertIn('health_log', serializer.errors)

    def test_invalid_health_log_serializer(self):
        data = fixtures.get_invalid_health_log_data()
        serializer = self._get_serializer_with_user(data)

        self.assertFalse(serializer.is_valid())
        self.assertIn('bodyweight',      serializer.errors)
        self.assertIn('hours_slept',     serializer.errors)
        self.assertIn('liquid_consumed', serializer.errors)

"""
Food-related serializer tests
"""
def create_food_item(data):
    serializer = FoodItemSerializer(data = data)
    if serializer.is_valid():
        return serializer.save()
    else:
        raise ValueError('Invalid data for creating FoodItem: {}'.format(serializer.errors))

class FoodItemSerializerTests(TestCase):
    def test_valid_food_item_serializer(self):
        data = fixtures.get_valid_food_item_data()
        serializer = FoodItemSerializer(data = data)

        self.assertTrue(serializer.is_valid())
        self.assertEqual(data['name'],        serializer.validated_data['name'])
        self.assertEqual(data['description'], serializer.validated_data['description'])
        self.assertEqual(data['calories'],    Decimal(serializer.validated_data['calories']))

    def test_too_low_nutrients_food_item_serializer(self):
        data = fixtures.get_invalid_food_item_data()
        serializer = FoodItemSerializer(data = data)

        self.assertFalse(serializer.is_valid())
        self.assertIn('calories', serializer.errors)

    def test_empty_food_item_serializer(self):
        data = fixtures.get_empty_food_item_data()
        serializer = FoodItemSerializer(data = data)

        self.assertTrue(serializer.is_valid())

    def test_too_high_total_nutrients_food_item_serializer(self):
        data = fixtures.get_too_high_total_nutrients_food_item_data()
        serializer = FoodItemSerializer(data = data)

        self.assertFalse(serializer.is_valid())
        self.assertIn('food_item', serializer.errors)

def create_food_log(data):
    correct_custom_user = create_custom_user(fixtures.get_valid_custom_user_data())
    request_with_user   = type('Request', (object,), { 'user': correct_custom_user })

    serializer = FoodLogSerializer(
            data = data,
            context = { 'request': request_with_user }
        )
    if serializer.is_valid():
        return serializer.save()
    else:
        raise ValueError('Invalid data for creating FoodLog: {}'.format(serializer.errors))

class FoodLogSerializerTests(TestCase):
    def _get_serializer_with_user(self, data):
        correct_custom_user = create_custom_user(fixtures.get_valid_custom_user_data())
        request_with_user   = type('Request', (object,), { 'user': correct_custom_user })
        return FoodLogSerializer(
            data = data,
            context = { 'request': request_with_user }
        )
    
    def test_valid_food_log_serializer(self):
        data = fixtures.get_valid_food_log_data()
        serializer = self._get_serializer_with_user(data)

        self.assertTrue(serializer.is_valid())
        self.assertEqual(data['date'], serializer.validated_data['date'])

    def test_future_date_food_log_serializer(self):
        data = fixtures.get_future_date_food_log_data()
        serializer = self._get_serializer_with_user(data)

        self.assertFalse(serializer.is_valid())
        self.assertIn('date', serializer.errors)

class FoodEntrySerializerTests(TestCase):
    def setUp(self):
        self.food_log = create_food_log(fixtures.get_valid_food_log_data())
        self.food_item = create_food_item(fixtures.get_valid_food_item_data())
        self.expected_total_macros = {
            'calories':      Decimal('100.10000'),
            'fat':           Decimal('10.01000'),
            'carbohydrates': Decimal('10.01000'),
            'protein':       Decimal('10.01000')
        }

    def test_valid_food_entry_serializer(self):
        data = fixtures.get_valid_food_entry_data()
        data['food_item_id'] = self.food_item.id
        data['description']  = 'Test description for valid food entry'

        serializer = FoodEntrySerializer(
            data = data,
            context = { 'parent_log': self.food_log }
        )

        self.assertTrue(serializer.is_valid())
        self.assertEqual(self.food_log,       serializer.validated_data['parent_log'])
        self.assertEqual(self.food_item,      serializer.validated_data['food_item'])
        self.assertEqual(data['quantity'],    serializer.validated_data['quantity'])
        self.assertEqual(data['description'], serializer.validated_data['description'])

    def test_too_low_quantity_food_entry_serializer(self):
        data = fixtures.get_invalid_food_entry_data()
        data['food_item_id'] = self.food_item.id

        serializer = FoodEntrySerializer(
            data = data,
            context = { 'parent_log': self.food_log }
        )

        self.assertFalse(serializer.is_valid())
        self.assertIn('quantity', serializer.errors)

    def test_no_food_item_food_entry_serializer(self):
        data = fixtures.get_valid_food_entry_data()

        serializer = FoodEntrySerializer(
            data = data,
            context = { 'parent_log': self.food_log }
        )

        self.assertFalse(serializer.is_valid())
        self.assertIn('food_item_id', serializer.errors)

    def test_meal_macros(self):
        data = fixtures.get_valid_food_entry_data()
        data['food_item_id'] = self.food_item.id
        data['description']  = 'Test description for meal macros food entry'

        serializer = FoodEntrySerializer(
            data = data,
            context = { 'parent_log': self.food_log }
        )
        self.assertTrue(serializer.is_valid())
        serializer.save()

        total_macros = self.food_log.total_macros
        self.assertEqual(self.expected_total_macros['calories'],      total_macros['calories'])
        self.assertEqual(self.expected_total_macros['fat'],           total_macros['fat'])
        self.assertEqual(self.expected_total_macros['carbohydrates'], total_macros['carbohydrates'])
        self.assertEqual(self.expected_total_macros['protein'],       total_macros['protein'])

"""
Strength-related serializer tests
"""
def create_muscle_group(data):
    serializer = MuscleGroupSerializer(data = data)
    if serializer.is_valid():
        return serializer.save()
    else:
        raise ValueError('Invalid data for creating MuscleGroup: {}'.format(serializer.errors))

class MuscleGroupSerializerTests(TestCase):
    def test_valid_muscle_group_serializer(self):
        data = fixtures.get_valid_muscle_group_data()
        serializer = MuscleGroupSerializer(data = data)

        self.assertTrue(serializer.is_valid())
        self.assertEqual(data['name'], serializer.validated_data['name'])

def create_strength_exercise(data, target_muscle_groups = []):
    data['target_muscle_group_ids'] = [mg.id for mg in target_muscle_groups]
    serializer = StrengthExerciseSerializer(data = data)
    if serializer.is_valid():
        return serializer.save()
    else:
        raise ValueError('Invalid data for creating StrengthExercise: {}'.format(serializer.errors))

class StrengthExerciseSerializerTests(TestCase):
    def setUp(self):
        self.muscle_group_1 = create_muscle_group(fixtures.get_valid_muscle_group_data("Test Muscle Group 1"))
        self.muscle_group_2 = create_muscle_group(fixtures.get_valid_muscle_group_data("Test Muscle Group 2"))

    def test_create_strength_exercise_with_m2m(self):
        data = fixtures.get_valid_strength_exercise_data()
        data['target_muscle_group_ids'] = [self.muscle_group_1.id, self.muscle_group_2.id]

        serializer = StrengthExerciseSerializer(data = data)

        self.assertTrue(serializer.is_valid())

        exercise = serializer.save()

        self.assertEqual(exercise.target_muscle_groups.count(), 2)
        self.assertIn(self.muscle_group_1, exercise.target_muscle_groups.all())
        self.assertIn(self.muscle_group_2, exercise.target_muscle_groups.all())

def create_strength_training(data):
    correct_custom_user = create_custom_user(fixtures.get_valid_custom_user_data())
    request_with_user   = type('Request', (object,), { 'user': correct_custom_user })

    serializer = StrengthTrainingSerializer(
            data = data,
            context = { 'request': request_with_user }
        )
    if serializer.is_valid():
        return serializer.save()
    else:
        raise ValueError('Invalid data for creating StrengthTraining: {}'.format(serializer.errors))

class StrengthTrainingSerializerTests(TestCase):
    def _get_serializer_with_user(self, data):
        correct_custom_user = create_custom_user(fixtures.get_valid_custom_user_data())
        request_with_user   = type('Request', (object,), { 'user': correct_custom_user })
        return StrengthTrainingSerializer(
            data = data,
            context = { 'request': request_with_user }
        )
    
    def test_valid_strength_training_serializer(self):
        data = fixtures.get_valid_strength_training_data()
        serializer = self._get_serializer_with_user(data)

        self.assertTrue(serializer.is_valid())
        self.assertEqual(data['date'], serializer.validated_data['date'])

    def test_future_date_strength_training_serializer(self):
        data = fixtures.get_future_date_strength_training_data()
        serializer = self._get_serializer_with_user(data)

        self.assertFalse(serializer.is_valid())
        self.assertIn('date', serializer.errors)

class StrengthSetSerializerTests(TestCase):
    def setUp(self):
        self.strength_training = create_strength_training(fixtures.get_valid_strength_training_data())
        self.strength_exercise = create_strength_exercise(fixtures.get_valid_strength_exercise_data())

    def test_valid_strength_set_serializer(self):
        data = fixtures.get_valid_strength_set_data()
        data['exercise_id'] = self.strength_exercise.id

        serializer = StrengthSetSerializer(
            data = data,
            context = { 'parent_log': self.strength_training }
        )

        self.assertTrue(serializer.is_valid())
        self.assertEqual(self.strength_training, serializer.validated_data['parent_log'])
        self.assertEqual(self.strength_exercise, serializer.validated_data['exercise'])
        self.assertEqual(data['weight'],         serializer.validated_data['weight'])
        self.assertEqual(data['reps'],           serializer.validated_data['reps'])

    def test_invalid_strength_set_serializer(self):
        data = fixtures.get_invalid_strength_set_data()
        data['exercise_id'] = self.strength_exercise.id

        serializer = StrengthSetSerializer(
            data = data,
            context = { 'parent_log': self.strength_training }
        )

        self.assertFalse(serializer.is_valid())
        self.assertIn('weight', serializer.errors)
        self.assertIn('reps',   serializer.errors)

"""
Cardio-related serializer tests
"""
def create_cardio_exercise(data):
    serializer = CardioExerciseSerializer(data = data)
    if serializer.is_valid():
        return serializer.save()
    else:
        raise ValueError('Invalid data for creating CardioExercise: {}'.format(serializer.errors))

class CardioExerciseSerializerTests(TestCase):
    def test_valid_cardio_exercise_serializer(self):
        data = fixtures.get_valid_cardio_exercise_data()
        serializer = CardioExerciseSerializer(data = data)

        self.assertTrue(serializer.is_valid())
        self.assertEqual(data['name'],                serializer.validated_data['name'])
        self.assertEqual(data['description'],         serializer.validated_data['description'])
        self.assertEqual(data['calories_per_minute'], Decimal(serializer.validated_data['calories_per_minute']))

    def test_invalid_cardio_exercise_serializer(self):
        data = fixtures.get_invalid_cardio_exercise_data()
        serializer = CardioExerciseSerializer(data = data)

        self.assertFalse(serializer.is_valid())
        self.assertIn('calories_per_minute', serializer.errors)

def create_cardio_training(data):
    correct_custom_user = create_custom_user(fixtures.get_valid_custom_user_data())
    request_with_user   = type('Request', (object,), { 'user': correct_custom_user })

    serializer = CardioTrainingSerializer(
            data = data,
            context = { 'request': request_with_user }
        )
    if serializer.is_valid():
        return serializer.save()
    else:
        raise ValueError('Invalid data for creating CardioTraining: {}'.format(serializer.errors))

class CardioTrainingSerializerTests(TestCase):
    def _get_serializer_with_user(self, data):
        correct_custom_user = create_custom_user(fixtures.get_valid_custom_user_data())
        request_with_user   = type('Request', (object,), { 'user': correct_custom_user })
        return CardioTrainingSerializer(
            data = data,
            context = { 'request': request_with_user }
        )
    
    def test_valid_cardio_training_serializer(self):
        data = fixtures.get_valid_cardio_training_data()
        serializer = self._get_serializer_with_user(data)

        self.assertTrue(serializer.is_valid())
        self.assertEqual(data['date'], serializer.validated_data['date'])

    def test_future_date_cardio_training_serializer(self):
        data = fixtures.get_future_date_cardio_training_data()
        serializer = self._get_serializer_with_user(data)

        self.assertFalse(serializer.is_valid())
        self.assertIn('date', serializer.errors)

class CardioSetSerializerTests(TestCase):
    def setUp(self):
        self.cardio_training = create_cardio_training(fixtures.get_valid_cardio_training_data())
        self.cardio_exercise = create_cardio_exercise(fixtures.get_valid_cardio_exercise_data())

    def test_valid_cardio_set_serializer(self):
        data = fixtures.get_valid_cardio_set_data()
        data['exercise_id'] = self.cardio_exercise.id

        serializer = CardioSetSerializer(
            data = data,
            context = { 'parent_log': self.cardio_training }
        )

        self.assertTrue(serializer.is_valid())
        self.assertEqual(self.cardio_training, serializer.validated_data['parent_log'])
        self.assertEqual(self.cardio_exercise, serializer.validated_data['exercise'])
        self.assertEqual(data['duration'],     serializer.validated_data['duration'])

    def test_invalid_cardio_set_serializer(self):
        data = fixtures.get_invalid_cardio_set_data()
        data['exercise_id'] = self.cardio_exercise.id

        serializer = CardioSetSerializer(
            data = data,
            context = { 'parent_log': self.cardio_training }
        )

        self.assertFalse(serializer.is_valid())
        self.assertIn('duration', serializer.errors)
