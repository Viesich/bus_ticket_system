from rest_framework import serializers
from station.models import Bus, Facility, Trip, Order, Ticket


class FacilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Facility
        fields = ("id", "name")


class BusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bus
        fields = ("id", "info", "num_seats", "is_small", "facilities",)


class BusListSerializer(BusSerializer):
    facilities = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="name",
    )


class BusRetrieveSerializer(BusSerializer):
    facilities = FacilitySerializer(many=True)


class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = (
            "id",
            "source",
            "destination",
            "departure",
            "bus"
        )


class TripRetrieveSerializer(TripSerializer):
    bus = BusRetrieveSerializer(many=False, read_only=True)


class TripListSerializer(serializers.ModelSerializer):
    bus_info = serializers.CharField(source="bus.info", read_only=True)
    bus_num_seats = serializers.IntegerField(source="bus.num_seats", read_only=True)

    class Meta:
        model = Trip
        fields = (
            "id",
            "source",
            "destination",
            "departure",
            "bus_info",
            "bus_num_seats"
        )


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ("id", "seat", "trip",)


class OrderSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True, read_only=False)

    class Meta:
        model = Order
        fields = ("id", "created_at", "tickets")

    def create(self, validated_data):
        print("Received data for order creation:", validated_data)
        tickets_data = validated_data.pop("tickets")
        order = Order.objects.create(**validated_data)
        for ticket_data in tickets_data:
            Ticket.objects.create(order=order, **ticket_data)
        return order

    def get_tickets(self, obj):
        return ((f"{ticket.trip.departure.strftime('%Y-%m-%d %H:%M')} "
                 f"Bus: {ticket.trip.bus} {ticket.trip.destination} - {ticket.trip.source} (Seat: {ticket.seat})")
                for ticket in obj.tickets.all())
