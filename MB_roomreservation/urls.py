"""MB_roomreservation URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from rooms.views import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^home/$', home),
    url(r'^home/delete/(?P<room_id>(\d)+)', del_room),
    url(r'^home/modify/(?P<room_id>(\d)+)', mod_room),
    url(r'^home/details/(?P<room_id>(\d)+)', details),
    url(r'^res_del/(?P<room_id>(\d)+)/(?P<res_day>((\d){4}-(\d){2}-(\d){2}))', res_del),
]
