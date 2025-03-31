import requests
from django.core.management.base import BaseCommand
from heroes.models import Hero


class Command(BaseCommand):
    help = 'Загружает всех героев из OpenDota API'

    def handle(self, *args, **options):
        url = "https://api.opendota.com/api/heroes?api_key=62e34084-5c55-49d7-8280-0f662a71d126"

        try:
            response = requests.get(url, timeout=15)
            response.raise_for_status()
            heroes_data = response.json()

            created_count = 0
            for hero_data in heroes_data:
                hero, created = Hero.objects.update_or_create(
                    id=hero_data['id'],
                    defaults={
                        'name': hero_data['name'],
                        'localized_name': hero_data['localized_name']
                    }
                )
                if created:
                    created_count += 1

            self.stdout.write(self.style.SUCCESS(
                f"Успешно загружено героев: {len(heroes_data)} (новых: {created_count})"
            ))

        except requests.exceptions.RequestException as e:
            self.stdout.write(self.style.ERROR(f"Ошибка при запросе к API: {e}"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Неожиданная ошибка: {e}"))