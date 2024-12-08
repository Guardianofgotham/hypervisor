from rest_framework.routers import DefaultRouter
from .views import DeploymentViewset
from django.urls import path, include

router = DefaultRouter()

router.register(r"deployments", DeploymentViewset, basename="deployment")

urlpatterns = [path("", include(router.urls))]
