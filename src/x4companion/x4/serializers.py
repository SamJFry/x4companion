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


class SectorsSerializer(serializers.ListSerializer):
    """Validate the values of a list of sectors."""

    child = SectorSerializer()

    def create(self, validated_data: list[dict]) -> models.Model:
        """Bulk create Sectors.

        Args:
            validated_data: The validated data to create sectors for.

        Returns:
            The created model.

        """
        return Sector.objects.bulk_create(
            [Sector(**item) for item in validated_data]
        )
