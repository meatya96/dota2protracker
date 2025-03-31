# draft_timings/management/commands/load_draft_timings.py
import requests
from django.core.management.base import BaseCommand
from matches.models import Match
from draft_timings.models import DraftTiming
from time import sleep
from django.db.models import Q


class Command(BaseCommand):
    help = 'Загружает тайминг драфта для матчей из базы данных (без времени)'

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
            help='Лимит матчей для обработки'
        )
        parser.add_argument(
            '--skip-existing',
            action='store_true',
            help='Пропускать матчи с уже загруженным драфтом'
        )

    def handle(self, *args, **options):
        delay = options['delay']
        limit = options['limit']
        skip_existing = options['skip_existing']
        api_key = "62e34084-5c55-49d7-8280-0f662a71d126"

        # Получаем матчи из базы данных
        matches_query = Match.objects.all().order_by('-start_time')

        if skip_existing:
            matches_query = matches_query.filter(
                ~Q(draft_timings__isnull=False)
            )

        if limit:
            matches_query = matches_query[:limit]

        total_matches = matches_query.count()
        self.stdout.write(f"Найдено матчей для обработки: {total_matches}")

        processed = 0
        for match in matches_query:
            try:
                url = f"https://api.opendota.com/api/matches/{match.match_id}?api_key={api_key}"
                response = requests.get(url, timeout=15)
                response.raise_for_status()
                match_data = response.json()

                if not match_data.get('picks_bans'):
                    self.stdout.write(
                        f"[{processed + 1}/{total_matches}] Матч {match.match_id} не содержит данных о драфте")
                    continue

                actions_processed = 0
                for action in match_data['picks_bans']:
                    team_id = match.radiant_team_id if action['team'] == 0 else match.dire_team_id

                    DraftTiming.objects.update_or_create(
                        match=match,
                        order=action['order'],
                        defaults={
                            'hero': action['hero_id'],
                            'is_pick': action['is_pick'],
                            'team_id': team_id,
                            'stage': self.get_stage_type(action['order'])
                        }
                    )
                    actions_processed += 1

                processed += 1
                self.stdout.write(
                    f"[{processed}/{total_matches}] Матч {match.match_id}: "
                    f"{actions_processed} действий драфта"
                )

            except requests.exceptions.RequestException as e:
                self.stdout.write(self.style.ERROR(
                    f"[{processed + 1}/{total_matches}] Ошибка запроса для матча {match.match_id}: {e}"
                ))
            except Exception as e:
                self.stdout.write(self.style.ERROR(
                    f"[{processed + 1}/{total_matches}] Ошибка обработки матча {match.match_id}: {e}"
                ))
            finally:
                sleep(delay)

        self.stdout.write(self.style.SUCCESS(
            f"\nЗавершено! Обработано матчей: {processed}/{total_matches}"
        ))

    def get_stage_type(self, order):
        """Определяет стадию драфта по порядковому номеру"""
        if order < 7: return 'ban_1'
        if order == 7: return 'first_pick'
        if order == 8: return 'second_pick'
        if order in range(9,12): return 'ban_10-12'
        if order in range(12,18): return 'pick_13-18'
        if order in range(18,22): return 'ban_19-22'
        if order == 22: return 'pick_23'
        return 'pick_24'
