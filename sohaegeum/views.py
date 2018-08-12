from rest_framework import permissions
from rest_framework import generics
from . import models
from . import serializers


# Create your views here.
class SohaeUserListView(generics.ListCreateAPIView):
    queryset = models.SohaeUser.objects.all()
    serializer_class = serializers.SohaeUserSerializer


class SohaeDormListView(generics.ListAPIView):
    queryset = models.SohaeDorm.objects.filter(is_active=True)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = serializers.SohaeDormSerializer


# Create new dorm - for admins only
class SohaeDormCreateView(generics.CreateAPIView):
    serializer_class = serializers.SohaeDormSerializer
    permission_classes = (permissions.IsAdminUser,)


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