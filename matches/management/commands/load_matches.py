import requests
from django.core.management.base import BaseCommand
from leagues.models import League
from matches.models import Match
from django.utils.timezone import make_aware
from datetime import datetime
import time
from django.db import transaction


class Command(BaseCommand):
    help = 'Полная перезапись матчей с фильтрацией по патчу'

    def add_arguments(self, parser):
        parser.add_argument(
            '--min-patch',
            type=int,
            default=57,
            help='Минимальный номер патча (включительно)'
        )
        parser.add_argument(
            '--delay',
            type=float,
            default=2.0,
            help='Задержка между запросами (секунды)'
        )

    def handle(self, *args, **options):
        min_patch = options['min_patch']
        delay = options['delay']

        # Диагностика перед запуском
        self.stdout.write(f"Конфигурация:\n"
                          f"- Минимальный патч: {min_patch}\n"
                          f"- Задержка: {delay} сек\n"
                          f"- Лиг в базе: {League.objects.count()}")

        # 1. Полная очистка матчей
        with transaction.atomic():
            Match.objects.all().delete()
            self.stdout.write(self.style.SUCCESS("База матчей очищена"))

            # 2. Загрузка новых данных
            total_created = 0
            for league in League.objects.all():
                self.stdout.write(f"\nОбработка лиги {league.name} (ID: {league.leagueid})...")
                league_created = 0
                offset = 0
                retries = 3  # Количество попыток повтора при ошибках

                while retries > 0:
                    try:
                        url = f"https://api.opendota.com/api/leagues/{league.leagueid}/matches?api_key=62e34084-5c55-49d7-8280-0f662a71d126"
                        params = {'offset': offset}

                        # Диагностический вывод
                        self.stdout.write(f"Запрос: {url}?offset={offset}")

                        response = requests.get(url, params=params, timeout=15)
                        response.raise_for_status()
                        matches = response.json()

                        if not matches:
                            self.stdout.write("Достигнут конец списка матчей")
                            break

                        for match in matches:
                            # Подробная диагностика каждого матча
                            patch = match.get('patch')
                            match_info = (
                                f"ID: {match['match_id']}, "
                                f"Патч: {patch}, "
                                f"Дата: {datetime.fromtimestamp(match['start_time'])}"
                            )

                            if patch is None:
                                self.stdout.write(f"⚠ Пропуск: {match_info} (нет данных о патче)")
                                continue

                            if int(patch) < min_patch:
                                self.stdout.write(f"⚠ Пропуск: {match_info} (патч {patch} < {min_patch})")
                                continue

                            # Создание записи
                            Match.objects.create(
                                match_id=match['match_id'],
                                league=league,
                                start_time=make_aware(datetime.fromtimestamp(match['start_time'])),
                                duration=match['duration'],
                                radiant_win=match['radiant_win'],
                                radiant_team=match.get('radiant_name'),
                                dire_team=match.get('dire_name'),
                                patch=int(patch)
                            )
                            league_created += 1
                            self.stdout.write(f"✓ Добавлен: {match_info}")

                        total_created += league_created
                        offset += len(matches)
                        retries = 3  # Сброс счетчика попыток после успеха
                        time.sleep(delay)

                    except requests.exceptions.RequestException as e:
                        retries -= 1
                        self.stdout.write(self.style.ERROR(
                            f"Ошибка запроса (осталось попыток: {retries}): {e}"
                        ))
                        if retries > 0:
                            time.sleep(5)
                        else:
                            break

                self.stdout.write(self.style.SUCCESS(
                    f"Добавлено матчей для лиги {league.name}: {league_created}"
                ))

            self.stdout.write(self.style.SUCCESS(
                f"\nГотово! Всего добавлено матчей: {total_created}"
            ))

        # Финальная проверка
        self.stdout.write(f"\nПроверка базы данных:")
        self.stdout.write(f"- Всего матчей: {Match.objects.count()}")
        self.stdout.write(f"- Пример последнего матча:")
        if Match.objects.exists():
            last_match = Match.objects.latest('start_time')
            self.stdout.write(f"  ID: {last_match.match_id}, "
                              f"Лига: {last_match.league.name}, "
                              f"Патч: {last_match.patch}")