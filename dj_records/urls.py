"""dj_records URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from app01 import views

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'reg/$', views.reg),
    re_path(r'login/$', views.login),
    re_path(r'logout/$', views.logout),
    re_path(r'records/$', views.records),
    re_path(r'records/add/', views.record_add),
    re_path(r'records/(\d+)/delete/', views.record_delete),
    re_path(r'records/(\d+)/edit/', views.record_edit),

    re_path(r'periods/$', views.periods),
    re_path(r'periods/add/', views.period_add),
    re_path(r'periods/(\d+)/delete/', views.period_delete),
    re_path(r'periods/(\d+)/edit/', views.period_edit),

    re_path(r'engineers/$', views.engineers),
    re_path(r'engineers/add/', views.engineer_add),
    re_path(r'engineers/(\d+)/delete/', views.engineer_delete),
    re_path(r'engineers/(\d+)/edit/', views.engineer_edit),

    re_path(r'orders/$', views.orders),
    re_path(r'orders/add/$',views.add_order),

    re_path(r'^$', views.login),
]
