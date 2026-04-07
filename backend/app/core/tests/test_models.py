from   decimal                import Decimal
from   django.test            import TestCase
from   django.core.exceptions import ValidationError
from   core.models            import CustomUser, HealthLog
from   core.models            import FoodItem, FoodLog, FoodEntry
from   core.models            import MuscleGroup, StrengthExercise, StrengthTraining, StrengthSet
from   core.models            import CardioExercise, CardioTraining, CardioSet
import core.tests.fixtures    as fixtures

"""
User-related model tests
"""
def create_custom_user(data):
    password = data.pop('password')
    custom_user = CustomUser(**data)
    custom_user.set_password(password)
    custom_user.full_clean()
    custom_user.save()
    return custom_user

class CustomUserModelTests(TestCase):
    def test_create_valid_custom_user(self):
        custom_user = create_custom_user(fixtures.get_valid_custom_user_data())
        self.assertIsNotNone(custom_user.id)

    def test_create_wrong_gender_custom_user(self):
        with self.assertRaises(ValidationError) as context:
            create_custom_user(fixtures.get_wrong_gender_custom_user_data())
        self.assertIn('gender', context.exception.message_dict)

    def test_create_too_young_custom_user(self):
        with self.assertRaises(ValidationError) as context:
            create_custom_user(fixtures.get_too_young_custom_user_data())
        self.assertIn('birth_date', context.exception.message_dict)

    def test_create_too_old_custom_user(self):
        with self.assertRaises(ValidationError) as context:
            create_custom_user(fixtures.get_too_old_custom_user_data())
        self.assertIn('birth_date', context.exception.message_dict)

    def test_create_too_short_custom_user(self):
        with self.assertRaises(ValidationError) as context:
            create_custom_user(fixtures.get_too_short_custom_user_data())
        self.assertIn('height', context.exception.message_dict)

    def test_create_too_tall_custom_user(self):
        with self.assertRaises(ValidationError) as context:
            create_custom_user(fixtures.get_too_tall_custom_user_data())
        self.assertIn('height', context.exception.message_dict)

    def test_create_too_light_custom_user(self):
        with self.assertRaises(ValidationError) as context:
            create_custom_user(fixtures.get_too_light_custom_user_data())
        self.assertIn('starting_weight', context.exception.message_dict)

    def test_create_too_heavy_custom_user(self):
        with self.assertRaises(ValidationError) as context:
            create_custom_user(fixtures.get_too_heavy_custom_user_data())
        self.assertIn('starting_weight', context.exception.message_dict)

    def test_create_too_low_target_weight_custom_user(self):
        with self.assertRaises(ValidationError) as context:
            create_custom_user(fixtures.get_too_low_target_weight_custom_user_data())
        self.assertIn('target_weight', context.exception.message_dict)
    
    def test_create_too_high_target_weight_custom_user(self):
        with self.assertRaises(ValidationError) as context:
            create_custom_user(fixtures.get_too_high_target_weight_custom_user_data())
        self.assertIn('target_weight', context.exception.message_dict)

    def test_create_too_low_target_calories_custom_user(self):
        with self.assertRaises(ValidationError) as context:
            create_custom_user(fixtures.get_too_low_target_calories_custom_user_data())
        self.assertIn('target_calories', context.exception.message_dict)

    def test_create_too_high_target_calories_custom_user(self):
        with self.assertRaises(ValidationError) as context:
            create_custom_user(fixtures.get_too_high_target_calories_custom_user_data())
        self.assertIn('target_calories', context.exception.message_dict)

"""
Health-related model tests
"""
class HealthLogModelTests(TestCase):
    def setUp(self):
        self.correct_custom_user = create_custom_user(fixtures.get_valid_custom_user_data())
        
    def create_health_log(self, data):
        health_log = HealthLog(**data)
        health_log.user = self.correct_custom_user
        health_log.full_clean()
        health_log.save()
        return health_log

    def test_create_valid_health_log(self):
        health_log = self.create_health_log(fixtures.get_valid_health_log_data())
        self.assertIsNotNone(health_log.id)

    def test_create_empty_health_log(self):
        with self.assertRaises(ValidationError) as context:
            self.create_health_log(fixtures.get_empty_health_log_data())
        self.assertIn('health_log', context.exception.message_dict)

    def test_create_too_low_bodyweight_health_log(self):
        with self.assertRaises(ValidationError) as context:
            self.create_health_log(fixtures.get_too_low_bodyweight_health_log_data())
        self.assertIn('bodyweight', context.exception.message_dict)

    def test_create_too_high_bodyweight_health_log(self):
        with self.assertRaises(ValidationError) as context:
            self.create_health_log(fixtures.get_too_high_bodyweight_health_log_data())
        self.assertIn('bodyweight', context.exception.message_dict)

    def test_create_too_low_hours_slept_health_log(self):
        with self.assertRaises(ValidationError) as context:
            self.create_health_log(fixtures.get_too_low_hours_slept_health_log_data())
        self.assertIn('hours_slept', context.exception.message_dict)

    def test_create_too_high_hours_slept_health_log(self):
        with self.assertRaises(ValidationError) as context:
            self.create_health_log(fixtures.get_too_high_hours_slept_health_log_data())
        self.assertIn('hours_slept', context.exception.message_dict)

    def test_create_too_low_liquid_consumed_health_log(self):
        with self.assertRaises(ValidationError) as context:
            self.create_health_log(fixtures.get_too_low_liquid_consumed_health_log_data())
        self.assertIn('liquid_consumed', context.exception.message_dict)

    def test_create_too_high_liquid_consumed_health_log(self):
        with self.assertRaises(ValidationError) as context:
            self.create_health_log(fixtures.get_too_high_liquid_consumed_health_log_data())
        self.assertIn('liquid_consumed', context.exception.message_dict)
        
"""
Food-related model tests
"""
def create_food_item(data):
        food_item = FoodItem(**data)
        food_item.full_clean()
        food_item.save()
        return food_item

class FoodItemModelTests(TestCase): 
    def test_create_valid_food_item(self):
        food_item = create_food_item(fixtures.get_valid_food_item_data())
        self.assertIsNotNone(food_item.id)
    
    def test_create_empty_food_item(self):
        food_item = create_food_item(fixtures.get_empty_food_item_data())
        self.assertIsNotNone(food_item.id)
        self.assertAlmostEqual(0, food_item.carbohydrates)
        self.assertAlmostEqual(0, food_item.protein)
        self.assertAlmostEqual(0, food_item.fat)

    def test_create_too_low_nutrients_food_item(self):
        with self.assertRaises(ValidationError) as context:
            create_food_item(fixtures.get_too_low_nutrients_food_item_data())
        self.assertIn('calories',      context.exception.message_dict)
        self.assertIn('fat',           context.exception.message_dict)
        self.assertIn('carbohydrates', context.exception.message_dict)
        self.assertIn('protein',       context.exception.message_dict)

    def test_create_too_high_nutrients_food_item(self):
        with self.assertRaises(ValidationError) as context:
            create_food_item(fixtures.get_too_high_nutrients_food_item_data())
        self.assertIn('calories',      context.exception.message_dict)
        self.assertIn('fat',           context.exception.message_dict)
        self.assertIn('carbohydrates', context.exception.message_dict)
        self.assertIn('protein',       context.exception.message_dict)

def create_food_log(data, user):
    food_log = FoodLog(**data)
    food_log.user = user
    food_log.full_clean()
    food_log.save()
    return food_log

class FoodLogModelTests(TestCase):
    def setUp(self):
        self.correct_custom_user = create_custom_user(fixtures.get_valid_custom_user_data())

    def test_create_valid_food_log(self):
        food_log = create_food_log(fixtures.get_valid_food_log_data(), self.correct_custom_user)
        self.assertIsNotNone(food_log.id)

    def test_create_future_food_log(self):
        with self.assertRaises(ValidationError) as context:
            create_food_log(fixtures.get_future_date_food_log_data(), self.correct_custom_user)
        self.assertIn('date', context.exception.message_dict)

class FoodEntryModelTests(TestCase):
    def setUp(self):
        self.correct_custom_user = create_custom_user(fixtures.get_valid_custom_user_data())
        self.correct_food_log    =    create_food_log(fixtures.get_valid_food_log_data(), self.correct_custom_user)
        self.correct_food_item   =   create_food_item(fixtures.get_valid_food_item_data())
        self.expected_total_macros = {
            'calories':      Decimal('100.10000'),
            'fat':           Decimal('10.01000'),
            'carbohydrates': Decimal('10.01000'),
            'protein':       Decimal('10.01000')
        }

    def create_food_entry(self, data, include_food_item = True):
        food_entry = FoodEntry(**data)
        food_entry.parent_log = self.correct_food_log
        if include_food_item:
            food_entry.food_item = self.correct_food_item
        food_entry.full_clean()
        food_entry.save()
        return food_entry
    
    def test_create_valid_food_entry(self):
        food_entry = self.create_food_entry(fixtures.get_valid_food_entry_data())
        self.assertIsNotNone(food_entry.id)

    def test_create_too_low_quantity_food_entry(self):
        with self.assertRaises(ValidationError) as context:
            self.create_food_entry(fixtures.get_too_low_quantity_food_entry_data())
        self.assertIn('quantity', context.exception.message_dict)

    def test_create_food_entry_without_food_item(self):
        with self.assertRaises(ValidationError) as context:
            self.create_food_entry(fixtures.get_valid_food_entry_data(), include_food_item = False)
        self.assertIn('food_item', context.exception.message_dict)

    def test_meal_macros(self):
        food_entry = self.create_food_entry(fixtures.get_valid_food_entry_data())
        self.assertIsNotNone(food_entry.id)
        self.assertEqual(self.expected_total_macros, self.correct_food_log.total_macros)

    def test_delete_food_entry_deletes_parent_log(self):
        food_entry = self.create_food_entry(fixtures.get_valid_food_entry_data())
        parent_log_id = food_entry.parent_log.id
        food_entry.delete()
        with self.assertRaises(FoodLog.DoesNotExist):
            FoodLog.objects.get(id = parent_log_id)

"""
Strength-related model tests
"""
def create_muscle_group(data):
    muscle_group = MuscleGroup(**data)
    muscle_group.full_clean()
    muscle_group.save()
    return muscle_group

class MuscleGroupModelTests(TestCase):
    def test_create_valid_muscle_group(self):
        muscle_group = create_muscle_group(fixtures.get_valid_muscle_group_data())
        self.assertIsNotNone(muscle_group.id)

def create_strength_exercise(data, target_muscle_groups):
    strength_exercise = StrengthExercise(**data)
    strength_exercise.full_clean()
    strength_exercise.save()
    strength_exercise.target_muscle_groups.set(target_muscle_groups)
    return strength_exercise

class StrengthExerciseModelTests(TestCase):
    def setUp(self):
        self.correct_muscle_group_1 = create_muscle_group(fixtures.get_valid_muscle_group_data())
        self.correct_muscle_group_2 = create_muscle_group(fixtures.get_valid_muscle_group_data(custom_name = 'Test Muscle Group 2'))

    def test_create_valid_strength_exercise(self):
        strength_exercise = create_strength_exercise(fixtures.get_valid_strength_exercise_data(), [self.correct_muscle_group_1, self.correct_muscle_group_2])
        self.assertIsNotNone(strength_exercise.id)

def create_strength_training(data, user):
    strength_training = StrengthTraining(**data)
    strength_training.user = user
    strength_training.full_clean()
    strength_training.save()
    return strength_training

class StrengthTrainingModelTests(TestCase):
    def setUp(self):
        self.correct_custom_user = create_custom_user(fixtures.get_valid_custom_user_data())

    def test_create_valid_strength_training(self):
        strength_training = create_strength_training(fixtures.get_valid_strength_training_data(), self.correct_custom_user)
        self.assertIsNotNone(strength_training.id)

    def test_create_future_strength_training(self):
        with self.assertRaises(ValidationError) as context:
            create_strength_training(fixtures.get_future_date_strength_training_data(), self.correct_custom_user)
        self.assertIn('date', context.exception.message_dict)

class StrengthSetModelTests(TestCase):
    def setUp(self):
        self.correct_custom_user = create_custom_user(fixtures.get_valid_custom_user_data())
        self.correct_strength_training = create_strength_training(fixtures.get_valid_strength_training_data(), self.correct_custom_user)
        self.correct_muscle_group = create_muscle_group(fixtures.get_valid_muscle_group_data())
        self.correct_strength_exercise = create_strength_exercise(fixtures.get_valid_strength_exercise_data(), [self.correct_muscle_group])

    def create_strength_set(self, data):
        strength_set = StrengthSet(**data)
        strength_set.parent_log = self.correct_strength_training
        strength_set.exercise = self.correct_strength_exercise
        strength_set.full_clean()
        strength_set.save()
        return strength_set

    def test_create_valid_strength_set(self):
        strength_set = self.create_strength_set(fixtures.get_valid_strength_set_data())
        self.assertIsNotNone(strength_set.id)

    def test_create_too_low_weight_strength_set(self):
        with self.assertRaises(ValidationError) as context:
            self.create_strength_set(fixtures.get_too_low_weight_strength_set_data())
        self.assertIn('weight', context.exception.message_dict)

    def test_create_too_high_weight_strength_set(self):
        with self.assertRaises(ValidationError) as context:
            self.create_strength_set(fixtures.get_too_high_weight_strength_set_data())
        self.assertIn('weight', context.exception.message_dict)

    def test_create_too_low_reps_strength_set(self):
        with self.assertRaises(ValidationError) as context:
            self.create_strength_set(fixtures.get_too_low_reps_strength_set_data())
        self.assertIn('reps', context.exception.message_dict)

    def test_delete_strength_set_deletes_parent_log(self):
        strength_set = self.create_strength_set(fixtures.get_valid_strength_set_data())
        parent_log_id = strength_set.parent_log.id
        strength_set.delete()
        with self.assertRaises(StrengthTraining.DoesNotExist):
            StrengthTraining.objects.get(id = parent_log_id)

"""
Cardio-related model tests
"""
def create_cardio_exercise(data):
    cardio_exercise = CardioExercise(**data)
    cardio_exercise.full_clean()
    cardio_exercise.save()
    return cardio_exercise

class CardioExerciseModelTests(TestCase):
    def test_create_valid_cardio_exercise(self):
        cardio_exercise = create_cardio_exercise(fixtures.get_valid_cardio_exercise_data())
        self.assertIsNotNone(cardio_exercise.id)

    def test_create_too_low_calories_per_minute_cardio_exercise(self):
        with self.assertRaises(ValidationError) as context:
            create_cardio_exercise(fixtures.get_too_low_calories_per_minute_cardio_exercise_data())
        self.assertIn('calories_per_minute', context.exception.message_dict)

    def test_create_too_high_calories_per_minute_cardio_exercise(self):
        with self.assertRaises(ValidationError) as context:
            create_cardio_exercise(fixtures.get_too_high_calories_per_minute_cardio_exercise_data())
        self.assertIn('calories_per_minute', context.exception.message_dict)

def create_cardio_training(data, user):
    cardio_training = CardioTraining(**data)
    cardio_training.user = user
    cardio_training.full_clean()
    cardio_training.save()
    return cardio_training

class CardioTrainingModelTests(TestCase):
    def setUp(self):
        self.correct_custom_user = create_custom_user(fixtures.get_valid_custom_user_data())

    def test_create_valid_cardio_training(self):
        cardio_training = create_cardio_training(fixtures.get_valid_cardio_training_data(), self.correct_custom_user)
        self.assertIsNotNone(cardio_training.id)

    def test_create_future_cardio_training(self):
        with self.assertRaises(ValidationError) as context:
            create_cardio_training(fixtures.get_future_date_cardio_training_data(), self.correct_custom_user)
        self.assertIn('date', context.exception.message_dict)

class CardioSetModelTests(TestCase):
    def setUp(self):
        self.correct_custom_user = create_custom_user(fixtures.get_valid_custom_user_data())
        self.correct_cardio_training = create_cardio_training(fixtures.get_valid_cardio_training_data(), self.correct_custom_user)
        self.correct_cardio_exercise = create_cardio_exercise(fixtures.get_valid_cardio_exercise_data())

    def create_cardio_set(self, data):
        cardio_set = CardioSet(**data)
        cardio_set.parent_log = self.correct_cardio_training
        cardio_set.exercise = self.correct_cardio_exercise
        cardio_set.full_clean()
        cardio_set.save()
        return cardio_set

    def test_create_valid_cardio_set(self):
        cardio_set = self.create_cardio_set(fixtures.get_valid_cardio_set_data())
        self.assertIsNotNone(cardio_set.id)

    def test_create_too_low_duration_cardio_set(self):
        with self.assertRaises(ValidationError) as context:
            self.create_cardio_set(fixtures.get_too_low_duration_cardio_set_data())
        self.assertIn('duration', context.exception.message_dict)

    def test_create_too_high_duration_cardio_set(self):
        with self.assertRaises(ValidationError) as context:
            self.create_cardio_set(fixtures.get_too_high_duration_cardio_set_data())
        self.assertIn('duration', context.exception.message_dict)

    def test_delete_cardio_set_deletes_parent_log(self):
        cardio_set = self.create_cardio_set(fixtures.get_valid_cardio_set_data())
        parent_log_id = cardio_set.parent_log.id
        cardio_set.delete()
        with self.assertRaises(CardioTraining.DoesNotExist):
            CardioTraining.objects.get(id = parent_log_id)
