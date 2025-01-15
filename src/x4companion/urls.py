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
from x4companion.x4.views import dataset
from x4companion.x4.game import factory, habitats, saves, sectors, stations

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", x4.index),
    path("api/auth/", views.obtain_auth_token),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("docs/", SpectacularSwaggerView.as_view(), name="swagger"),
    path(
        "game/<int:game_id>/sectors/",
        sectors.Sectors.as_view(),
        name="sectors",
    ),
    path(
        "game/<int:game__id>/sectors/<int:id>/",
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
        "game/<int:game__id>/stations/<int:id>/",
        stations.StationView.as_view(),
        name="station",
    ),
    path(
        "game/<int:save_id>/stations/<int:station_id>/factories/",
        factory.StationFactories.as_view(),
        name="station_habitats",
    ),
    path(
        "game/<int:station__game__id>/stations/<int:station__id>/factories/<int:id>/",
        factory.StationFactoriesView.as_view(),
        name="station_habitat",
    ),
    path(
        "game/<int:save_id>/stations/<int:station_id>/habitats/",
        habitats.StationHabitats.as_view(),
        name="station_habitats",
    ),
    path(
        "game/<int:station__game__id>/stations/<int:station_id>/habitats/<int:id>/",
        habitats.StationHabitatsView.as_view(),
        name="station_habitat",
    ),
    path("dataset/", dataset.Datasets.as_view(), name="datasets"),
    path("dataset/<int:id>/", dataset.DatasetView.as_view(), name="dataset"),
    path(
        "dataset/<int:dataset_id>/sector-templates/",
        dataset.SectorTemplates.as_view(),
        name="sector_templates",
    ),
    path(
        "dataset/<int:dataset_id>/sector-templates/<int:id>/",
        dataset.SectorTemplatesView.as_view(),
        name="sector_template",
    ),
    path(
        "dataset/<int:dataset_id>/habitat-modules/",
        dataset.HabitatModules.as_view(),
        name="habitat_modules",
    ),
    path(
        "dataset/<int:dataset_id>/habitat-modules/<int:id>/",
        dataset.HabitatModuleView.as_view(),
        name="habitat_module",
    ),
    path(
        "dataset/<int:dataset_id>/factory-modules/",
        dataset.FactoryModules.as_view(),
        name="habitat_modules",
    ),
    path(
        "dataset/<int:dataset_id>/factory-modules/<int:id>/",
        dataset.FactoryModuleView.as_view(),
        name="habitat_module",
    ),
    path(
        "dataset/<int:dataset_id>/wares/",
        dataset.Wares.as_view(),
        name="wares",
    ),
    path(
        "dataset/<int:dataset_id>/wares/<int:id>/",
        dataset.WareView.as_view(),
        name="ware",
    ),
    path(
        "dataset/<int:ware__dataset>/ware-orders/",
        dataset.WareOrders.as_view(),
        name="ware_orders",
    ),
    path(
        "dataset/<int:ware__dataset>/ware-orders/<int:id>/",
        dataset.WareOrderView.as_view(),
        name="ware_order",
    ),
]
