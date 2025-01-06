import django_filters
from django.utils import timezone
from reservation.apps.authentication.models import User
from reservation.models import Room


class UserReservationsFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(field_name="username", lookup_expr="icontains")

    has_active_reservations = django_filters.BooleanFilter(method="active_reservations")

    class Meta:
        model = User
        fields = []

    def active_reservations(self, queryset, name, value):
        if value:
            now = timezone.now()
            return queryset.filter(reservation__date_end__gte=now).distinct()
        return queryset


class RoomFilter(django_filters.FilterSet):
    capacity_gte = django_filters.NumberFilter(field_name="capacity", lookup_expr="gte")
    price_gte = django_filters.NumberFilter(field_name="price", lookup_expr="gte")

    class Meta:
        model = Room
        fields = []
