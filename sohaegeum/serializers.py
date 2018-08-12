# -*- coding: utf-8 -*-
from rest_framework import serializers
from . import models


class SohaeUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SohaeUser
        fields = ('email', 'username',)


class SohaeDormSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.SohaeDorm
        fields = ('id', 'dorm_name', 'dorm_type', 'dorm_latitude',
            'dorm_longitude', 'is_active')