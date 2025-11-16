"""
Сравнительный анализ производительности разных реализаций хеш-таблиц
"""

import time
import timeit
import random
import string
from hash_table_chaining import HashTableChaining
from hash_table_open_addressing import HashTableOpenAddressing
from hash_functions import HASH_FUNCTIONS


class PerformanceAnalyzer:
    """Анализатор производительности хеш-таблиц"""

    def __init__(self):
        self.results = {}

    def generate_random_keys(self, count: int, key_length: int = 8) -> list:
        """Генерация случайных строковых ключей"""
        return [''.join(random.choices(string.ascii_letters, k=key_length))
                for _ in range(count)]

    def measure_operation_time(self, ht, operation: str, keys: list, values: list = None) -> float:
        """Измерение времени выполнения операции"""
        if operation == 'insert':
            def operation_wrapper():
                for i, key in enumerate(keys):
                    value = values[i] if values else i
                    ht.insert(key, value)

        elif operation == 'search':
            def operation_wrapper():
                for key in keys:
                    ht.search(key)

        elif operation == 'delete':
            def operation_wrapper():
                for key in keys:
                    ht.delete(key)

        else:
            raise ValueError(f"Неизвестная операция: {operation}")

        # Измерение времени
        timer = timeit.Timer(operation_wrapper)
        times = timer.repeat(repeat=3, number=1)
        return min(times)  # Берем лучшее время

    def run_performance_test(self, key_count: int = 1000, load_factors: list = None):
        """Запуск полного теста производительности"""
        if load_factors is None:
            load_factors = [0.1, 0.25, 0.5, 0.75, 0.9]

        print("Запуск тестов производительности...")
        print(f"Количество ключей: {key_count}")
        print(f"Коэффициенты заполнения: {load_factors}")
        print("=" * 60)

        # Генерация тестовых данных
        all_keys = self.generate_random_keys(key_count)
        all_values = list(range(key_count))

        self.results = {}

        # Тестируемые реализации
        implementations = [
            ('Chaining', HashTableChaining),
            ('OpenAddr-Linear', lambda size: HashTableOpenAddressing(
                initial_size=size, probing_method='linear')),
            ('OpenAddr-Double', lambda size: HashTableOpenAddressing(
                initial_size=size, probing_method='double_hashing'))
        ]

        for impl_name, impl_class in implementations:
            print(f"\nТестирование: {impl_name}")
            self.results[impl_name] = {}

            for load_factor in load_factors:
                print(f"  Коэффициент заполнения: {load_factor}", end=" ", flush=True)

                # Вычисляем начальный размер для достижения нужного коэффициента
                initial_size = int(key_count / load_factor)
                ht = impl_class(initial_size)

                # Вставляем часть ключей для достижения целевого коэффициента
                insert_count = int(key_count * load_factor)
                insert_keys = all_keys[:insert_count]
                insert_values = all_values[:insert_count]

                # Измеряем время операций
                times = {}

                # Вставка
                times['insert'] = self.measure_operation_time(
                    ht, 'insert', insert_keys, insert_values)
                print("I", end="", flush=True)

                # Поиск (успешный)
                times['search_success'] = self.measure_operation_time(
                    ht, 'search', insert_keys)
                print("S", end="", flush=True)

                # Поиск (неуспешный)
                unused_keys = all_keys[insert_count:insert_count + 100]  # 100 ключей для поиска
                times['search_fail'] = self.measure_operation_time(
                    ht, 'search', unused_keys)
                print("F", end="", flush=True)

                # Удаление
                delete_keys = insert_keys[:len(insert_keys) // 2]  # Удаляем половину
                times['delete'] = self.measure_operation_time(
                    ht, 'delete', delete_keys)
                print("D", end="", flush=True)

                # Получаем статистику
                stats = ht.get_stats()
                times.update(stats)

                self.results[impl_name][load_factor] = times
                print(" ✓")

        return self.results

    def print_performance_summary(self):
        """Вывод сводной таблицы производительности"""
        print("\n" + "="*80)
        print("СВОДНАЯ ТАБЛИЦА ПРОИЗВОДИТЕЛЬНОСТИ")
        print("="*80)

        operations = ['insert', 'search_success', 'search_fail', 'delete']

        for operation in operations:
            print(f"\nОперация: {operation.upper()}")
            print("Implementation".ljust(20), end="")

            # Заголовки с коэффициентами заполнения
            load_factors = list(list(self.results.values())[0].keys())
            for lf in load_factors:
                print(f"{lf:>10}", end="")
            print()
            print("-" * (20 + 10 * len(load_factors)))

            # Данные по реализациям
            for impl_name, lf_data in self.results.items():
                print(f"{impl_name:<20}", end="")
                for lf in load_factors:
                    time_val = lf_data[lf].get(operation, 0)
                    print(f"{time_val:>10.4f}", end="")
                print()

    def analyze_collisions(self):
        """Анализ количества коллизий"""
        print("\n" + "=" * 60)
        print("АНАЛИЗ КОЛЛИЗИЙ")
        print("=" * 60)

        key_count = 1000
        test_keys = self.generate_random_keys(key_count)

        # Увеличиваем размер таблицы для избежания переполнения
        table_size = 2000  # Увеличили размер для надежности

        # Тестируем разные хеш-функции
        for hash_func_name in HASH_FUNCTIONS.keys():
            print(f"\nХеш-функция: {hash_func_name}")

            try:
                # Тестируем с методом цепочек
                ht_chaining = HashTableChaining(
                    initial_size=table_size,
                    hash_function=hash_func_name,
                    load_factor_threshold=1.0  # Отключаем auto-resize для чистоты эксперимента
                )

                for key in test_keys:
                    ht_chaining.insert(key, 1)

                stats = ht_chaining.get_stats()
                print(f"  Метод цепочек:")
                print(f"    Коллизии: {stats['collisions']}")
                print(f"    Средняя длина цепочки: {stats['avg_chain_length']:.2f}")
                print(f"    Макс. длина цепочки: {stats['max_chain_length']}")

            except Exception as e:
                print(f"  Метод цепочек: Ошибка - {e}")

            try:
                # Тестируем с открытой адресацией
                ht_oa = HashTableOpenAddressing(
                    initial_size=table_size,
                    hash_function=hash_func_name,
                    load_factor_threshold=1.0
                )

                for key in test_keys:
                    ht_oa.insert(key, 1)

                stats = ht_oa.get_stats()
                print(f"  Открытая адресация:")
                print(f"    Средняя длина пробирования: {stats['avg_probe_length']:.2f}")
                print(f"    Макс. длина пробирования: {stats['max_probe_length']}")

            except Exception as e:
                print(f"  Открытая адресация: Ошибка - {e}")


def main():
    """Основная функция анализа производительности"""
    analyzer = PerformanceAnalyzer()

    # Запуск тестов производительности
    results = analyzer.run_performance_test(
        key_count=1000,
        load_factors=[0.1, 0.25, 0.5, 0.75, 0.9]
    )

    # Вывод результатов
    analyzer.print_performance_summary()

    # Анализ коллизий
    analyzer.analyze_collisions()

    return results


if __name__ == "__main__":
    results = main()