from rest_framework import serializers
from .models import Country

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = [
            'id',
            'name_common',
            'name_official',
            'cca2',
            'capital',
            'region',
            'subregion',
            'languages',
            'population',
            'timezones',
            'flags_svg',
            'flags_png',
            'latitude',
            'longitude',
        ]

        lookup_field = 'cca2' 