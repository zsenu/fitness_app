from django.db                      import transaction
from rest_framework                 import status
from rest_framework.views           import APIView
from rest_framework.permissions     import IsAuthenticated
from rest_framework.response        import Response
from rest_framework.generics        import get_object_or_404

from core.models                    import HealthLog
from core.models                    import FoodItem,         FoodLog,          FoodEntry
from core.models                    import StrengthExercise, StrengthSet, StrengthTraining
from core.models                    import CardioExercise,   CardioSet,   CardioTraining

from core.serializers               import HealthLogSerializer
from core.serializers               import RegisterSerializer,         UserProfileSerializer
from core.serializers               import FoodItemSerializer,         FoodLogSerializer,     FoodEntrySerializer
from core.serializers               import StrengthExerciseSerializer, StrengthSetSerializer, StrengthTrainingSerializer
from core.serializers               import CardioExerciseSerializer,   CardioSetSerializer,   CardioTrainingSerializer

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
        serializer = UserProfileSerializer(request.user.profile)
        return Response(serializer.data)

    def patch(self, request):
        profile = request.user.profile
        serializer = UserProfileSerializer(profile, data = request.data, partial = True, context = { 'request': request })

        serializer.is_valid(raise_exception = True)
        serializer.save()

        return Response(serializer.data, status = status.HTTP_200_OK)

"""
Health-related views
"""
class HealthLogListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        health_logs = HealthLog.objects.filter(user = request.user)

        serializer = HealthLogSerializer(health_logs, many = True)

        return Response(serializer.data, status = status.HTTP_200_OK)
    
    def post(self, request):
        serializer = HealthLogSerializer(data = request.data, context = { 'request': request })
        serializer.is_valid(raise_exception = True)
        serializer.save()

        return Response(serializer.data, status = status.HTTP_201_CREATED)

class HealthLogDetailView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        health_log = get_object_or_404(HealthLog, pk = pk, user = request.user)
        
        serializer = HealthLogSerializer(health_log)

        return Response(serializer.data, status = status.HTTP_200_OK)
    
    def put(self, request, pk):
        health_log = get_object_or_404(HealthLog, pk = pk, user = request.user)
        
        serializer = HealthLogSerializer(health_log, data = request.data, context = { 'request': request })
        serializer.is_valid(raise_exception = True)
        serializer.save()

        return Response(serializer.data, status = status.HTTP_200_OK)

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
        serializer = FoodItemSerializer(data = request.data, context = { 'request': request })
        serializer.is_valid(raise_exception = True)
        serializer.save()

        return Response(serializer.data, status = status.HTTP_201_CREATED)

class FoodItemDetailView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        food_item = get_object_or_404(FoodItem, pk = pk)
        
        serializer = FoodItemSerializer(food_item)

        return Response(serializer.data, status = status.HTTP_200_OK)

class FoodEntryListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, log_id):
        parent_log = get_object_or_404(FoodLog, id = log_id, user = request.user)
        food_entries = FoodEntry.objects.filter(parent_log = parent_log)

        serializer = FoodEntrySerializer(food_entries, many = True)

        return Response(serializer.data, status = status.HTTP_200_OK)
    
    def post(self, request, log_id):
        parent_log = get_object_or_404(FoodLog, id = log_id, user = request.user)

        data = request.data.copy()
        data['parent_log'] = parent_log.id

        serializer = FoodEntrySerializer(data = data, context = { 'request': request })
        serializer.is_valid(raise_exception = True)
        serializer.save()

        return Response(serializer.data, status = status.HTTP_201_CREATED)

class FoodEntryDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        food_entry = get_object_or_404(FoodEntry, pk = pk, parent_log__user = request.user)
        
        serializer = FoodEntrySerializer(food_entry)

        return Response(serializer.data, status = status.HTTP_200_OK)
    
    def put(self, request, pk):
        food_entry = get_object_or_404(FoodEntry, pk = pk, parent_log__user = request.user)
        
        serializer = FoodEntrySerializer(food_entry, data = request.data, context = { 'request': request })
        serializer.is_valid(raise_exception = True)
        serializer.save()

        return Response(serializer.data, status = status.HTTP_200_OK)
    
    def delete(self, request, pk):
        food_entry = get_object_or_404(FoodEntry, pk = pk, parent_log__user = request.user)
        
        food_entry.delete()

        return Response(status = status.HTTP_204_NO_CONTENT)

class FoodLogListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        food_logs = FoodLog.objects.filter(user = request.user)

        serializer = FoodLogSerializer(food_logs, many = True)

        return Response(serializer.data, status = status.HTTP_200_OK)
    
    def post(self, request):
        serializer = FoodLogSerializer(data = request.data, context = { 'request': request })
        serializer.is_valid(raise_exception = True)
        serializer.save()

        return Response(serializer.data, status = status.HTTP_201_CREATED)

class FoodLogDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        food_log = get_object_or_404(FoodLog, pk = pk, user = request.user)
        
        serializer = FoodLogSerializer(food_log)

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
        serializer = StrengthExerciseSerializer(data = request.data, context = { 'request': request })
        serializer.is_valid(raise_exception = True)
        serializer.save()

        return Response(serializer.data, status = status.HTTP_201_CREATED)

class StrengthExerciseDetailView(APIView):
    permission_classes = [IsAuthenticated]
        
    def get(self, request, pk):
        exercise = get_object_or_404(StrengthExercise, pk = pk)
        
        serializer = StrengthExerciseSerializer(exercise)

        return Response(serializer.data, status = status.HTTP_200_OK)

class StrengthSetListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, log_id):
        parent_log = get_object_or_404(StrengthTraining, id = log_id, user = request.user)
        sets = StrengthSet.objects.filter(parent_log = parent_log)

        serializer = StrengthSetSerializer(sets, many = True)

        return Response(serializer.data, status = status.HTTP_200_OK)
    
    def post(self, request, log_id):
        parent_log = get_object_or_404(StrengthTraining, id = log_id, user = request.user)

        data = request.data.copy()
        data['parent_log'] = parent_log.id

        serializer = StrengthSetSerializer(data = data, context = { 'request': request })
        serializer.is_valid(raise_exception = True)
        serializer.save()

        return Response(serializer.data, status = status.HTTP_201_CREATED)
    
class StrengthSetDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        strength_set = get_object_or_404(StrengthSet, pk = pk, parent_log__user = request.user)

        serializer = StrengthSetSerializer(strength_set)

        return Response(serializer.data, status = status.HTTP_200_OK)
    
    def patch(self, request, pk):
        strength_set = get_object_or_404(StrengthSet, pk = pk, parent_log__user = request.user)

        serializer = StrengthSetSerializer(strength_set, data = request.data, partial = True, context = { 'request': request })
        serializer.is_valid(raise_exception = True)
        serializer.save()

        return Response(serializer.data, status = status.HTTP_200_OK)
    
    def delete(self, request, pk):
        strength_set = get_object_or_404(StrengthSet, pk = pk, parent_log__user = request.user)
        
        strength_set.delete()

        return Response(status = status.HTTP_204_NO_CONTENT)

class StrengthTrainingListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        strength_trainings = StrengthTraining.objects.filter(user = request.user)

        serializer = StrengthTrainingSerializer(strength_trainings, many = True)

        return Response(serializer.data, status = status.HTTP_200_OK)
    
    def post(self, request):
        serializer = StrengthTrainingSerializer(data = request.data, context = { 'request': request })
        serializer.is_valid(raise_exception = True)
        serializer.save()

        return Response(serializer.data, status = status.HTTP_201_CREATED)

class StrengthTrainingDetailView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        training = get_object_or_404(StrengthTraining, pk = pk, user = request.user)

        serializer = StrengthTrainingSerializer(training)

        return Response(serializer.data, status = status.HTTP_200_OK)

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
        serializer = CardioExerciseSerializer(data = request.data, context = { 'request': request })
        serializer.is_valid(raise_exception = True)
        serializer.save()

        return Response(serializer.data, status = status.HTTP_201_CREATED)

class CardioExerciseDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        exercise = get_object_or_404(CardioExercise, pk = pk)

        serializer = CardioExerciseSerializer(exercise)

        return Response(serializer.data, status = status.HTTP_200_OK)

class CardioSetListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, log_id):
        parent_log = get_object_or_404(CardioTraining, id = log_id, user = request.user)
        sets = CardioSet.objects.filter(parent_log = parent_log)

        serializer = CardioSetSerializer(sets, many = True)

        return Response(serializer.data, status = status.HTTP_200_OK)
    
    def post(self, request, log_id):
        parent_log = get_object_or_404(CardioTraining, id = log_id, user = request.user)

        data = request.data.copy()
        data['parent_log'] = parent_log.id

        serializer = CardioSetSerializer(data = data)
        serializer.is_valid(raise_exception = True)
        serializer.save()

        return Response(serializer.data, status = status.HTTP_201_CREATED)

class CardioSetDetailView(APIView):
    permission_classes = [IsAuthenticated]
        
    def get(self, request, pk):
        cardio_set = get_object_or_404(CardioSet, pk = pk, parent_log__user = request.user)

        serializer = CardioSetSerializer(cardio_set)

        return Response(serializer.data, status = status.HTTP_200_OK)
    
    def patch(self, request, pk):
        cardio_set = get_object_or_404(CardioSet, pk = pk, parent_log__user = request.user)

        serializer = CardioSetSerializer(cardio_set, data = request.data, partial = True, context = { 'request': request })
        serializer.is_valid(raise_exception = True)
        serializer.save()

        return Response(serializer.data, status = status.HTTP_200_OK)
    
    def delete(self, request, pk):
        cardio_set = get_object_or_404(CardioSet, pk = pk, parent_log__user = request.user)

        cardio_set.delete()
        
        return Response(status = status.HTTP_204_NO_CONTENT)

class CardioTrainingListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        trainings  = CardioTraining.objects.filter(user = request.user)

        serializer = CardioTrainingSerializer(trainings, many = True)

        return Response(serializer.data, status = status.HTTP_200_OK)
    
    def post(self, request):
        serializer = CardioTrainingSerializer(data = request.data, context = { 'request': request })
        serializer.is_valid(raise_exception = True)
        serializer.save()

        return Response(serializer.data, status = status.HTTP_201_CREATED)

class CardioTrainingDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        training = get_object_or_404(CardioTraining, pk = pk, user = request.user)

        serializer = CardioTrainingSerializer(training)

        return Response(serializer.data, status = status.HTTP_200_OK)
    
    def patch(self, request, pk):
        training = get_object_or_404(CardioTraining, pk = pk, user = request.user)

        serializer = CardioTrainingSerializer(training, data = request.data, partial = True, context = { 'request': request })
        serializer.is_valid(raise_exception = True)
        serializer.save()

        return Response(serializer.data, status = status.HTTP_200_OK)
    
    def delete(self, request, pk):
        training = get_object_or_404(CardioTraining, pk = pk, user = request.user)

        training.delete()

        return Response(status = status.HTTP_204_NO_CONTENT)
