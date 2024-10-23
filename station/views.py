from rest_framework import viewsets

from station.models import Bus, Trip, Order, Ticket, Facility
from station.serializers import (
    BusSerializer,
    TripSerializer,
    TripListSerializer,
    OrderSerializer,
    TicketSerializer,
    FacilitySerializer, BusListSerializer, BusRetrieveSerializer, TripRetrieveSerializer
)

from user.models import User


class BusViewSet(viewsets.ModelViewSet):
    queryset = Bus.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return BusListSerializer
        elif self.action == "retrieve":
            return BusRetrieveSerializer
        return BusSerializer

    def get_queryset(self):
        queryset = Bus.objects.all()
        if self.action in ("list", "retrieve"):
            return queryset.prefetch_related("facilities")
        return queryset


class FacilityViewSet(viewsets.ModelViewSet):
    queryset = Facility.objects.all()
    serializer_class = FacilitySerializer


class TripViewSet(viewsets.ModelViewSet):
    queryset = Trip.objects.all().select_related()

    def get_serializer_class(self):
        if self.action == "list":
            return TripListSerializer
        elif self.action == "retrieve":
            return TripRetrieveSerializer
        return TripSerializer

    def get_queryset(self):
        queryset = Trip.objects.all()
        if self.action == ("list", "retrieve"):
            return queryset.select_related()
        return queryset


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
