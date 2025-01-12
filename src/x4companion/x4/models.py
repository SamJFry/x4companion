"""This module contains all the Django models for the companion app."""

from django.contrib.auth.models import User
from django.db import models


class Dataset(models.Model):
    """Links a set of resources to be loaded into the app.

    This model is referenced by template classes like HabitatModule or
    FactoryModule. A Dataset is used to present a filtered view of templates,
    so that only the content that is relevant to a SaveGame is accessible.

    Attributes:
        name (str): The name of the Dataset.

    """

    name = models.CharField(
        max_length=50, blank=False, null=False, unique=True
    )

    def __str__(self) -> str:
        return f"Dataset {self.name}"


class SaveGame(models.Model):
    """The overarching save game that's being modeled.

    Attributes:
        name (str): The name of the save game.
        user (models.Model): The owner of the save game.

    """

    name = models.CharField(max_length=50, blank=False, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"SaveGame {self.name}"


class SectorTemplate(models.Model):
    """Represents an in game sector.

    Attributes:
        name (str): The name of the sector.
        dataset (Dataset): The Dataset this sector belongs to.
        sunlight_percent (int): The sunlight intensity in this sector.

    """

    name = models.CharField(
        max_length=50, unique=True, blank=False, null=False
    )
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE)
    sunlight_percent = models.IntegerField(blank=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["name", "dataset"], name="No duplicate sectors"
            )
        ]

    def __str__(self) -> str:
        return f"Sector {self.name}"


class Sector(models.Model):
    """Represents an instance of a sector in a users save game.

    Attributes:
        name (str): The name of the sector.
        game (SaveGame): The save game this sector belongs to.

    """

    template = models.ForeignKey(SectorTemplate, on_delete=models.CASCADE)
    game = models.ForeignKey(SaveGame, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["template", "game"],
                name="No duplicate sector templates",
            )
        ]

    def __str__(self) -> str:
        return f"Sector {self.template.name}"


class Station(models.Model):
    """Represents an in game station.

    Attributes:
        name (str): The name of the station.
        population (int): The stations population, defaults to 0.
        sector (Sector): The sector the station is in.
        game (SaveGame): The save game the station belongs to.

    """

    name = models.CharField(max_length=50, blank=False, null=False)
    game = models.ForeignKey(SaveGame, on_delete=models.CASCADE)
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE)
    population = models.IntegerField(default=0, null=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["name", "game"], name="No duplicate stations"
            )
        ]

    def __str__(self) -> str:
        return f"Station {self.name}"

    def calculate_population(self) -> None:
        """Recalculate the maximum population of a station."""
        modules = Habitat.objects.filter(station=self)
        self.population = sum(
            [mod.count * mod.module.capacity for mod in modules]
        )
        self.save()


class HabitatModule(models.Model):
    """Represents a habitat module that can be attached to stations.

    Attributes:
        name: The name of the template.
        capacity: The capacity of the habitat module.
        species: The species that can use the habitat.

    """

    name = models.CharField(max_length=50, blank=False, null=False)
    capacity = models.IntegerField(null=False)
    species = models.CharField(max_length=50, blank=False, null=False)
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["name", "capacity", "species"], name="Global unique"
            )
        ]

    def __str__(self) -> str:
        return f"Habitat {self.name}"


class Habitat(models.Model):
    """Represents an instance of habitat modules connected to a station.

    Attributes:
        count: The number of modules connected to the station.
        module: The habitat module that contains the habitats attributes.
        station: The station these modules are attached to.

    """

    count = models.IntegerField(null=False)
    module = models.ForeignKey(HabitatModule, on_delete=models.CASCADE)
    station = models.ForeignKey(Station, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["module", "station"], name="Unique Habitats"
            )
        ]

    def __str__(self) -> str:
        return f"Habitats {self.station.name} Station {self.module.name}"

    def save(self, *args, **kwargs) -> None:
        """Overridden save method to ensure clean is called."""
        self.clean()
        return super().save(*args, **kwargs)

    def clean(self) -> None:
        """Custom clean to calculate new station population."""
        self.station.calculate_population()


class Ware(models.Model):
    """Represents an in game ware such as hull parts.

    Attributes:
        name: The name of the ware.
        storage: The type of storage the ware uses, either C, L or S.
        dataset: The dataset the ware belongs to.

    """

    STORAGE_TYPES = {
        "C": "Container",
        "L": "Liquid",
        "S": "Solid",
    }
    name = models.CharField(
        max_length=50, blank=False, null=False, unique=True
    )
    storage = models.CharField(
        choices=STORAGE_TYPES, null=False, blank=False, max_length=1
    )
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"Ware {self.name}"


class FactoryModule(models.Model):
    """Represents a factory module that can be attached to stations.

    Attributes:
        name: The name of the template.
        ware: The ware the factory produces.
        hourly_production: The hourly production rate of the ware.
        hourly_energy: The quantity of energy cells the factory consumes each
            hour.
        dataset: The dataset the factory belongs to.
        workforce: The required workforce to operate the module.

    """

    name = models.CharField(
        max_length=50, blank=False, null=False, unique=True
    )
    ware = models.ForeignKey(Ware, on_delete=models.CASCADE)
    hourly_production = models.IntegerField(null=False)
    hourly_energy = models.IntegerField(null=False)
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE)
    workforce = models.IntegerField(null=False)

    def __str__(self) -> str:
        return f"Factory Module {self.ware.name}"


class Factory(models.Model):
    """Represents an instance of factory modules connected to a station.

    Attributes:
        count: The number of modules connected to the station.
        module: The habitat module that contains the habitats attributes.
        station: The station these modules are attached to.

    """

    count = models.IntegerField(null=False)
    module = models.ForeignKey(FactoryModule, on_delete=models.CASCADE)
    station = models.ForeignKey(Station, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["module", "station"], name="Unique Factory"
            )
        ]

    def __str__(self) -> str:
        return f"{self.module.ware.name} Factories {self.station.name}"


class WareOrder(models.Model):
    """A ware order requested from a factory.

    A factory will have one or more orders attached to it. These define the
    resources a factory needs to operate each hour.

    Attributes:
        ware: The ware being consumed.
        quantity: The quantity of the order
        factory: The factory module the order is attached to.

    """

    ware = models.ForeignKey(Ware, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=False)
    factory = models.ForeignKey(FactoryModule, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"Ware Order {self.ware.name}"
