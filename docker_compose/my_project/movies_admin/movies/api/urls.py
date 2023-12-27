"""Declarating of routing in API."""

from django.urls import include, path

urlpatterns = [
    path('v1/', include('movies.api.v1.urls')),
]
