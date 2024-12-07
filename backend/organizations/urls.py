from rest_framework.routers import DefaultRouter

from organizations.views import OrganizationViewSet
from django.urls import path, include

router = DefaultRouter()

router.register(r"organizations", OrganizationViewSet, basename="organization")

urlpatterns = [path("", include(router.urls))]
