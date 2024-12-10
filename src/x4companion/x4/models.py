"""This module contains all the Django models for the companion app."""

from django.contrib.auth.models import User
from django.db import models


class SaveGame(models.Model):
    """The overarching save game that's being modeled.

    Attributes:
        name (str): The name of the save game.
        user (models.Model): The owner of the save game.

    """

    name = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"SaveGame {self.name}"


class Sector(models.Model):
    """Represents an in game sector.

    Attributes:
        name (str): The name of the sector.
        game (SaveGame): The save game this sector belongs to.

    """

    name = models.CharField(max_length=50, unique=True)
    game = models.ForeignKey(SaveGame, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"Sector {self.name}"
