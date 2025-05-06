from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q 
from django_filters.rest_framework import DjangoFilterBackend


from .models import Country
from .serializers import CountrySerializer

class CountryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows countries to be viewed or edited.
    Provides standard CRUD, plus search, regional listing, and language listing.
    """
    queryset = Country.objects.all().order_by('name_common') 
    serializer_class = CountrySerializer
    lookup_field = 'cca2' 
    permission_classes = []

    # --- Filtering & Search ---
    filter_backends = [
        DjangoFilterBackend, 
        filters.SearchFilter,
        filters.OrderingFilter
    ]

    filterset_fields = ['region', 'subregion']

    search_fields = ['name_common', 'name_official', 'capital', 'cca2']

    ordering_fields = ['name_common', 'population', 'region']


    @action(detail=True, methods=['get'])
    def regional(self, request, cca2=None):

        try:
            country = self.get_object() 
        except Country.DoesNotExist:
             return Response({"error": "Country not found"}, status=status.HTTP_404_NOT_FOUND)

        if not country.region:
            return Response({"message": "Specified country does not have a region defined."}, status=status.HTTP_200_OK)

        regional_countries = Country.objects.filter(region=country.region).exclude(cca2=country.cca2)
        page = self.paginate_queryset(regional_countries)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(regional_countries, many=True)
        return Response(serializer.data)


    @action(detail=False, methods=['get'], url_path='by_language')
    def by_language(self, request):
        language_name_query = request.query_params.get('language', None)
        if not language_name_query:
            return Response({"error": "Please provide a 'language' query parameter."}, status=status.HTTP_400_BAD_REQUEST)

        
        all_countries_with_languages = Country.objects.filter(languages__isnull=False)

        matching_countries_pks = [] 
        for country in all_countries_with_languages:
            if country.languages: 
                
                if any(lang_val.lower() == language_name_query.lower() for lang_val in country.languages.values()):
                    matching_countries_pks.append(country.pk)

        filtered_queryset = Country.objects.filter(pk__in=matching_countries_pks).order_by('name_common')
        page = self.paginate_queryset(filtered_queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(filtered_queryset, many=True)
        if not serializer.data:
                return Response({"message": f"No countries found speaking '{language_name_query}'"}, status=status.HTTP_200_OK)

        return Response(serializer.data)