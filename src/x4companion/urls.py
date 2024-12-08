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

from x4companion import x4

urlpatterns = [path("admin/", admin.site.urls), path("", x4.index)]
