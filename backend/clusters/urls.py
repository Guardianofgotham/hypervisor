from django.urls import include, path
from rest_framework.routers import DefaultRouter

from clusters.views import ClusterViewset


router = DefaultRouter()

router.register(r"clusters", ClusterViewset, basename="cluster")

urlpatterns = [path("", include(router.urls))]
