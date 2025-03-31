import requests
from django.core.management.base import BaseCommand
from leagues.models import League
from matches.models import Match
from teams.models import Team
from django.utils.timezone import make_aware
from datetime import datetime
from time import sleep


class Command(BaseCommand):
    help = 'Загружает ВСЕ матчи для всех лиг из базы данных (без лимитов)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--delay',
            type=float,
            default=1.0,
            help='Задержка между запросами к API (в секундах)'
        )

    def handle(self, *args, **options):
        delay = options['delay']
        leagues = League.objects.all()

        if not leagues.exists():
            self.stdout.write(self.style.WARNING('Нет лиг в базе. Сначала запустите load_leagues.'))
            return

        total_created = 0

        for league in leagues:
            self.stdout.write(f"\nНачинаю загрузку матчей для лиги: {league.name} (ID: {league.leagueid})")

            url = f"https://api.opendota.com/api/leagues/{league.leagueid}/matches?api_key=62e34084-5c55-49d7-8280-0f662a71d126"
            has_more = True
            offset = 0
            league_created = 0

            while has_more:
                try:
                    params = {'offset': offset}
                    response = requests.get(url, params=params)
                    response.raise_for_status()
                    matches_data = response.json()

                    if not matches_data:
                        break

                    for match in matches_data:
                        url = f"https://api.opendota.com/api/matches/{match['match_id']}?api_key=62e34084-5c55-49d7-8280-0f662a71d126"
                        response = requests.get(url, params=params)
                        response.raise_for_status()
                        matches_patch = response.json()
                        _, created = Match.objects.update_or_create(
                            match_id=match['match_id'],
                            defaults={
                                'league': league,
                                'start_time': make_aware(datetime.fromtimestamp(match['start_time'])),
                                'duration': match['duration'],
                                'radiant_win': match['radiant_win'],
                                'radiant_team': Team.objects.filter(team_id=match.get('radiant_team_id')).first(),
                                'dire_team': Team.objects.filter(team_id=match.get('dire_team_id')).first(),
                                'patch':matches_patch.get('patch')
                            }
                        )
                        if created:
                            league_created += 1

                    offset += len(matches_data)
                    has_more = len(matches_data) == 100  # OpenDota возвращает по 100 матчей за запрос

                    self.stdout.write(f"Загружено {offset} матчей...")
                    sleep(delay)

                except requests.exceptions.RequestException as e:
                    self.stdout.write(self.style.ERROR(f"Ошибка: {e}. Пропускаю лигу {league.name}"))
                    break
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Неожиданная ошибка: {e}"))
                    break

            total_created += league_created
            self.stdout.write(
                self.style.SUCCESS(f"Добавлено {league_created} новых матчей для лиги {league.name}")
            )

        self.stdout.write(
            self.style.SUCCESS(f"\nГотово! Всего добавлено {total_created} новых матчей.")
        )