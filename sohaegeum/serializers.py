# -*- coding: utf-8 -*-
from rest_framework import serializers
from . import models


class SohaeUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SohaeUser
        fields = ('email', 'username',)


class SohaeDormSerializer(serializers.ModelSerializer):
    distance = serializers.DecimalField(max_digits=9, decimal_places=6)

    class Meta:
        model = models.SohaeDorm
        fields = ('id', 'dorm_name', 'dorm_type', 'dorm_latitude',
            'dorm_longitude', 'is_active', 'distance')