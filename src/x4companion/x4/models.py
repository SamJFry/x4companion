"""This module contains all the Django models for the companion app."""

from django.db import models


class Sector(models.Model):
    """Represents an in game sector.

    Attributes:
        name (str): The name of the sector.

    """

    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return f"Sector {self.name}"
