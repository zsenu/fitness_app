from django.contrib                 import admin
from django.urls                    import path
from rest_framework_simplejwt.views import TokenObtainPairView

from core.views                     import HealthCheckView
from core.views                     import RegisterView,             UserProfileView
from core.views                     import HealthLogListView,        HealthLogDetailView
from core.views                     import FoodItemListView,         FoodItemDetailView
from core.views                     import FoodLogListView,          FoodLogDetailView
from core.views                     import StrengthExerciseListView, StrengthExerciseDetailView
from core.views                     import StrengthSetListView,      StrengthSetDetailView
from core.views                     import StrengthTrainingListView, StrengthTrainingDetailView
from core.views                     import CardioExerciseListView,   CardioExerciseDetailView
from core.views                     import CardioSetListView,        CardioSetDetailView
from core.views                     import CardioTrainingListView,   CardioTrainingDetailView

urlpatterns = [
    path('health/', HealthCheckView.as_view(), name = 'health-check'),

    path('admin/', admin.site.urls),

    path('api/auth/register/',                             RegisterView.as_view()),
    path('api/auth/login/',                                TokenObtainPairView.as_view()),

    path('api/profiles/me/',                               UserProfileView.as_view()),

    path('api/health-logs/',                               HealthLogListView.as_view()),
    path('api/health-logs/<int:pk>/',                      HealthLogDetailView.as_view()),

    path('api/food-items/',                                FoodItemListView.as_view()),
    path('api/food-items/<int:pk>/',                       FoodItemDetailView.as_view()),

    path('api/food-logs/',                                 FoodLogListView.as_view()),
    path('api/food-logs/<int:pk>/',                        FoodLogDetailView.as_view()),

    path('api/strength-exercises/',                        StrengthExerciseListView.as_view()),
    path('api/strength-exercises/<int:pk>/',               StrengthExerciseDetailView.as_view()),
    path('api/strength-trainings/',                        StrengthTrainingListView.as_view()),
    path('api/strength-trainings/<int:pk>/',               StrengthTrainingDetailView.as_view()),
    path('api/strength-trainings/<int:training_id>/sets/', StrengthSetListView.as_view()),
    path('api/strength-trainings/sets/<int:pk>/',          StrengthSetDetailView.as_view()),

    path('api/cardio-exercises/',                          CardioExerciseListView.as_view()),
    path('api/cardio-exercises/<int:pk>/',                 CardioExerciseDetailView.as_view()),
    path('api/cardio-trainings/',                          CardioTrainingListView.as_view()),
    path('api/cardio-trainings/<int:pk>/',                 CardioTrainingDetailView.as_view()),
    path('api/cardio-trainings/<int:training_id>/sets/',   CardioSetListView.as_view()),
    path('api/cardio-trainings/sets/<int:pk>/',            CardioSetDetailView.as_view())
]
