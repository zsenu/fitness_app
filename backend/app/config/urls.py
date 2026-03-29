from django.contrib                 import admin
from django.urls                    import path
from core.views                     import RegisterView
from rest_framework_simplejwt.views import TokenObtainPairView
from core.views                     import UserProfileView

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/auth/register/',       RegisterView.as_view()),
    path('api/auth/login/',          TokenObtainPairView.as_view()),

    path('api/profiles/me/',         UserProfileView.as_view()),
]
