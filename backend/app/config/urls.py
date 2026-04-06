from django.contrib                 import admin
from django.urls                    import path
from rest_framework_simplejwt.views import TokenObtainPairView

from core.views                     import HealthCheckView
from core.views                     import RegisterView,             UserProfileView
from core.views                     import HealthLogListView,        HealthLogDetailView
from core.views                     import FoodItemListView,         FoodItemDetailView
from core.views                     import FoodLogListView,          FoodLogDetailView
from core.views                     import FoodEntryListView,        FoodEntryDetailView
from core.views                     import StrengthExerciseListView, StrengthExerciseDetailView
from core.views                     import StrengthSetListView,      StrengthSetDetailView
from core.views                     import StrengthTrainingListView, StrengthTrainingDetailView
from core.views                     import CardioExerciseListView,   CardioExerciseDetailView
from core.views                     import CardioSetListView,        CardioSetDetailView
from core.views                     import CardioTrainingListView,   CardioTrainingDetailView

urlpatterns = [
    path('health/',                                   HealthCheckView.as_view(),            name = 'health-check'),

    path('admin/',                                    admin.site.urls,                      name = 'admin'),

    path('api/auth/register/',                        RegisterView.as_view(),               name = 'register'),
    path('api/auth/login/',                           TokenObtainPairView.as_view(),        name = 'login'),

    path('api/profiles/me/',                          UserProfileView.as_view(),            name = 'user-profile'),

    path('api/health-logs/',                          HealthLogListView.as_view(),          name = 'health-log-list'),
    path('api/health-logs/<int:pk>/',                 HealthLogDetailView.as_view(),        name = 'health-log-detail'),

    path('api/food-items/',                           FoodItemListView.as_view(),           name = 'food-item-list'),
    path('api/food-items/<int:pk>/',                  FoodItemDetailView.as_view(),         name = 'food-item-detail'),
    path('api/food-logs/',                            FoodLogListView.as_view(),            name = 'food-log-list'),
    path('api/food-logs/<int:pk>/',                   FoodLogDetailView.as_view(),          name = 'food-log-detail'),
    path('api/food-logs/<int:log_id>/entries/',       FoodEntryListView.as_view(),          name = 'food-entry-list'),
    path('api/food-logs/entries/<int:pk>/',           FoodEntryDetailView.as_view(),        name = 'food-entry-detail'),

    path('api/strength-exercises/',                   StrengthExerciseListView.as_view(),   name = 'strength-exercise-list'),
    path('api/strength-exercises/<int:pk>/',          StrengthExerciseDetailView.as_view(), name = 'strength-exercise-detail'),
    path('api/strength-trainings/',                   StrengthTrainingListView.as_view(),   name = 'strength-training-list'),
    path('api/strength-trainings/<int:pk>/',          StrengthTrainingDetailView.as_view(), name = 'strength-training-detail'),
    path('api/strength-trainings/<int:log_id>/sets/', StrengthSetListView.as_view(),        name = 'strength-set-list'),
    path('api/strength-trainings/sets/<int:pk>/',     StrengthSetDetailView.as_view(),      name = 'strength-set-detail'),

    # TO BE TESTED
    path('api/cardio-exercises/',                     CardioExerciseListView.as_view(),     name = 'cardio-exercise-list'),
    # TO BE TESTED
    path('api/cardio-exercises/<int:pk>/',            CardioExerciseDetailView.as_view(),   name = 'cardio-exercise-detail'),
    # TO BE TESTED
    path('api/cardio-trainings/',                     CardioTrainingListView.as_view(),     name = 'cardio-training-list'),
    # TO BE TESTED
    path('api/cardio-trainings/<int:pk>/',            CardioTrainingDetailView.as_view(),   name = 'cardio-training-detail'),
    # TO BE TESTED
    path('api/cardio-trainings/<int:log_id>/sets/',   CardioSetListView.as_view(),          name = 'cardio-set-list'),
    # TO BE TESTED
    path('api/cardio-trainings/sets/<int:pk>/',       CardioSetDetailView.as_view(),        name = 'cardio-set-detail')
]
