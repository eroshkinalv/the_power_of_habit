from rest_framework.routers import SimpleRouter

from habit_tracker.apps import HabitTrackerConfig
from habit_tracker.views import HabitViewSet

app_name = HabitTrackerConfig.name

router = SimpleRouter()

router.register(r"habit", HabitViewSet, basename="habit")

urlpatterns = []

urlpatterns += router.urls
