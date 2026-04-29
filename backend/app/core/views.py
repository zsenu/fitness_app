from rest_framework                       import status
from rest_framework.views                 import APIView
from rest_framework.permissions           import IsAuthenticated
from rest_framework.response              import Response
from rest_framework.generics              import get_object_or_404
from rest_framework.generics              import ListAPIView,               CreateAPIView,         ListCreateAPIView
from rest_framework.generics              import RetrieveAPIView,           RetrieveUpdateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.tokens      import RefreshToken
from django.utils.decorators              import method_decorator
from django.views.decorators.csrf         import csrf_exempt

from core.models                          import HealthLog
from core.models                          import FoodItem,       FoodLog,          FoodEntry
from core.models                          import MuscleGroup,    StrengthExercise, StrengthSet, StrengthTraining
from core.models                          import CardioExercise, CardioSet,        CardioTraining

from core.serializers                     import HealthLogSerializer
from core.serializers                     import RegisterSerializer,       UserSerializer
from core.serializers                     import FoodItemSerializer,       FoodLogSerializer,     FoodEntrySerializer
from core.serializers                     import MuscleGroupSerializer,    StrengthExerciseSerializer, StrengthSetSerializer, StrengthTrainingSerializer
from core.serializers                     import CardioExerciseSerializer, CardioSetSerializer,   CardioTrainingSerializer

"""
Abstract views to apply certain behaviors
"""
class InjectParentLogIntoContextMixin:
    log_model = None

    def get_parent_log(self):
        if self.log_model is None:
            raise NotImplementedError('log_model must be defined')
        if not hasattr(self, '_parent_log'):
            log_id = self.kwargs['log_id']
            self._parent_log = get_object_or_404(self.log_model, id = log_id, user = self.request.user)
        return self._parent_log

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['parent_log'] = self.get_parent_log()
        return context

"""
View for health endpoint
"""
class HealthCheckView(APIView):
    def get(self, request):
        return Response({ 'status': 'ok' }, status = status.HTTP_200_OK)

"""
User-related views
"""
class UserProfileView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class   = UserSerializer

    def get_object(self):
        return self.request.user
    
class RegisterView(CreateAPIView):
    serializer_class = RegisterSerializer

@method_decorator(csrf_exempt, name = 'dispatch')
class LoginView(APIView):
    def post(self, request):
        serializer = TokenObtainPairSerializer(data = request.data)

        try:
            serializer.is_valid(raise_exception = True)
        except Exception:
            return Response({ 'detail': 'Invalid credentials' }, status = status.HTTP_401_UNAUTHORIZED)
        
        access_token = serializer.validated_data['access']
        refresh_token = serializer.validated_data['refresh']

        response = Response({ 'access': access_token }, status = status.HTTP_200_OK)
        response.set_cookie(
            key = 'refresh_token',
            value = refresh_token,
            httponly = True,
            secure = True,
            samesite = 'None',
            path = '/'
        )

        return response

@method_decorator(csrf_exempt, name = 'dispatch')
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token')
        if refresh_token is not None:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
            except Exception:
                pass

        response = Response({ 'detail': 'Logged out successfully' }, status = status.HTTP_200_OK)
        response.delete_cookie('refresh_token', path = '/')
        return response

@method_decorator(csrf_exempt, name = 'dispatch')
class TokenRefreshView(APIView):
    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token')
        if refresh_token is None:
            return Response({ 'detail': 'Refresh token not found' }, status = status.HTTP_404_NOT_FOUND)
        
        serializer = TokenRefreshSerializer(data = { 'refresh': refresh_token })
        try:
            serializer.is_valid(raise_exception = True)
        except Exception:
            return Response({ 'detail': 'Invalid refresh token' }, status = status.HTTP_401_UNAUTHORIZED)
        
        access_token = serializer.validated_data['access']
        return Response({ 'access': access_token }, status = status.HTTP_200_OK)

"""
Health-related views
"""
class HealthLogListView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class   = HealthLogSerializer

    def get_queryset(self):
        return HealthLog.objects.filter(user = self.request.user)

class HealthLogDetailView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class   = HealthLogSerializer

    def get_queryset(self):
        return HealthLog.objects.filter(user = self.request.user)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        serializer = self.get_serializer(instance, data = request.data, partial = True)
        serializer.is_valid(raise_exception = True)
        serializer.save()

        if not HealthLog.objects.filter(pk = instance.id).exists():
            return Response(status = status.HTTP_410_GONE)

        return Response(serializer.data, status = status.HTTP_200_OK)

class HealthLogByDateView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class   = HealthLogSerializer

    def get_object(self):
        date_str = self.kwargs['date']
        health_log = get_object_or_404(HealthLog, user = self.request.user, date = date_str)
        return health_log

"""
Food-related views
"""
class FoodItemListView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class   = FoodItemSerializer
    queryset           = FoodItem.objects.all()

class FoodItemDetailView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class   = FoodItemSerializer
    queryset           = FoodItem.objects.all()

class FoodEntryListView(InjectParentLogIntoContextMixin, ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class   = FoodEntrySerializer
    log_model          = FoodLog

    def get_queryset(self):
        return FoodEntry.objects.filter(parent_log = self.get_parent_log()).select_related('food_item')

class FoodEntryDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class   = FoodEntrySerializer

    def get_queryset(self):
        return FoodEntry.objects.filter(parent_log__user = self.request.user).select_related('food_item')

class FoodLogListView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class   = FoodLogSerializer

    def get_queryset(self):
        return FoodLog.objects.filter(user = self.request.user).prefetch_related('entries__food_item')

class FoodLogDetailView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class   = FoodLogSerializer

    def get_queryset(self):
        return FoodLog.objects.filter(user = self.request.user).prefetch_related('entries__food_item')

class FoodLogByDateView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class   = FoodLogSerializer

    def get_object(self):
        date_str = self.kwargs['date']
        food_log = get_object_or_404(FoodLog, user = self.request.user, date = date_str)
        return food_log

"""
Strength-related views
"""
class MuscleGroupListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class   = MuscleGroupSerializer
    queryset           = MuscleGroup.objects.all()

class StrengthExerciseListView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class   = StrengthExerciseSerializer
    queryset           = StrengthExercise.objects.all()

class StrengthExerciseDetailView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class   = StrengthExerciseSerializer
    queryset           = StrengthExercise.objects.all()

class StrengthSetListView(InjectParentLogIntoContextMixin, ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class   = StrengthSetSerializer
    log_model          = StrengthTraining
    
    def get_queryset(self):
        return StrengthSet.objects.filter(parent_log = self.get_parent_log()).select_related('exercise')
   
class StrengthSetDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class   = StrengthSetSerializer

    def get_queryset(self):
        return StrengthSet.objects.filter(parent_log__user = self.request.user).select_related('exercise')

class StrengthTrainingListView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class   = StrengthTrainingSerializer

    def get_queryset(self):
        return StrengthTraining.objects.filter(user = self.request.user).prefetch_related('session_sets__exercise')

class StrengthTrainingDetailView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class   = StrengthTrainingSerializer

    def get_queryset(self):
        return StrengthTraining.objects.filter(user = self.request.user).prefetch_related('session_sets__exercise')

class StrengthTrainingByDateView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class   = StrengthTrainingSerializer

    def get_object(self):
        date_str = self.kwargs['date']
        training = get_object_or_404(StrengthTraining, user = self.request.user, date = date_str)
        return training

"""
Cardio-related views
"""
class CardioExerciseListView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class   = CardioExerciseSerializer
    queryset           = CardioExercise.objects.all()

class CardioExerciseDetailView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class   = CardioExerciseSerializer
    queryset           = CardioExercise.objects.all()

class CardioSetListView(InjectParentLogIntoContextMixin, ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class   = CardioSetSerializer
    log_model          = CardioTraining
    
    def get_queryset(self):
        return CardioSet.objects.filter(parent_log = self.get_parent_log()).select_related('exercise')
    
class CardioSetDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class   = CardioSetSerializer

    def get_queryset(self):
        return CardioSet.objects.filter(parent_log__user = self.request.user).select_related('exercise')

class CardioTrainingListView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class   = CardioTrainingSerializer

    def get_queryset(self):
        return CardioTraining.objects.filter(user = self.request.user).prefetch_related('session_sets__exercise')
    
class CardioTrainingDetailView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class   = CardioTrainingSerializer

    def get_queryset(self):
        return CardioTraining.objects.filter(user = self.request.user).prefetch_related('session_sets__exercise')

class CardioTrainingByDateView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class   = CardioTrainingSerializer

    def get_object(self):
        date_str = self.kwargs['date']
        training = get_object_or_404(CardioTraining, user = self.request.user, date = date_str)
        return training
