# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.urls import include, path
from rest_framework.authtoken import views as rest_framework_views

# Note to self - change the rest-auth to something else for security
urlpatterns = [
    path('sohaegeum/', include('sohaegeum.urls')),
    path('rest-auth/', include('rest_auth.urls')),
    url(r'^get_auth_token/$', rest_framework_views.obtain_auth_token,
        name='get_auth_token'),
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),
]