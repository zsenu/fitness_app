from django.db                  import transaction
from rest_framework             import status
from rest_framework.views       import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response    import Response

from .models                    import FoodItem
from .models                    import StrengthExercise
from .models                    import CardioExercise

from .serializers               import RegisterSerializer
from .serializers               import UserProfileSerializer
from .serializers               import FoodItemSerializer
from .serializers               import StrengthExerciseSerializer
from .serializers               import CardioExerciseSerializer

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
