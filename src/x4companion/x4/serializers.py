"""Module containing all the DRF serializers."""

from typing import ClassVar

from django.db import models
from rest_framework import serializers

from x4companion.x4.models import Sector, SaveGame


class SaveGameSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model: models.Model = SaveGame
        fields: ClassVar[list[str]] = ["name", "user"]


class SectorSerializer(serializers.ModelSerializer):
    """Validates Sectors values."""
    game = SaveGameSerializer

    class Meta:
        model: models.Model = Sector
        fields: ClassVar[list[str]] = ["name", "game"]


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
        save = SaveGame.objects.get(id=validated_data[0]["game"])
        return Sector.objects.bulk_create(
            [Sector(game=save, name=item["name"]) for item in validated_data]
        )
