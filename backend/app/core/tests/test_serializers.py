from   datetime                        import date
from   decimal                         import Decimal
from   django.test                     import TestCase
from   core.models                     import CustomUser
from   core.serializers                import UserSerializer, RegisterSerializer
import core.tests.fixtures_serializers as fixtures

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

    def ignore_test_invalid_registration_serializer(self):
        data = fixtures.get_invalid_custom_user_data()
        serializer = RegisterSerializer(data = data)

        self.assertFalse(serializer.is_valid())
        self.assertIn('gender', serializer.errors)
        self.assertIn('birth_date', serializer.errors)
        self.assertIn('height', serializer.errors)
        self.assertIn('starting_weight', serializer.errors)
        self.assertIn('target_weight', serializer.errors)
        self.assertIn('target_date', serializer.errors)
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
        self.assertEqual(data['target_weight'],   Decimal(serializer.data['target_weight']))
        self.assertEqual(data['target_date'],     date.fromisoformat(serializer.data['target_date']))
        self.assertEqual(data['target_calories'], Decimal(serializer.data['target_calories']))
