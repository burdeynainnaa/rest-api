from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import PlayerViewSet, TeamViewSet, TournamentViewSet

router = DefaultRouter()
router.register("tournaments", TournamentViewSet, basename="tournament")
router.register("teams", TeamViewSet, basename="team")
router.register("players", PlayerViewSet, basename="player")

urlpatterns = [
    path("", include(router.urls)),
]