from django.contrib                 import admin
from django.urls                    import path
from core.views                     import RegisterView
from rest_framework_simplejwt.views import TokenObtainPairView
from core.views                     import UserProfileView
from core.views                     import FoodItemListView
from core.views                     import FoodItemDetailView
from core.views                     import StrengthExerciseListView
from core.views                     import StrengthExerciseDetailView
from core.views                     import CardioExerciseListView
from core.views                     import CardioExerciseDetailView

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/auth/register/',       RegisterView.as_view()),
    path('api/auth/login/',          TokenObtainPairView.as_view()),

    path('api/profiles/me/',         UserProfileView.as_view()),

    path('api/food-items/',          FoodItemListView.as_view()),
    path('api/food-items/<int:pk>/', FoodItemDetailView.as_view()),

    path('api/strength-exercises/',          StrengthExerciseListView.as_view()),
    path('api/strength-exercises/<int:pk>/', StrengthExerciseDetailView.as_view()),

    path('api/cardio-exercises/',          CardioExerciseListView.as_view()),
    path('api/cardio-exercises/<int:pk>/', CardioExerciseDetailView.as_view()),
]
