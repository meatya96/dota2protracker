import requests
from django.core.management.base import BaseCommand
from leagues.models import League


class Command(BaseCommand):
    help = 'Загружает лиги из OpenDota API, начиная с указанного leagueid'

    def add_arguments(self, parser):
        parser.add_argument(
            '--min-id',
            type=int,
            default=17891,  # ID, с которого начинать загрузку (по умолчанию 17891)
            help='Минимальный leagueid для загрузки'
        )
        parser.add_argument(
            '--max-id',
            type=int,
            default=None,  # Максимальный leagueid (по умолчанию нет ограничения)
            help='Максимальный leagueid для загрузки'
        )

    def handle(self, *args, **options):
        min_id = options['min_id']
        max_id = options['max_id']
        url = "https://api.opendota.com/api/leagues?api_key=62e34084-5c55-49d7-8280-0f662a71d126"

        try:
            self.stdout.write(f"Запрашиваю данные лиг с {url}...")
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            leagues_data = response.json()
            self.stdout.write(f"Получено {len(leagues_data)} лиг")

            # Фильтрация лиг по диапазону ID
            filtered_leagues = [
                league for league in leagues_data
                if league['leagueid'] >= min_id and (max_id is None or league['leagueid'] <= max_id)
            ]

            if not filtered_leagues:
                self.stdout.write(self.style.WARNING("Нет лиг, соответствующих критериям фильтрации"))
                return

            # Запись в базу
            created_count = 0
            updated_count = 0
            for league in filtered_leagues:
                _, created = League.objects.update_or_create(
                    leagueid=league['leagueid'],
                    defaults={'name': league['name']}
                )
                if created:
                    created_count += 1
                else:
                    updated_count += 1

            self.stdout.write(
                self.style.SUCCESS(
                    f"Успешно обработано {len(filtered_leagues)} лиг\n"
                    f"Создано новых: {created_count}\n"
                    f"Обновлено существующих: {updated_count}\n"
                    f"Диапазон ID: от {min_id} {f'до {max_id}' if max_id else 'и выше'}"
                )
            )

        except requests.exceptions.RequestException as e:
            self.stdout.write(self.style.ERROR(f"Ошибка при запросе к API: {e}"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Неожиданная ошибка: {e}"))