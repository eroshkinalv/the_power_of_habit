from rest_framework.routers import SimpleRouter

from habit_tracker.apps import HabitTrackerConfig
from habit_tracker.views import HabitViewSet, DayViewSet

app_name = HabitTrackerConfig.name

router = SimpleRouter()

router.register(r"habit", HabitViewSet, basename="habit")
router.register(r"day", DayViewSet, basename="day")

urlpatterns = []

urlpatterns += router.urls
