from django.contrib import admin
from .models        import UserProfile
from .models        import FoodItem
from .models        import StrengthExercise
from .models        import StrengthSet
from .models        import StrengthTraining
from .models        import CardioExercise
from .models        import CardioSet
from .models        import CardioTraining

admin.site.register(UserProfile)

admin.site.register(FoodItem)

admin.site.register(StrengthExercise)
admin.site.register(StrengthSet)
admin.site.register(StrengthTraining)

admin.site.register(CardioExercise)
admin.site.register(CardioSet)
admin.site.register(CardioTraining)
