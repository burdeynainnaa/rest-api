import logging
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, extend_schema_view

from .models import Player, Team, Tournament
from .serializers import PlayerSerializer, TeamSerializer, TournamentSerializer

logger = logging.getLogger(__name__)


@extend_schema_view(
    list=extend_schema(summary="Отримати список усіх турнірів"),
    create=extend_schema(summary="Створити новий турнір"),
    retrieve=extend_schema(summary="Отримати деталі турніру"),
    update=extend_schema(summary="Повністю оновити турнір"),
    partial_update=extend_schema(summary="Частково оновити турнір"),
    destroy=extend_schema(summary="Видалити турнір"),
)
class TournamentViewSet(viewsets.ModelViewSet):
    queryset = Tournament.objects.all()
    serializer_class = TournamentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        tournament = serializer.save()
        logger.info(
            f'Створено новий турнір: "{tournament.title}" (ID: {tournament.id})'
        )

    def perform_destroy(self, instance):
        tournament_title = instance.title
        tournament_id = instance.id
        if instance.teams.exists():
            raise ValidationError(
                f"Неможливо видалити турнір '{tournament_title}', оскільки до нього прив'язано команд: {instance.teams.count()}."
            )
        instance.delete()
        logger.info(
            f'Видалено турнір: "{tournament_title}" (ID: {tournament_id})'
        )


@extend_schema_view(
    list=extend_schema(summary="Отримати список усіх команд"),
    create=extend_schema(summary="Створити нову команду"),
    retrieve=extend_schema(summary="Отримати деталі команди"),
    update=extend_schema(summary="Повністю оновити команду"),
    partial_update=extend_schema(summary="Частково оновити команду"),
    destroy=extend_schema(summary="Видалити команду"),
)
class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_destroy(self, instance):
        if instance.players.exists():
            raise ValidationError(
                f"Неможливо видалити команду '{instance.name}', оскільки в ній зареєстровано гравців: {instance.players.count()}."
            )
        instance.delete()


@extend_schema_view(
    list=extend_schema(summary="Отримати список усіх гравців"),
    create=extend_schema(summary="Створити нового гравця"),
    retrieve=extend_schema(summary="Отримати деталі гравця"),
    update=extend_schema(summary="Повністю оновити гравця"),
    partial_update=extend_schema(summary="Частково оновити гравця"),
    destroy=extend_schema(summary="Видалити гравця"),
)
class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]