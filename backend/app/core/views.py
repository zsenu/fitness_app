from django.db                  import transaction
from rest_framework             import status
from rest_framework.views       import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response    import Response

from .models                    import FoodItem
from .models                    import StrengthExercise
from .models                    import StrengthSet
from .models                    import StrengthTraining
from .models                    import CardioExercise
from .models                    import CardioSet
from .models                    import CardioTraining

from .serializers               import RegisterSerializer
from .serializers               import UserProfileSerializer
from .serializers               import FoodItemSerializer
from .serializers               import StrengthExerciseSerializer
from .serializers               import StrengthSetSerializer
from .serializers               import StrengthTrainingSerializer
from .serializers               import CardioExerciseSerializer
from .serializers               import CardioSetSerializer
from .serializers               import CardioTrainingSerializer

"""
View for health endpoint
"""
class HealthCheckView(APIView):
    def get(self, request):
        return Response({"status": "ok"}, status = status.HTTP_200_OK)

"""
User-related views
"""
class RegisterView(APIView):
    def post(self, request, *args, **kwargs):
        with transaction.atomic():
            serializer = RegisterSerializer(data = request.data)
            serializer.is_valid(raise_exception = True)
            user = serializer.save()
            return Response(UserProfileSerializer(user.profile).data, status = status.HTTP_201_CREATED)

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile    = request.user.profile
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data)

    def patch(self, request):
        profile    = request.user.profile
        serializer = UserProfileSerializer(profile, data = request.data, partial = True)

        serializer.is_valid(raise_exception = True)
        serializer.save()
        return Response(serializer.data, status = status.HTTP_200_OK)

"""
Health-related views
"""

"""
Food-related views
"""
class FoodItemListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        food_items = FoodItem.objects.all()
        serializer = FoodItemSerializer(food_items, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    def post(self, request):
        serializer = FoodItemSerializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        return Response(serializer.data, status = status.HTTP_201_CREATED)

class FoodItemDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return FoodItem.objects.get(pk = pk)
        except FoodItem.DoesNotExist:
            return None
    
    def get(self, request, pk):
        food_item = self.get_object(pk)
        if not food_item:
            return Response({"detail": "Food item not found."}, status = status.HTTP_404_NOT_FOUND)
        serializer = FoodItemSerializer(food_item)
        return Response(serializer.data, status = status.HTTP_200_OK)

"""
Strength-related views
"""
class StrengthExerciseListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        strength_exercises = StrengthExercise.objects.all()
        serializer = StrengthExerciseSerializer(strength_exercises, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    def post(self, request):
        serializer = StrengthExerciseSerializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        return Response(serializer.data, status = status.HTTP_201_CREATED)

class StrengthExerciseDetailView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get_object(self, pk):
        try:
            return StrengthExercise.objects.get(pk = pk)
        except StrengthExercise.DoesNotExist:
            return None
        
    def get(self, request, pk):
        exercise = self.get_object(pk)
        if not exercise:
            return Response({"detail": "Strength exercise not found."}, status = status.HTTP_404_NOT_FOUND)
        serializer = StrengthExerciseSerializer(exercise)
        return Response(serializer.data, status = status.HTTP_200_OK)

class StrengthSetListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, training_id):
        sets = StrengthSet.objects.filter(training__id = training_id, training__user = request.user)
        serializer = StrengthSetSerializer(sets, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    def post(self, request, training_id):
        try:
            training = StrengthTraining.objects.get(id = training_id, user = request.user)
        except StrengthTraining.DoesNotExist:
            return Response({"detail": "Strength training not found."}, status = status.HTTP_404_NOT_FOUND)
        
        serializer = StrengthSetSerializer(data = request.data, context = {'request': request})
        serializer.is_valid(raise_exception = True)
        serializer.save(training = training)
        return Response(serializer.data, status = status.HTTP_201_CREATED)
    
class StrengthSetDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user):
        try:
            return StrengthSet.objects.get(pk = pk, training__user = user)
        except StrengthSet.DoesNotExist:
            return None
        
    def get(self, request, pk):
        strength_set = self.get_object(pk, request.user)
        if not strength_set:
            return Response({"detail": "Strength set not found."}, status = status.HTTP_404_NOT_FOUND)
        serializer = StrengthSetSerializer(strength_set)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    def patch(self, request, pk):
        strength_set = self.get_object(pk, request.user)
        if not strength_set:
            return Response({"detail": "Strength set not found."}, status = status.HTTP_404_NOT_FOUND)
        serializer = StrengthSetSerializer(strength_set, data = request.data, partial = True, context = {'request': request})
        serializer.is_valid(raise_exception = True)
        serializer.save()
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    def delete(self, request, pk):
        strength_set = self.get_object(pk, request.user)
        if not strength_set:
            return Response({"detail": "Strength set not found."}, status = status.HTTP_404_NOT_FOUND)
        strength_set.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)

class StrengthTrainingListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        trainings  = StrengthTraining.objects.filter(user = request.user)
        serializer = StrengthTrainingSerializer(trainings, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    def post(self, request):
        serializer = StrengthTrainingSerializer(data = request.data, context = {'request': request})
        serializer.is_valid(raise_exception = True)
        serializer.save(user = request.user)
        return Response(serializer.data, status = status.HTTP_201_CREATED)

class StrengthTrainingDetailView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get_object(self, pk, user):
        try:
            return StrengthTraining.objects.get(pk = pk, user = user)
        except StrengthTraining.DoesNotExist:
            return None
        
    def get(self, request, pk):
        training = self.get_object(pk, request.user)
        if not training:
            return Response({"detail": "Strength training not found."}, status = status.HTTP_404_NOT_FOUND)
        serializer = StrengthTrainingSerializer(training)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    def patch(self, request, pk):
        training = self.get_object(pk, request.user)
        if not training:
            return Response({"detail": "Strength training not found."}, status = status.HTTP_404_NOT_FOUND)
        serializer = StrengthTrainingSerializer(training, data = request.data, partial = True, context = {'request': request})
        serializer.is_valid(raise_exception = True)
        serializer.save()
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    def delete(self, request, pk):
        training = self.get_object(pk, request.user)
        if not training:
            return Response({"detail": "Strength training not found."}, status = status.HTTP_404_NOT_FOUND)
        training.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)

"""
Cardio-related views
"""
class CardioExerciseListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cardio_exercises = CardioExercise.objects.all()
        serializer = CardioExerciseSerializer(cardio_exercises, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    def post(self, request):
        serializer = CardioExerciseSerializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        return Response(serializer.data, status = status.HTTP_201_CREATED)

class CardioExerciseDetailView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get_object(self, pk):
        try:
            return CardioExercise.objects.get(pk = pk)
        except CardioExercise.DoesNotExist:
            return None
        
    def get(self, request, pk):
        exercise = self.get_object(pk)
        if not exercise:
            return Response({"detail": "Cardio exercise not found."}, status = status.HTTP_404_NOT_FOUND)
        serializer = CardioExerciseSerializer(exercise)
        return Response(serializer.data, status = status.HTTP_200_OK)

class CardioSetListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, training_id):
        sets = CardioSet.objects.filter(training__id = training_id, training__user = request.user)
        serializer = CardioSetSerializer(sets, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    def post(self, request, training_id):
        try:
            training = CardioTraining.objects.get(id = training_id, user = request.user)
        except CardioTraining.DoesNotExist:
            return Response({"detail": "Cardio training not found."}, status = status.HTTP_404_NOT_FOUND)
        
        serializer = CardioSetSerializer(data = request.data, context = {'request': request})
        serializer.is_valid(raise_exception = True)
        serializer.save(training = training)
        return Response(serializer.data, status = status.HTTP_201_CREATED)

class CardioSetDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user):
        try:
            return CardioSet.objects.get(pk = pk, training__user = user)
        except CardioSet.DoesNotExist:
            return None
        
    def get(self, request, pk):
        cardio_set = self.get_object(pk, request.user)
        if not cardio_set:
            return Response({"detail": "Cardio set not found."}, status = status.HTTP_404_NOT_FOUND)
        serializer = CardioSetSerializer(cardio_set)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    def patch(self, request, pk):
        cardio_set = self.get_object(pk, request.user)
        if not cardio_set:
            return Response({"detail": "Cardio set not found."}, status = status.HTTP_404_NOT_FOUND)
        serializer = CardioSetSerializer(cardio_set, data = request.data, partial = True, context = {'request': request})
        serializer.is_valid(raise_exception = True)
        serializer.save()
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    def delete(self, request, pk):
        cardio_set = self.get_object(pk, request.user)
        if not cardio_set:
            return Response({"detail": "Cardio set not found."}, status = status.HTTP_404_NOT_FOUND)
        cardio_set.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)

class CardioTrainingListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        trainings  = CardioTraining.objects.filter(user = request.user)
        serializer = CardioTrainingSerializer(trainings, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    def post(self, request):
        serializer = CardioTrainingSerializer(data = request.data, context = {'request': request})
        serializer.is_valid(raise_exception = True)
        serializer.save(user = request.user)
        return Response(serializer.data, status = status.HTTP_201_CREATED)

class CardioTrainingDetailView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get_object(self, pk, user):
        try:
            return CardioTraining.objects.get(pk = pk, user = user)
        except CardioTraining.DoesNotExist:
            return None
        
    def get(self, request, pk):
        training = self.get_object(pk, request.user)
        if not training:
            return Response({"detail": "Cardio training not found."}, status = status.HTTP_404_NOT_FOUND)
        serializer = CardioTrainingSerializer(training)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    def patch(self, request, pk):
        training = self.get_object(pk, request.user)
        if not training:
            return Response({"detail": "Cardio training not found."}, status = status.HTTP_404_NOT_FOUND)
        serializer = CardioTrainingSerializer(training, data = request.data, partial = True, context = {'request': request})
        serializer.is_valid(raise_exception = True)
        serializer.save()
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    def delete(self, request, pk):
        training = self.get_object(pk, request.user)
        if not training:
            return Response({"detail": "Strength training not found."}, status = status.HTTP_404_NOT_FOUND)
        training.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)
