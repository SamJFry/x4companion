"""Module containing all the DRF serializers."""

from rest_framework import serializers


class SectorSerializer(serializers.Serializer):
    """Validates Sectors values."""

    name = serializers.CharField(max_length=50)
