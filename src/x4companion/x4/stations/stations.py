"""Contains API views relating to Stations."""

from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response


class Stations(GenericAPIView):
    """Manage multiple stations."""