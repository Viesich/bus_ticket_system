from django.urls import path, include

from rest_framework import routers


from station.views import (
    BusViewSet,
    FacilityViewSet,
    TripViewSet,
    OrderViewSet,
    TicketViewSet
)

app_name = "station"

router = routers.DefaultRouter()
router.register("buses", BusViewSet)
router.register("facilities", FacilityViewSet)
router.register("trips", TripViewSet)
router.register("orders", OrderViewSet)
router.register("tickets", TicketViewSet)


urlpatterns = [
    path("", include(router.urls)),
]
