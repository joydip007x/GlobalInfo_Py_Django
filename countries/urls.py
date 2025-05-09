from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CountryViewSet

router = DefaultRouter()
router.register(r'countries', CountryViewSet, basename='country') 

urlpatterns = [
    path('', include(router.urls)),
    # path('', CountryListView.as_view(), name='country_list'),
    # path('country/<slug:cca2>/', CountryDetailView.as_view(), name='country_detail'),
]