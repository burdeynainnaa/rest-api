from django.contrib.auth.models import User
from django.urls import reverse
import pytest
from rest_framework import status
from tournaments.models import Tournament


@pytest.mark.django_db
def test_get_tournament_list(api_client):
  Tournament.objects.create(
      title="Kyiv Cyber Cup", game="CS2", status="registration", organizer_id=1
  )
  response = api_client.get("/api/tournaments/", format="json")
  assert response.status_code == status.HTTP_200_OK
  assert len(response.data) == 1


@pytest.mark.django_db
def test_create_tournament_authenticated(api_client, user):
  login_url = reverse("token_obtain_pair")
  tokens = api_client.post(
      login_url,
      {"username": "adminuser", "password": "1234"},
      format="json",
  ).data

  api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {tokens["access"]}')
  response = api_client.post(
      "/api/tournaments/",
      {
          "title": "Dota 2 Open",
          "game": "Dota 2",
          "status": "registration",
          "organizer_id": user.id,
      },
      format="json",
  )
  assert response.status_code == status.HTTP_201_CREATED
  assert response.data["title"] == "Dota 2 Open"


@pytest.mark.django_db
def test_create_tournament_invalid_data(api_client, user):
  login_url = reverse("token_obtain_pair")
  tokens = api_client.post(
      login_url,
      {"username": "adminuser", "password": "1234"},
      format="json",
  ).data

  api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {tokens["access"]}')
  response = api_client.post(
      "/api/tournaments/",
      {
          "title": "",
          "game": "CS2",
          "status": "registration",
          "organizer_id": user.id,
      },
      format="json",
  )
  assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_create_tournament_no_auth(api_client):
  response = api_client.post(
      "/api/tournaments/",
      {
          "title": "Unauthorized Cup",
          "game": "CS2",
          "status": "registration",
          "organizer_id": 1,
      },
      format="json",
  )
  assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_delete_nonexistent_tournament(api_client, user):
  login_url = reverse("token_obtain_pair")
  tokens = api_client.post(
      login_url,
      {"username": "adminuser", "password": "1234"},
      format="json",
  ).data

  api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {tokens["access"]}')
  response = api_client.delete("/api/tournaments/9999/", format="json")
  assert response.status_code == status.HTTP_404_NOT_FOUND