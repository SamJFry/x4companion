"""Module containing all the DRF serializers."""

from typing import ClassVar

from django.db import models
from rest_framework import serializers

from x4companion.x4.models import Sector


class SectorSerializer(serializers.ModelSerializer):
    """Validates Sectors values."""

    class Meta:
        model: models.Model = Sector
        fields: ClassVar[list[str]] = ["name"]
