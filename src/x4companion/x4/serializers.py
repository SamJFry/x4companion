"""Module containing all the DRF serializers."""

from typing import ClassVar

from django.contrib.auth.models import User
from django.db import models
from rest_framework import serializers

from x4companion.x4.models import SaveGame, Sector, Station


class SaveGameSerializer(serializers.ModelSerializer):
    """Serialize SaveGames."""

    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model: models.Model = SaveGame
        fields: ClassVar[list[str]] = ["id", "name", "user"]


class SectorSerializer(serializers.ModelSerializer):
    """Validates Sectors values."""

    game_id = SaveGameSerializer

    class Meta:
        model: models.Model = Sector
        fields: ClassVar[list[str]] = ["name", "game_id"]


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
        save = SaveGame.objects.get(id=self.context["game"])
        return Sector.objects.bulk_create(
            [Sector(game=save, name=item["name"]) for item in validated_data]
        )


class StationSerializer(serializers.ModelSerializer):
    game_id = SaveGameSerializer
    sector_id = SectorsSerializer

    class Meta:
        model: models.Model = Station
        fields: ClassVar[list[str]] = [
            "name", "game_id", "sector_id"
        ]