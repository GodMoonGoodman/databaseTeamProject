"""VMS URL Configuration

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
from django.conf.urls import url, include
from django.conf import settings
from django.contrib import admin
from Monitor import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/', views.LogIn),
    url(r'^logout/', views.Logout),
    url(r'^main/', views.Main),
    url(r'^manage_admin/', views.Manage_admin),
    url(r'^manage_admin_delete/(?P<pk>\d+)', views.Manage_admin_delete),
    url(r'^manage_admin_cctv/(?P<pk>\d+)', views.Manage_admin_cctv),
    url(r'^manage_cctv/', views.Manage_cctv),
    url(r'^manage_cctv_alloc/(?P<pk>\d+)', views.Manage_cctv_alloc),
    url(r'^manage_cctv_add/', views.Manage_cctv_add),
    url(r'^manage_cctv_delete/(?P<pk>\d+)', views.Manage_cctv_delete),
    url(r'^manage_area_modify/(?P<pk>\d+)', views.Manage_area_modify),


    url(r'^manage_area/', views.Manage_area),
    url(r'^manage_area_delete/(?P<pk>\d+)', views.Manage_area_delete),

    url(r'^manage_neighbor/', views.Manage_neighbor),
    url(r'^manage_neighbor_delete/(?P<pk>\d+)', views.Manage_neighbor_delete),
    url(r'^manage_neighbor_map/(?P<pk>\d+)', views.Manage_neighbor_map),
    url(r'^manage_neighbor_innermap/(?P<pk>\d+)', views.Manage_neighbor_innermap),


    url(r'^manage_sequence/', views.Manage_sequence),
    url(r'^manage_sequence_append/(?P<pk>\d+)', views.Manage_sequence_append),
    url(r'^manage_sequence_del/(?P<pk>\d+)', views.Manage_sequence_del),
    url(r'^manage_sequence_remove/(?P<pk>\d+)', views.Manage_sequence_remove),
    url(r'^manage_sequence_map/(?P<pk>\d+)', views.Manage_sequence_map),
    url(r'^manage_sequence_mapview/(?P<pk>\d+)', views.Manage_sequence_mapview),

    url(r'^admin_cctv_area_alloc/(?P<pk>\d+)', views.Admin_cctv_area_alloc),
    url(r'^admin_cctv_area_alloc_append/', views.Admin_cctv_area_alloc_append),
    url(r'^admin_video/', views.Admin_video),
    url(r'^video_view/(?P<pk>\d+)', views.Video_view),
    url(r'^admin_cctv/', views.Admin_cctv),
    url(r'^map/', views.Map),
    url(r'^my/', views.My),

    url(r'^my/video_search', views.Video_search),

    url(r'^search/', views.Search),
    
    url(r'^statistic_download/(?P<pk>\d+)', views.Statistic_download),

    url(r'^manage_videos/', views.Manage_videos),


]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns