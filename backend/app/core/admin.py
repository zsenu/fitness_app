from django.contrib import admin
from .models        import UserProfile
from .models        import FoodItem
from .models        import StrengthExercise
from .models        import CardioExercise

admin.site.register(UserProfile)
admin.site.register(FoodItem)
admin.site.register(StrengthExercise)
admin.site.register(CardioExercise)
