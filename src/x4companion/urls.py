"""URL configuration for x4_companion project.

The `urlpatterns` list routes URLs to x4. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/

Examples:
Function x4
    1. Add an import:  from my_app import x4
    2. Add a URL to urlpatterns:  path('', x4.home, name='home')
Class-based x4
    1. Add an import:  from other_app.x4 import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.authtoken import views

from x4companion import x4
from x4companion.x4.dataset import (
    dataset,
    habitat_modules,
    habitats,
    sector_templates,
)
from x4companion.x4.game import saves, sectors, stations

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", x4.index),
    path("api/auth/", views.obtain_auth_token),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("docs/", SpectacularSwaggerView.as_view(), name="swagger"),
    path(
        "game/<int:save_id>/sectors/",
        sectors.Sectors.as_view(),
        name="sectors",
    ),
    path(
        "game/<int:save_id>/sectors/<int:id_>/",
        sectors.SectorView.as_view(),
        name="sector",
    ),
    path("game/", saves.SaveGames.as_view(), name="create_game"),
    path("game/<int:id_>/", saves.SaveGameView.as_view(), name="game"),
    path(
        "game/<int:save_id>/stations/",
        stations.Stations.as_view(),
        name="stations",
    ),
    path(
        "game/<int:save_id>/stations/<int:id_>/",
        stations.StationView.as_view(),
        name="station",
    ),
    path(
        "game/<int:save_id>/stations/<int:station_id>/habitats/",
        habitats.StationHabitats.as_view(),
        name="station_habitats",
    ),
    path(
        "game/<int:save_id>/stations/<int:station_id>/habitats/<int:id_>/",
        habitats.StationHabitatsView.as_view(),
        name="station_habitat",
    ),
    path("dataset/", dataset.Datasets.as_view(), name="datasets"),
    path("dataset/<int:id_>/", dataset.DatasetView.as_view(), name="dataset"),
    path(
        "dataset/<int:dataset_id>/sector-templates/",
        sector_templates.SectorTemplates.as_view(),
        name="sector_templates",
    ),
    path(
        "dataset/<int:dataset_id>/sector-templates/<int:id_>/",
        sector_templates.SectorTemplatesView.as_view(),
        name="sector_template",
    ),
    path(
        "dataset/<int:dataset_id>/habitat-modules/",
        habitat_modules.HabitatModules.as_view(),
        name="habitat_modules",
    ),
    path(
        "dataset/<int:dataset_id>/habitat-modules/<int:id_>/",
        habitat_modules.HabitatModuleView.as_view(),
        name="habitat_module",
    ),
]
