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
        model = SaveGame
        fields: ClassVar[list[str]] = ["id", "name", "user"]


class SectorSerializer(serializers.ModelSerializer):
    """Validates Sectors values."""

    game_id = SaveGameSerializer

    class Meta:
        model = Sector
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


class StationSerializerWrite(serializers.Serializer):
    """The serializer used for stations when createing new ones."""

    name = serializers.CharField(max_length=50)
    sector_id = serializers.PrimaryKeyRelatedField(
        queryset=Sector.objects.all()
    )

    def validate(self, data: dict) -> dict:
        """Performs additional validation.

        Station's name and sector should be unique within the current save
        game. Although the DB should catch this error, it's better to catch it
        here before we attempt to write the data.

        Args:
            data: The data to be validated.

        Returns:
            The Validated data.

        """
        if Station.objects.filter(
            name=data.get("name"),
            sector=data.get("sector_id"),
            game=self.context.get("save_id"),
        ):
            msg = (
                "Station with name and sector already exists. "
                "Stations must be unique."
            )
            raise serializers.ValidationError(msg)
        return data

    def create(self, validated_data: dict) -> models.Model:
        """Create a station from the validated serializer data.

        Since we don't allow creating stations on different save games, all
        stations are created under a save game gleaned from the serializers
        context.

        Args:
            validated_data: The data to create a sector with.
        """
        return Station.objects.create(
            name=validated_data["name"],
            sector=validated_data["sector_id"],
            game=SaveGame.objects.get(id=self.context.get("save_id")),
        )


class StationSerializerRead(serializers.ModelSerializer):
    """The serializer used for reading stations from the DB."""

    game_id = SaveGameSerializer
    sector_id = SectorSerializer

    class Meta:
        model = Station
        fields: ClassVar[list[str]] = [
            "id",
            "name",
            "sector_id",
            "game_id",
            "population",
        ]
