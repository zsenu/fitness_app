from django.contrib import admin

from core.models    import CustomUser
from core.models    import HealthLog
from core.models    import FoodItem,       FoodLog,          FoodEntry
from core.models    import MuscleGroup,    StrengthExercise, StrengthSet, StrengthTraining
from core.models    import CardioExercise, CardioSet,        CardioTraining

admin.site.register(CustomUser)

admin.site.register(HealthLog)

admin.site.register(FoodItem)
admin.site.register(FoodLog)
admin.site.register(FoodEntry)

admin.site.register(MuscleGroup)
admin.site.register(StrengthExercise)
admin.site.register(StrengthSet)
admin.site.register(StrengthTraining)

admin.site.register(CardioExercise)
admin.site.register(CardioSet)
admin.site.register(CardioTraining)
