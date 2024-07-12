# This work is licensed under a Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License.
# https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
]
