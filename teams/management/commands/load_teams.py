import requests
from django.core.management.base import BaseCommand
from teams.models import Team
from django.utils.timezone import make_aware
from datetime import datetime
from time import sleep


class Command(BaseCommand):
    help = 'Загружает все команды из OpenDota API'

    def add_arguments(self, parser):
        parser.add_argument(
            '--delay',
            type=float,
            default=2.0,
            help='Задержка между запросами (секунды)'
        )
        parser.add_argument(
            '--limit',
            type=int,
            default=None,
            help='Лимит количества команд для загрузки'
        )

    def handle(self, *args, **options):
        delay = options['delay']
        limit = options['limit']
        api_key = "62e34084-5c55-49d7-8280-0f662a71d126"
        base_url = "https://api.opendota.com/api/teams"

        try:
            # Получаем общее количество команд
            count_url = f"{base_url}?api_key={api_key}"
            count_response = requests.get(count_url, timeout=15)
            count_response.raise_for_status()
            total_teams = len(count_response.json())

            if limit and limit < total_teams:
                total_teams = limit

            self.stdout.write(f"Найдено команд: {total_teams}\nНачинаю загрузку...")

            processed = 0
            batch_size = 100  # OpenDota возвращает максимум 100 команд за запрос
            offset = 0

            while processed < total_teams:
                params = {
                    'api_key': api_key,
                    'limit': batch_size,
                    'offset': offset
                }

                try:
                    response = requests.get(base_url, params=params, timeout=15)
                    response.raise_for_status()
                    teams_data = response.json()

                    if not teams_data:
                        break

                    for team_data in teams_data:
                        # Преобразование Unix timestamp в datetime
                        last_match_time = None
                        if team_data.get('last_match_time'):
                            last_match_time = make_aware(datetime.fromtimestamp(team_data['last_match_time']))

                        Team.objects.update_or_create(
                            team_id=team_data['team_id'],
                            defaults={
                                'name': team_data.get('name', f"Team {team_data['team_id']}"),
                                'tag': team_data.get('tag'),
                                'logo_url': team_data.get('logo_url'),
                                'rating': team_data.get('rating'),
                                'wins': team_data.get('wins', 0),
                                'losses': team_data.get('losses', 0),
                                'last_match_time': last_match_time
                            }
                        )
                        processed += 1
                        if processed % 10 == 0:
                            self.stdout.write(f"Обработано: {processed}/{total_teams}")

                        if limit and processed >= limit:
                            break

                    offset += batch_size
                    sleep(delay)

                except requests.exceptions.RequestException as e:
                    self.stdout.write(self.style.ERROR(f"Ошибка запроса: {e}"))
                    sleep(delay * 2)  # Увеличиваем задержку при ошибке
                    continue

            self.stdout.write(self.style.SUCCESS(
                f"\nЗавершено! Успешно загружено {processed} команд"
            ))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Критическая ошибка: {e}"))