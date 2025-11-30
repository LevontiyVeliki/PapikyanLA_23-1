"""
Сравнительный анализ различных подходов динамического программирования.
"""

import time
import matplotlib.pyplot as plt
from dynamic_programming import *
import sys
import psutil
import os


class DPComparison:
    """
    Класс для сравнения различных реализаций алгоритмов ДП.
    """

    @staticmethod
    def compare_fibonacci_methods(max_n: int = 1000):
        """
        Сравнение методов вычисления чисел Фибоначчи.
        """
        print("=== СРАВНЕНИЕ МЕТОДОВ ВЫЧИСЛЕНИЯ ЧИСЕЛ ФИБОНАЧЧИ ===\n")

        # Тестируем разные диапазоны
        small_test_values = list(range(5, 36, 5))  # Для наивного метода
        large_test_values = list(range(100, max_n + 1, 100))  # Для оптимизированных методов

        naive_times = []
        memo_times = []
        bottom_up_times = []
        optimized_times = []
        matrix_times = []

        print("МАЛЕНЬКИЕ ЗНАЧЕНИЯ (n <= 35):")
        print("n\tНаивный\tМемоизация\tВосходящий\tОптимизир.\tМатричный")
        print("-" * 70)

        for n in small_test_values:
            times_row = [n]

            # Наивный метод (только для маленьких n)
            if n <= 35:
                start = time.perf_counter()
                result = FibonacciDP.fibonacci_naive(n)
                end = time.perf_counter()
                naive_time = (end - start) * 1000
                times_row.append(f"{naive_time:.3f}")
                naive_times.append(naive_time)
            else:
                times_row.append("N/A")
                naive_times.append(None)

            # Мемоизация
            start = time.perf_counter()
            result = FibonacciDP.fibonacci_memo(n)
            end = time.perf_counter()
            memo_time = (end - start) * 1000
            times_row.append(f"{memo_time:.3f}")
            memo_times.append(memo_time)

            # Восходящий
            start = time.perf_counter()
            result = FibonacciDP.fibonacci_bottom_up(n)
            end = time.perf_counter()
            bottom_up_time = (end - start) * 1000
            times_row.append(f"{bottom_up_time:.3f}")
            bottom_up_times.append(bottom_up_time)

            # Оптимизированный
            start = time.perf_counter()
            result = FibonacciDP.fibonacci_optimized(n)
            end = time.perf_counter()
            optimized_time = (end - start) * 1000
            times_row.append(f"{optimized_time:.3f}")
            optimized_times.append(optimized_time)

            # Матричный
            start = time.perf_counter()
            result = FibonacciDP.fibonacci_matrix(n)
            end = time.perf_counter()
            matrix_time = (end - start) * 1000
            times_row.append(f"{matrix_time:.3f}")
            matrix_times.append(matrix_time)

            print("\t".join(str(x) for x in times_row))

        print("\nБОЛЬШИЕ ЗНАЧЕНИЯ (n >= 100):")
        print("n\tМемоизация\tВосходящий\tОптимизир.\tМатричный")
        print("-" * 60)

        large_memo_times = []
        large_bottom_up_times = []
        large_optimized_times = []
        large_matrix_times = []

        for n in large_test_values:
            times_row = [n]

            try:
                # Мемоизация
                start = time.perf_counter()
                result = FibonacciDP.fibonacci_memo(n)
                end = time.perf_counter()
                memo_time = (end - start) * 1000
                times_row.append(f"{memo_time:.3f}")
                large_memo_times.append(memo_time)
            except RecursionError:
                times_row.append("RECURSION")
                large_memo_times.append(None)

            # Восходящий
            start = time.perf_counter()
            result = FibonacciDP.fibonacci_bottom_up(n)
            end = time.perf_counter()
            bottom_up_time = (end - start) * 1000
            times_row.append(f"{bottom_up_time:.3f}")
            large_bottom_up_times.append(bottom_up_time)

            # Оптимизированный
            start = time.perf_counter()
            result = FibonacciDP.fibonacci_optimized(n)
            end = time.perf_counter()
            optimized_time = (end - start) * 1000
            times_row.append(f"{optimized_time:.3f}")
            large_optimized_times.append(optimized_time)

            # Матричный
            start = time.perf_counter()
            result = FibonacciDP.fibonacci_matrix(n)
            end = time.perf_counter()
            matrix_time = (end - start) * 1000
            times_row.append(f"{matrix_time:.3f}")
            large_matrix_times.append(matrix_time)

            print("\t".join(str(x) for x in times_row))

        # Построение графиков
        plt.figure(figsize=(15, 10))

        # График 1: Маленькие значения
        plt.subplot(2, 2, 1)
        available_test_values = [n for n in small_test_values if n <= 35]
        if available_test_values:
            plt.plot(available_test_values, [t for t in naive_times if t is not None],
                    'o-', label='Наивный', linewidth=2, markersize=6)
        plt.plot(small_test_values, memo_times, 's-', label='Мемоизация', linewidth=2, markersize=6)
        plt.plot(small_test_values, bottom_up_times, '^-', label='Восходящий', linewidth=2, markersize=6)
        plt.plot(small_test_values, optimized_times, 'd-', label='Оптимизированный', linewidth=2, markersize=6)
        plt.plot(small_test_values, matrix_times, 'v-', label='Матричный', linewidth=2, markersize=6)

        plt.xlabel('n')
        plt.ylabel('Время (мс)')
        plt.title('Сравнение времени вычисления чисел Фибоначчи\n(маленькие n)')
        plt.legend()
        plt.grid(True, alpha=0.3)

        # График 2: Большие значения
        plt.subplot(2, 2, 2)
        # Фильтруем значения, где мемоизация не вызвала рекурсию
        valid_large_values = [n for n, t in zip(large_test_values, large_memo_times) if t is not None]
        valid_memo_times = [t for t in large_memo_times if t is not None]

        if valid_large_values:
            plt.plot(valid_large_values, valid_memo_times, 's-', label='Мемоизация', linewidth=2, markersize=6)
        plt.plot(large_test_values, large_bottom_up_times, '^-', label='Восходящий', linewidth=2, markersize=6)
        plt.plot(large_test_values, large_optimized_times, 'd-', label='Оптимизированный', linewidth=2, markersize=6)
        plt.plot(large_test_values, large_matrix_times, 'v-', label='Матричный', linewidth=2, markersize=6)

        plt.xlabel('n')
        plt.ylabel('Время (мс)')
        plt.title('Сравнение времени вычисления чисел Фибоначчи\n(большие n)')
        plt.legend()
        plt.grid(True, alpha=0.3)

        # График 3: Сравнение сложности
        plt.subplot(2, 2, 3)
        methods = ['Наивный', 'Мемоизация', 'Восходящий', 'Оптимизированный', 'Матричный']
        time_complexities = ['O(2ⁿ)', 'O(n)', 'O(n)', 'O(n)', 'O(log n)']
        space_complexities = ['O(n)', 'O(n)', 'O(n)', 'O(1)', 'O(1)']

        # Создаем таблицу
        cell_text = [
            ['O(2ⁿ)', 'O(n)', 'O(n)', 'O(n)', 'O(log n)'],
            ['O(n)', 'O(n)', 'O(n)', 'O(1)', 'O(1)']
        ]

        plt.axis('tight')
        plt.axis('off')
        table = plt.table(cellText=cell_text,
                         rowLabels=['Время', 'Память'],
                         colLabels=methods,
                         cellLoc='center',
                         loc='center')
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1, 2)
        plt.title('Сравнение сложности алгоритмов')

        # График 4: Логарифмическая шкала для больших n
        plt.subplot(2, 2, 4)
        plt.plot(large_test_values, large_bottom_up_times, '^-', label='Восходящий O(n)', linewidth=2)
        plt.plot(large_test_values, large_optimized_times, 'd-', label='Оптимизированный O(n)', linewidth=2)
        plt.plot(large_test_values, large_matrix_times, 'v-', label='Матричный O(log n)', linewidth=2)

        plt.xlabel('n')
        plt.ylabel('Время (мс)')
        plt.title('Время вычисления (логарифмическая шкала)')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.yscale('log')

        plt.tight_layout()
        plt.savefig('fibonacci_comparison.png', dpi=300, bbox_inches='tight')
        plt.show()

        return (small_test_values, naive_times, memo_times, bottom_up_times, optimized_times, matrix_times,
                large_test_values, large_memo_times, large_bottom_up_times, large_optimized_times, large_matrix_times)

    @staticmethod
    def compare_knapsack_approaches():
        """
        Сравнение жадного подхода и ДП для задачи о рюкзаке.
        """
        print("\n=== СРАВНЕНИЕ ЖАДНОГО ПОДХОДА И ДП ДЛЯ РЮКЗАКА ===\n")

        # Тестовые данные
        weights = [2, 3, 4, 5]
        values = [3, 4, 5, 6]
        capacity = 5

        print("Предметы:")
        for i, (w, v) in enumerate(zip(weights, values)):
            print(f"  Предмет {i}: вес={w}, стоимость={v}, удельная={v/w:.2f}")

        print(f"\nВместимость рюкзака: {capacity}")

        # Жадный подход (для непрерывного рюкзака)
        items = list(zip(values, weights, range(len(weights))))
        items_sorted = sorted(items, key=lambda x: x[0]/x[1], reverse=True)

        greedy_value = 0
        remaining = capacity
        greedy_selection = []

        for value, weight, idx in items_sorted:
            if remaining >= weight:
                greedy_value += value
                remaining -= weight
                greedy_selection.append((idx, weight, value, 1.0))
            else:
                fraction = remaining / weight
                greedy_value += value * fraction
                greedy_selection.append((idx, weight, value, fraction))
                break

        print(f"\nЖадный алгоритм (непрерывный):")
        print(f"  Максимальная стоимость: {greedy_value:.2f}")
        print("  Выбранные предметы:")
        for idx, weight, value, fraction in greedy_selection:
            print(f"    Предмет {idx}: вес {weight}, стоимость {value}, доля {fraction:.1%}")

        # ДП для 0-1 рюкзака
        dp_value, dp_selection = KnapsackDP.knapsack_01_bottom_up(weights, values, capacity)

        print(f"\nДП алгоритм (0-1 рюкзак):")
        print(f"  Максимальная стоимость: {dp_value}")
        print("  Выбранные предметы:")
        total_weight = 0
        for idx in dp_selection:
            print(f"    Предмет {idx}: вес {weights[idx]}, стоимость {values[idx]}")
            total_weight += weights[idx]
        print(f"  Общий вес: {total_weight}")

        # Визуализация таблицы ДП
        print("\n" + "="*50)
        DPVisualizer.visualize_knapsack_dp(weights, values, capacity)

        return greedy_value, dp_value, greedy_selection, dp_selection

    @staticmethod
    def compare_dp_approaches_complexity():
        """
        Анализ масштабируемости алгоритмов ДП.
        """
        print("\n=== АНАЛИЗ МАСШТАБИРУЕМОСТИ АЛГОРИТМОВ ДП ===\n")

        # Характеристики тестовой машины
        import platform
        print("Характеристики тестовой машины:")
        print(f"Процессор: {platform.processor()}")
        print(f"Память: {psutil.virtual_memory().total // (1024**3)} GB")
        print(f"ОС: {platform.system()} {platform.release()}")
        print(f"Python: {sys.version}")
        print()

        # Анализ времени для рюкзака при увеличении размера
        sizes = [10, 20, 50, 100, 200]
        knapsack_times = []
        lcs_times = []
        levenshtein_times = []

        print("Размер\tРюкзак (мс)\tLCS (мс)\tЛевенштейн (мс)")
        print("-" * 50)

        for size in sizes:
            # Генерация тестовых данных
            weights = [i % 10 + 1 for i in range(size)]
            values = [i * 2 + 1 for i in range(size)]
            capacity = size * 2

            # Рюкзак
            start = time.perf_counter()
            KnapsackDP.knapsack_01_bottom_up(weights, values, capacity)
            end = time.perf_counter()
            knapsack_time = (end - start) * 1000
            knapsack_times.append(knapsack_time)

            # LCS
            str1 = 'a' * size + 'b' * size
            str2 = 'b' * size + 'a' * size
            start = time.perf_counter()
            LCSDP.lcs_length(str1, str2)
            end = time.perf_counter()
            lcs_time = (end - start) * 1000
            lcs_times.append(lcs_time)

            # Левенштейн
            start = time.perf_counter()
            LevenshteinDP.levenshtein_distance(str1, str2)
            end = time.perf_counter()
            levenshtein_time = (end - start) * 1000
            levenshtein_times.append(levenshtein_time)

            print(f"{size}\t{knapsack_time:.2f}\t\t{lcs_time:.2f}\t\t{levenshtein_time:.2f}")

        # Построение графиков масштабируемости
        plt.figure(figsize=(12, 5))

        plt.subplot(1, 2, 1)
        plt.plot(sizes, knapsack_times, 'o-', label='Рюкзак', linewidth=2, markersize=6)
        plt.plot(sizes, lcs_times, 's-', label='LCS', linewidth=2, markersize=6)
        plt.plot(sizes, levenshtein_times, '^-', label='Левенштейн', linewidth=2, markersize=6)
        plt.xlabel('Размер входных данных')
        plt.ylabel('Время (мс)')
        plt.title('Масштабируемость алгоритмов ДП')
        plt.legend()
        plt.grid(True, alpha=0.3)

        # График теоретической сложности
        plt.subplot(1, 2, 2)
        # Нормализуем для сравнения
        max_time = max(max(knapsack_times), max(lcs_times), max(levenshtein_times))
        normalized_knapsack = [t/max_time for t in knapsack_times]
        normalized_lcs = [t/max_time for t in lcs_times]
        normalized_levenshtein = [t/max_time for t in levenshtein_times]

        plt.plot(sizes, normalized_knapsack, 'o-', label='Рюкзак O(nW)', linewidth=2)
        plt.plot(sizes, normalized_lcs, 's-', label='LCS O(n²)', linewidth=2)
        plt.plot(sizes, normalized_levenshtein, '^-', label='Левенштейн O(n²)', linewidth=2)
        plt.xlabel('Размер входных данных')
        plt.ylabel('Нормализованное время')
        plt.title('Относительная производительность')
        plt.legend()
        plt.grid(True, alpha=0.3)

        plt.tight_layout()
        plt.savefig('dp_scalability.png', dpi=300, bbox_inches='tight')
        plt.show()

        return sizes, knapsack_times, lcs_times, levenshtein_times

    @staticmethod
    def memory_usage_analysis():
        """
        Анализ использования памяти различными подходами ДП.
        """
        print("\n=== АНАЛИЗ ИСПОЛЬЗОВАНИЯ ПАМЯТИ ===\n")

        def get_memory_usage():
            process = psutil.Process(os.getpid())
            return process.memory_info().rss / 1024 / 1024  # MB

        # Тестируем различные реализации
        initial_memory = get_memory_usage()

        print("Измерение использования памяти...")

        # 1. Наивный Фибоначчи (маленькое n)
        memory_before = get_memory_usage()
        if sys.getrecursionlimit() > 1000:
            FibonacciDP.fibonacci_naive(25)  # Уменьшили для избежания переполнения
        naive_memory = get_memory_usage() - memory_before

        # 2. Мемоизация Фибоначчи
        memory_before = get_memory_usage()
        FibonacciDP.fibonacci_memo(100)
        memo_memory = get_memory_usage() - memory_before

        # 3. Восходящий Фибоначчи
        memory_before = get_memory_usage()
        FibonacciDP.fibonacci_bottom_up(1000)
        bottom_up_memory = get_memory_usage() - memory_before

        # 4. Рюкзак
        memory_before = get_memory_usage()
        weights = [i % 10 + 1 for i in range(100)]
        values = [i * 2 + 1 for i in range(100)]
        KnapsackDP.knapsack_01_bottom_up(weights, values, 200)
        knapsack_memory = get_memory_usage() - memory_before

        # 5. Оптимизированный рюкзак
        memory_before = get_memory_usage()
        KnapsackDP.knapsack_01_optimized(weights, values, 200)
        knapsack_optimized_memory = get_memory_usage() - memory_before

        print("Метод\t\t\tИспользование памяти (МБ)")
        print("-" * 50)
        print(f"Наивный Фибоначчи (n=25)\t{naive_memory:.2f}")
        print(f"Мемоизация Фибоначчи (n=100)\t{memo_memory:.2f}")
        print(f"Восходящий Фибоначчи (n=1000)\t{bottom_up_memory:.2f}")
        print(f"Рюкзак 0-1 (стандартный)\t{knapsack_memory:.2f}")
        print(f"Рюкзак 0-1 (оптимизированный)\t{knapsack_optimized_memory:.2f}")

        # Визуализация
        methods = ['Наивный\nФибоначчи', 'Мемоизация\nФибоначчи', 'Восходящий\nФибоначчи',
                  'Рюкзак\nстандартный', 'Рюкзак\nоптимизированный']
        memory_usage = [naive_memory, memo_memory, bottom_up_memory, knapsack_memory, knapsack_optimized_memory]

        plt.figure(figsize=(12, 6))
        bars = plt.bar(methods, memory_usage, color=['red', 'orange', 'yellow', 'lightblue', 'blue'])
        plt.ylabel('Использование памяти (МБ)')
        plt.title('Сравнение использования памяти алгоритмами ДП')
        plt.xticks(rotation=45, ha='right')

        # Добавляем значения на столбцы
        for bar, value in zip(bars, memory_usage):
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                    f'{value:.2f} МБ', ha='center', va='bottom', fontsize=9)

        plt.grid(True, alpha=0.3, axis='y')
        plt.tight_layout()
        plt.savefig('memory_usage.png', dpi=300, bbox_inches='tight')
        plt.show()

        return methods, memory_usage


def run_comprehensive_comparison():
    """
    Запуск комплексного сравнения всех аспектов ДП.
    """
    print("=== КОМПЛЕКСНЫЙ АНАЛИЗ ДИНАМИЧЕСКОГО ПРОГРАММИРОВАНИЯ ===\n")

    try:
        # Сравнение методов Фибоначчи
        print("1. Сравнение методов вычисления чисел Фибоначчи...")
        fib_results = DPComparison.compare_fibonacci_methods(1000)

        # Сравнение подходов к рюкзаку
        print("\n2. Сравнение подходов к задаче о рюкзаке...")
        knapsack_results = DPComparison.compare_knapsack_approaches()

        # Анализ масштабируемости
        print("\n3. Анализ масштабируемости алгоритмов ДП...")
        scalability_results = DPComparison.compare_dp_approaches_complexity()

        # Анализ памяти
        print("\n4. Анализ использования памяти...")
        memory_results = DPComparison.memory_usage_analysis()

        print("\n" + "="*60)
        print("Анализ завершен успешно! Все графики сохранены в файлы PNG.")
        print("="*60)

        return fib_results, knapsack_results, scalability_results, memory_results

    except Exception as e:
        print(f"\nПроизошла ошибка во время анализа: {e}")
        print("Продолжаем выполнение остальных тестов...")
        return None, None, None, None


if __name__ == "__main__":
    run_comprehensive_comparison()