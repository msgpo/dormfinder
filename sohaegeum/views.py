from rest_framework import permissions
from rest_framework import generics
from django.db.models.expressions import RawSQL
from . import models
from . import serializers


# Create your views here.
class SohaeUserListView(generics.ListCreateAPIView):
    queryset = models.SohaeUser.objects.all()
    serializer_class = serializers.SohaeUserSerializer


class SohaeDormListView(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = serializers.SohaeDormSerializer
    queryset = models.SohaeDorm.objects.filter(is_active=True)


# Create new dorm
class SohaeDormCreateView(generics.CreateAPIView):
    serializer_class = serializers.SohaeDormSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


# View specific dorm info - now with coordinates added!
class SohaeDormInfoView(generics.ListAPIView):
    serializer_class = serializers.SohaeDormSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        """
        This view should return the information for
        the user as determined by the dorm ID portion of the URL.
        """
        dorm_id = self.kwargs['dorm_id']
        # Get latitude and longitude from user
        lat1 = self.kwargs['user_latitude']
        lon1 = self.kwargs['user_longitude']

        return models.SohaeDorm.objects.annotate(
            # Add the distance in KM as an attribute
            distance=RawSQL(
                "SELECT sohae_calculate_distance5(%s, %s, %s) AS distance",
                (lat1, lon1, dorm_id)
            )
        ).filter(id=dorm_id, is_active=True)


# Edit specific dorm info - for admins only
class SohaeDormEditView(generics.UpdateAPIView):
    serializer_class = serializers.SohaeDormSerializer
    permission_classes = (permissions.IsAdminUser,)
    lookup_field = 'id'
    queryset = models.SohaeDorm.objects.all()


# Delete dorm info - for admins only
class SohaeDormDeleteView(generics.UpdateAPIView):
    serializer_class = serializers.SohaeDormSerializer
    permission_classes = (permissions.IsAdminUser,)
    lookup_field = 'id'
    queryset = models.SohaeDorm.objects.all()


# Get nearest dorms within 10km radius
# By default, Sohaegeum app uses KMs instead of miles
class SohaeDormNearbyView(generics.ListAPIView):
    serializer_class = serializers.SohaeDormSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = models.SohaeDorm.objects.filter(is_active=True)

    def get_queryset(self):
        # Get latitude and longitude from user
        lat1 = self.kwargs['user_latitude']
        lon1 = self.kwargs['user_longitude']

        """
        WITHOUT use of any external library,
        using raw PostgreSQL and Haversine Formula
        http://en.wikipedia.org/wiki/Haversine_formula
        """

        """
        STOP! Before running, add the following stored procedure!

        CREATE FUNCTION sohae_calculate_distance5(u_lat float, u_lng float,
            d_id integer) RETURNS float AS $$
        SELECT (6367*acos(cos(radians(u_lat))
               *cos(radians(dorm_latitude))
               *cos(radians(dorm_longitude)
               -radians(u_lng))
               +sin(radians(u_lat))*sin(radians(dorm_latitude))))
               AS distance FROM sohaegeum_sohaedorm WHERE id = d_id
        $$ LANGUAGE SQL;
        """

        return models.SohaeDorm.objects.annotate(
            # Add the distance in KM as an attribute
            distance=RawSQL(
                "SELECT sohae_calculate_distance5(%s, %s, %s) AS distance",
                (lat1, lon1, 1)
            )
        )