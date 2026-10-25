from django.db import models


class Tournament(models.Model):
    title = models.CharField(max_length=200)
    game = models.CharField(max_length=100)
    status = models.CharField(max_length=50, default="registration")
    organizer_id = models.IntegerField()

    def __str__(self):
        return self.title


class Team(models.Model):
    name = models.CharField(max_length=100)
    tournament = models.ForeignKey(
        Tournament, on_delete=models.CASCADE, related_name="teams"
    )

    def __str__(self):
        return self.name


class Player(models.Model):
    nickname = models.CharField(max_length=100)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="players")

    def __str__(self):
        return self.nickname
