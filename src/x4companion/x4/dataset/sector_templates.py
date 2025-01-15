"""Contains views for Sector Templates."""

from x4companion.x4.models import SectorTemplate
from x4companion.x4.serializers import SectorTemplateSerializer
from x4companion.x4.views import X4APIBulkView, X4APISingleView


class SectorTemplates(X4APIBulkView):
    """Manage sector templates for a dataset."""

    serializer_class = SectorTemplateSerializer
    model_class = SectorTemplate


class SectorTemplatesView(X4APISingleView):
    """Manage an individual sector template."""

    serializer_class = SectorTemplateSerializer
    model_class = SectorTemplate
