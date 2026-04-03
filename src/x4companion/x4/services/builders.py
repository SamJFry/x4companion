"""Builder classes for producing DB objects."""

from typing import NotRequired, TypedDict

from django.db import models, transaction

from x4companion.x4.models import (
    Factory,
    FactoryModule,
    Habitat,
    HabitatModule,
    Station,
)


class ModuleCount(TypedDict):
    """A set of modules attached to a station."""

    count: int
    id: int


class StationPayload(TypedDict):
    """Defines what a station payload looks like."""

    name: str
    sector_id: int
    habitats: NotRequired[ModuleCount]
    factories: NotRequired[ModuleCount]


class StationBuilder:
    """Create stations."""

    def __init__(self) -> None:
        """Initialise the builder."""
        self.current_station: Station | None = None
        self.built_instances: list[Station] = []

    def _add_station_module(
        self,
        mtype: type[models.Model],
        mdata: list[ModuleCount],
        parent_module: type[models.Model],
    ) -> None:
        """Add a set of modules to a station."""
        for module in mdata:
            parent = parent_module.objects.get(id=module["id"])
            mtype.objects.create(
                count=module["count"], module=parent, station=self.current_station
            )

    @transaction.atomic
    def create(self, data: StationPayload, save_id: int) -> None:
        """Create a single station instance."""
        station = Station.objects.create(
            name=data["name"], game_id=save_id, sector_id=data["sector_id"]
        )
        self.current_station = station
        if habitats := data.get("habitats"):
            self._add_station_module(
                mtype=Habitat, mdata=habitats, parent_module=HabitatModule
            )
        if factories := data.get("factories"):
            self._add_station_module(
                mtype=Factory, mdata=factories, parent_module=FactoryModule
            )
        self.built_instances.append(station)
        return station
