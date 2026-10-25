from django.urls import path

from .views import (
    PlayerDetailAPIView,
    PlayerListCreateAPIView,
    TeamDetailAPIView,
    TeamListCreateAPIView,
    TournamentDetailAPIView,
    TournamentListCreateAPIView,
)

urlpatterns = [
    path(
        "tournaments/",
        TournamentListCreateAPIView.as_view(),
        name="tournament-list-create",
    ),
    path(
        "tournaments/<int:pk>/",
        TournamentDetailAPIView.as_view(),
        name="tournament-detail",
    ),
    path("teams/", TeamListCreateAPIView.as_view(), name="team-list-create"),
    path("teams/<int:pk>/", TeamDetailAPIView.as_view(), name="team-detail"),
    path("players/", PlayerListCreateAPIView.as_view(), name="player-list-create"),
    path("players/<int:pk>/", PlayerDetailAPIView.as_view(), name="player-detail"),
]
