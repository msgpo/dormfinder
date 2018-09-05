# -*- coding: utf-8 -*-
from django.urls import path

from . import views

urlpatterns = [
    path('', views.SohaeUserListView.as_view()),
    path('dorms/', views.SohaeDormListView.as_view()),
    path('dorms/create/', views.SohaeDormCreateView.as_view()),
    path('dorms/info/<int:dorm_id>/<user_latitude>/<user_longitude>/',
        views.SohaeDormInfoView.as_view()),
    path('dorms/edit/<int:id>/', views.SohaeDormEditView.as_view()),
    path('dorms/delete/<int:id>/', views.SohaeDormDeleteView.as_view()),
    path('dorms/nearby/<user_latitude>/<user_longitude>',
        views.SohaeDormNearbyView.as_view()),
]
