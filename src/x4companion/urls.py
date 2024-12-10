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

from x4companion import x4
from x4companion.x4 import sectors

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", x4.index),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("docs/", SpectacularSwaggerView.as_view(), name="swagger"),
    path("game/<int:save_id>/sectors/", sectors.Sectors.as_view(), name="sectors"),
    path("game/<int:save_id>/sectors/<int:id_>/", sectors.SectorView.as_view(), name="sector"),
]
