"""Module containing all the DRF serializers."""

from django.contrib.auth.models import User
from django.db import models
from rest_framework import serializers

from x4companion.x4.models import HabitatModule, SaveGame, Sector, Station


class SaveGameSerializer(serializers.ModelSerializer):
    """Serialize SaveGames."""

    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = SaveGame
        fields = ["id", "name", "user"]


class SectorSerializerRead(serializers.ModelSerializer):
    """Validates Sectors values."""

    game_id = serializers.PrimaryKeyRelatedField(
        queryset=SaveGame.objects.all()
    )

    class Meta:
        model = Sector
        fields = ["name", "game_id"]


class SectorSerializerWrite(serializers.Serializer):
    name = serializers.CharField(max_length=50)

    def create(self, validated_data: dict) -> models.Model:
        """Create a sector from the validated serializer data.

        Since we don't allow creating sectors on different save games, all
        sectors are created under a save game gleaned from the serializers
        context.

        Args:
            validated_data: The data to create a sector with.
        """
        return Sector.objects.create(
            name=validated_data["name"],
            game=SaveGame.objects.get(id=self.context.get("game_id")),
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
    sector_id = SectorSerializerRead

    class Meta:
        model = Station
        fields = [
            "id",
            "name",
            "sector_id",
            "game_id",
            "population",
        ]


class HabitatModuleSerializer(serializers.ModelSerializer):
    """The serializer used for Habitat Modules."""

    class Meta:
        model = HabitatModule
        fields = ["name", "capacity", "species"]
