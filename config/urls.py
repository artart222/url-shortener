"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path

from shortener.views import ShortenerURLCreateView
from shortener.views import ShortenerListURLsView
from shortener.views import ShortenerRedirectView
from shortener.views import ShortenerRetrieveURLView

from analytics.views import AnalyticsCodeList, AnalyticsListView

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "api/shortener/url/", ShortenerURLCreateView.as_view()
    ),  # POST endpoint to create short URL
    path(
        "api/shortener/urls/", ShortenerListURLsView.as_view()
    ),  # GET endpoint to list all short URLs
    path(
        "api/analytics/", AnalyticsListView.as_view()
    ),  # GET endpoint to list all analytics records
    path(
        "api/analytics/<str:base62_code>/", AnalyticsCodeList.as_view()
    ),
    path(
        "api/shortener/url/<str:base62_code>/", ShortenerRetrieveURLView.as_view()
    ),  # GET endpoint to get details of a specific short URL
    # Swagger URLs
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
    path("<str:short_code>/", ShortenerRedirectView.as_view()),  # Redirect endpoint
]


""" Summary of API Endpoints:
Done POST /api/shortener/url/ {original_url: ""}                     # create short url
Done GET  /<code>/                        # redirect

Done GET  /api/shortener/urls/                      # list all short urls
Done GET  /api/shortener/url/<code>/               # details for a specific short url

Done GET  /api/analytics/                 # list all analytics records
GET  /api/analytics/<int:id>/        # get specific analytics record # TODO: implement this
"""
