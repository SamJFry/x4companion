"""Module containing all the DRF serializers."""

from django.contrib.auth.models import User
from django.db import models
from rest_framework import serializers

from x4companion.x4.models import SaveGame, Sector, Station


class SaveGameSerializer(serializers.ModelSerializer):
    """Serialize SaveGames."""

    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = SaveGame
        fields = ["id", "name", "user"]


class SectorSerializer(serializers.ModelSerializer):
    """Validates Sectors values."""

    game_id = SaveGameSerializer

    class Meta:
        model = Sector
        fields = ["name", "game_id"]


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
    name = serializers.CharField(max_length=50)
    sector_id = serializers.PrimaryKeyRelatedField(queryset=Sector.objects.all())

    def create(self, validated_data: dict):
        return Station.objects.create(
            name=validated_data["name"],
            sector=validated_data["sector_id"],
            game=SaveGame.objects.get(id=self.context.get("save_id")),
        )


class StationSerializerRead(serializers.ModelSerializer):
    game_id = SaveGameSerializer
    sector_id = SectorSerializer

    class Meta:
        model = Station
        fields = ["id", "name", "sector_id", "game_id", "population"]