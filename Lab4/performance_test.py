"""
Эмпирический анализ производительности алгоритмов сортировки
"""

import time
import timeit
import sys
from typing import Dict, List
from sorts import SORTING_ALGORITHMS
from generate_data import generate_test_datasets


class PerformanceTester:
    """Класс для тестирования производительности алгоритмов сортировки"""

    def __init__(self):
        self.results = {}
        self.system_info = self._get_system_info()

    def _get_system_info(self) -> Dict:
        """Получение информации о системе для воспроизводимости"""
        return {
            'platform': sys.platform,
            'python_version': sys.version,
            'processor': 'Unknown'  # Можно добавить psutil для детальной информации
        }

    def measure_time(self, algo_func, arr: List[int], iterations: int = 1) -> float:
        """Измерение времени выполнения с использованием timeit"""

        def sort_wrapper():
            return algo_func(arr.copy())

        timer = timeit.Timer(sort_wrapper)
        times = timer.repeat(repeat=3, number=iterations)
        return min(times) / iterations  # Берем лучшее время

    def run_performance_tests(self, sizes: List[int] = None, iterations: int = 1):
        """Запуск полного тестирования производительности"""
        if sizes is None:
            sizes = [100, 500, 1000, 3000, 5000]

        print("Запуск тестов производительности...")
        print(f"Размеры массивов: {sizes}")
        print(f"Итераций на тест: {iterations}")
        print(f"Система: {self.system_info['platform']}")
        print("=" * 60)

        # Генерация тестовых данных
        datasets = generate_test_datasets(sizes)
        self.results = {}

        for data_type, sizes_data in datasets.items():
            print(f"\nТип данных: {data_type.upper()}")
            print("-" * 40)

            self.results[data_type] = {}

            for algo_name, algo_func in SORTING_ALGORITHMS.items():
                print(f"  {algo_name}:", end=" ", flush=True)
                algo_times = []

                for size, test_array in sizes_data.items():
                    time_taken = self.measure_time(algo_func, test_array, iterations)
                    algo_times.append((size, time_taken))
                    print(f"{size}({time_taken:.4f}s)", end=" ", flush=True)

                self.results[data_type][algo_name] = algo_times
                print()  # новая строка

        return self.results

    def print_summary(self):
        """Вывод сводной таблицы результатов"""
        print("\n" + "=" * 80)
        print("СВОДНАЯ ТАБЛИЦА РЕЗУЛЬТАТОВ")
        print("=" * 80)

        for data_type, algorithms in self.results.items():
            print(f"\n{data_type.upper()}:")
            print("Algorithm".ljust(20), end="")

            # Заголовки с размерами
            sizes = [size for size, _ in list(algorithms.values())[0]]
            for size in sizes:
                print(f"{size:>10}", end="")
            print()
            print("-" * (20 + 10 * len(sizes)))

            # Данные по алгоритмам
            for algo_name, times in algorithms.items():
                print(f"{algo_name:<20}", end="")
                for size, time_val in times:
                    print(f"{time_val:>10.4f}", end="")
                print()


def main():
    """Основная функция тестирования производительности"""
    tester = PerformanceTester()

    # Размеры для тестирования (можно увеличить для более точных результатов)
    test_sizes = [100, 500, 1000, 3000, 5000, 7000, 10000]

    # Запуск тестов
    results = tester.run_performance_tests(sizes=test_sizes, iterations=1)

    # Вывод сводки
    tester.print_summary()

    return results


if __name__ == "__main__":
    results = main()