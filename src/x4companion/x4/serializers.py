"""Module containing all the DRF serializers."""

from django.contrib.auth.models import User
from django.db import models
from rest_framework import serializers

from x4companion.x4.models import (
    Dataset,
    Habitat,
    HabitatModule,
    SaveGame,
    Sector,
    SectorTemplate,
    Station,
    Ware,
    FactoryModule,
)


class DatasetSerializer(serializers.ModelSerializer):
    """Serialize Datasets."""

    class Meta:
        model = Dataset
        fields = ["id", "name"]


class SaveGameSerializer(serializers.ModelSerializer):
    """Serialize SaveGames."""

    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    dataset_id = serializers.PrimaryKeyRelatedField(
        queryset=Dataset.objects.all()
    )

    class Meta:
        model = SaveGame
        fields = ["id", "name", "user", "dataset_id"]

    def create(self, validated_data: dict) -> models.Model:
        """Create a save game from the validated data.

        Args:
            validated_data: The data that has been validated by the
                serializer.

        Returns:
            A model instance of the created object.

        """
        return SaveGame.objects.create(
            name=validated_data["name"],
            user=validated_data["user"],
            dataset=validated_data["dataset_id"],
        )


class SectorSerializerRead(serializers.ModelSerializer):
    """Validates Sectors values."""

    template_id = serializers.PrimaryKeyRelatedField(
        queryset=SectorTemplate.objects.all()
    )
    game_id = serializers.PrimaryKeyRelatedField(
        queryset=SaveGame.objects.all()
    )

    class Meta:
        model = Sector
        fields = ["id", "template_id", "game_id"]


class SectorTemplateSerializer(serializers.ModelSerializer):
    """Serializer class used for Sector Templates."""

    class Meta:
        model = SectorTemplate
        fields = ["id", "name", "sunlight_percent"]

    def create(self, validated_data: dict) -> models.Model:
        """Creates a sector template from validated data.

        Args:
            validated_data: The data from the serializer.

        Returns:
            A new SectorTemplate instance.

        """
        return SectorTemplate.objects.create(
            name=validated_data["name"],
            dataset_id=self.context["dataset_id"],
            sunlight_percent=validated_data["sunlight_percent"],
        )


class WareSerializer(serializers.Serializer):
    """Serializer class used for Wares."""

    id = serializers.ModelField(
        model_field=Ware()._meta.get_field("id"),  # noqa: SLF001
        required=False,
    )
    name = serializers.CharField(
        max_length=50, allow_blank=False, allow_null=False
    )
    storage = serializers.CharField(allow_blank=False, allow_null=False)

    def validate_storage(self, value: str) -> str:
        """Validates that a proper storage type has been provided.

        Valid storage types are defined by the `Ware` model and must be
        provided as the human-readable form.

        Args:
            value: The storage vale to be verified.

        Returns:
            The single character version of the storage mode that can be
            written to the DB.

        """
        if value not in (choices := Ware.STORAGE_TYPES.values()):
            msg = f"{value} is not a valid storage type, Choices are {choices}"
            raise serializers.ValidationError(msg)
        return next(
            key for key, val in Ware.STORAGE_TYPES.items() if val == value
        )

    def to_representation(self, instance: models.Model) -> dict:
        """Converts the storage value to a human-readable form.

        Args:
            instance: The model instance to use.

        Returns:
            The serialized data to be returned in the API response.

        """
        data = super().to_representation(instance)
        data["storage"] = Ware.STORAGE_TYPES[data["storage"]]
        return data

    def create(self, validated_data: dict) -> models.Model:
        """Creates a ware from validated data.

        Args:
            validated_data: The data from the serializer.

        Returns:
            A new SectorTemplate instance.

        """
        return Ware.objects.create(
            name=validated_data["name"],
            dataset_id=self.context["dataset_id"],
            storage=validated_data["storage"],
        )


class SectorSerializerWrite(serializers.Serializer):
    """Serializer class used to create sectors."""

    template_id = serializers.PrimaryKeyRelatedField(
        queryset=SectorTemplate.objects.all()
    )

    def create(self, validated_data: dict) -> models.Model:
        """Create a sector from the validated serializer data.

        Since we don't allow creating sectors on different save games, all
        sectors are created under a save game gleaned from the serializers
        context.

        Args:
            validated_data: The data to create a sector with.
        """
        return Sector.objects.create(
            template=validated_data["template_id"],
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


class FactoryModuleSerializer(serializers.ModelSerializer):
    """The serializer used for Factory Modules."""

    ware_id = serializers.PrimaryKeyRelatedField(
        queryset=Ware.objects.all()
    )

    class Meta:
        model = FactoryModule
        fields = ["id", "name", "ware_id", "hourly_production", "hourly_energy", "workforce"]

    def create(self, validated_data: dict) -> models.Model:
        """Create a Factory Module from the validated serializer data.

        Since we don't allow creating modules on different Datasets, all
        modules are created under a dataset gleaned from the serializers
        context.

        Args:
            validated_data: The data to create a sector with.

        """
        validated_data["ware"] = validated_data.pop("ware_id")
        return FactoryModule.objects.create(
            **validated_data,
            dataset=Dataset.objects.get(id=self.context.get("dataset_id")),
        )


class HabitatModuleSerializer(serializers.ModelSerializer):
    """The serializer used for Habitat Modules."""

    class Meta:
        model = HabitatModule
        fields = ["id", "name", "capacity", "species"]

    def create(self, validated_data: dict) -> models.Model:
        """Create a Habitat Module from the validated serializer data.

        Since we don't allow creating modules on different Datasets, all
        modules are created under a dataset gleaned from the serializers
        context.

        Args:
            validated_data: The data to create a sector with.

        """
        return HabitatModule.objects.create(
            **validated_data,
            dataset=Dataset.objects.get(id=self.context.get("dataset_id")),
        )


class HabitatSerializer(serializers.ModelSerializer):
    """The serializer for station Habitats."""

    module_id = serializers.PrimaryKeyRelatedField(
        queryset=HabitatModule.objects.all()
    )
    station_id = StationSerializerRead

    class Meta:
        model = Habitat
        fields = ["id", "count", "module_id", "station_id"]

    def create(self, validated_data: dict) -> models.Model:
        """Create a station Habitat from validated serial data.

        The ID of the station to create modules for is retrieved from the
        context.

        Args:
            validated_data: The data to create a sector with.

        """
        return Habitat.objects.create(
            module=validated_data["module_id"],
            station=Station.objects.get(id=self.context.get("station_id")),
            count=validated_data["count"],
        )
