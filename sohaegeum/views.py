from rest_framework import permissions
from rest_framework import generics
from django.db.models import FloatField, ExpressionWrapper, F, Func, Value
from django.db.models.expressions import RawSQL
from decimal import Decimal
from math import cos, sin, asin, sqrt
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


# View specific dorm info
class SohaeDormInfoView(generics.ListAPIView):
    serializer_class = serializers.SohaeDormSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        """
        This view should return the information for
        the user as determined by the dorm ID portion of the URL.
        """
        dorm_id = self.kwargs['dorm_id']
        return models.SohaeDorm.objects.filter(id=dorm_id, is_active=True)


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
        lat1 = self.kwargs['user_latitude']
        lon1 = self.kwargs['user_longitude']
        lat2 = F('dorm_latitude')
        lon2 = F('dorm_longitude')

        template = '%(function)s(%(expressions)s AS FLOAT)'
        fv1 = Func(lat2, function='CAST', template=template)
        fv2 = Func(lon2, function='CAST', template=template)
        dlat = fv1 - lat1
        dlon = fv2 - lon1

        """
        WITHOUT use of any external library,
        using raw PostgreSQL and Haversine Formula
        http://en.wikipedia.org/wiki/Haversine_formula
        """
        radius = 10000.0 / 1000.0

        query = """SELECT (6367*acos(cos(radians({0}))
            *cos(radians(dorm_latitude))
            *cos(radians(dorm_longitude)-radians({1}))
            +sin(radians({2}))*sin(radians(dorm_latitude))))
            AS distance
            FROM sohaegeum_sohaedorm""".format(float(lat1), float(lon1), float(lat1), radius)
        params = (float(lat1), float(lon1), float(lat1), radius,)

        return models.SohaeDorm.objects.annotate(
            #distance=c * r
            distance=RawSQL(
                """SELECT (6367*acos(cos(radians(%s))
                *cos(radians(F('dorm_latitude')))
                *cos(radians(F('dorm_longitude'))-radians(%s))
                +sin(radians(%s))*sin(radians(F('dorm_latitude')))))
                AS distance
                FROM sohaegeum_sohaedorm""",
                params)
        )