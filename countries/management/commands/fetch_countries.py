import requests
from django.core.management.base import BaseCommand
from django.conf import settings 
from countries.models import Country
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

API_URL = "https://restcountries.com/v3.1/all"

class Command(BaseCommand):

    def handle(self, *args, **options):
        logger.info("Starting country data fetch...")

        try:
            response = requests.get(API_URL, timeout=30) 
            response.raise_for_status()
            data = response.json()
            logger.info(f"Successfully fetched data for {len(data)} countries.")

        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching data from API: {e}")
            self.stderr.write(self.style.ERROR(f"API request failed: {e}"))
            return 

        except ValueError as e: 
             logger.error(f"Error decoding JSON response: {e}")
             self.stderr.write(self.style.ERROR(f"JSON decoding failed: {e}"))
             return

        countries_created_count = 0
        countries_updated_count = 0

        for country_data in data:

            cca2 = country_data.get('cca2')
            if not cca2:
                logger.warning(f"Skipping entry due to missing 'cca2': {country_data.get('name', {}).get('common', 'N/A')}")
                continue 

            name_common = country_data.get('name', {}).get('common', '')
            name_official = country_data.get('name', {}).get('official', '')

            
            capitals = country_data.get('capital', [])
            capital_str = capitals[0] if capitals else None

            region = country_data.get('region', '')
            subregion = country_data.get('subregion')
            languages = country_data.get('languages') 
            population = country_data.get('population', 0)
            timezones = country_data.get('timezones') 

            flags = country_data.get('flags', {})
            flags_svg = flags.get('svg')
            flags_png = flags.get('png')

            latlng = country_data.get('latlng', [])
            latitude = latlng[0] if len(latlng) == 2 else None
            longitude = latlng[1] if len(latlng) == 2 else None

            try:
                country, created = Country.objects.update_or_create(
                    cca2=cca2,
                    defaults={
                        'name_common': name_common,
                        'name_official': name_official,
                        'capital': capital_str,
                        'region': region,
                        'subregion': subregion,
                        'languages': languages,
                        'population': population,
                        'timezones': timezones,
                        'flags_svg': flags_svg,
                        'flags_png': flags_png,
                        'latitude': latitude,
                        'longitude': longitude,
                    }
                )

                if created:
                    countries_created_count += 1
                   
                else:
                    countries_updated_count += 1
                    

            except Exception as e:
                logger.error(f"Error saving country {name_common} ({cca2}): {e}")
                self.stderr.write(self.style.ERROR(f"Failed to save {name_common}: {e}"))


        success_message = f"Finished fetching countries. Created: {countries_created_count}, Updated: {countries_updated_count}"
        logger.info(success_message)
        self.stdout.write(self.style.SUCCESS(success_message))