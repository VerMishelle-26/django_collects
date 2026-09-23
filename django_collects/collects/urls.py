from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CollectViewSet, PaymentViewSet

router = DefaultRouter()
router.register("collects", CollectViewSet, basename="collect")
router.register("payments", PaymentViewSet, basename="payment")

urlpatterns = [
    path("", include(router.urls)),
]