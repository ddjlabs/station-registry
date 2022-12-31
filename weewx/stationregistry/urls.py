from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'Stations', views.StationsViewSet)
router.register(r'StationEntry', views.StationEntryViewSet)

urlpatterns = [
    path('register.cgi', views.register_cgi, name='register_cgi'),
    path('api/', include(router.urls)),
]
