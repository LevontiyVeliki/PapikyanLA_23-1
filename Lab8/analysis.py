"""
Анализ производительности и корректности жадных алгоритмов.
"""

import time
import random
import matplotlib.pyplot as plt
from greedy_algorithms import GreedyAlgorithms, KnapsackSolver, Interval, Item
import string


def analyze_interval_scheduling():
    """
    Анализ задачи о выборе заявок.
    """
    print("=== АНАЛИЗ ЗАДАЧИ О ВЫБОРЕ ЗАЯВОК ===\n")

    # Генерация тестовых данных
    intervals = [
        Interval(1, 3, "A"),
        Interval(2, 5, "B"),
        Interval(4, 7, "C"),
        Interval(6, 9, "D"),
        Interval(8, 10, "E"),
        Interval(1, 2, "F"),
    ]

    print("Все интервалы:")
    for interval in intervals:
        print(f"  {interval.name}: [{interval.start}, {interval.end}]")

    selected = GreedyAlgorithms.interval_scheduling(intervals)

    print("\nВыбранные интервалы (жадный алгоритм):")
    for interval in selected:
        print(f"  {interval.name}: [{interval.start}, {interval.end}]")

    print(f"\nВсего выбрано: {len(selected)} интервалов")

    # Измерение производительности
    sizes = [10, 50, 100, 500, 1000]
    times = []

    print("\nИзмерение производительности:")
    for size in sizes:
        # Генерация случайных интервалов
        test_intervals = []
        for i in range(size):
            start = random.randint(0, size * 2)
            end = start + random.randint(1, 10)
            test_intervals.append(Interval(start, end, f"Task_{i}"))

        start_time = time.perf_counter()
        GreedyAlgorithms.interval_scheduling(test_intervals)
        end_time = time.perf_counter()

        elapsed = (end_time - start_time) * 1000  # мс
        times.append(elapsed)
        print(f"  Размер {size}: {elapsed:.3f} мс")

    return sizes, times


def analyze_knapsack_problems():
    """
    Анализ задач о рюкзаке.
    """
    print("\n=== АНАЛИЗ ЗАДАЧ О РЮКЗАКЕ ===\n")

    # Тестовые данные
    capacity = 10
    items = [
        Item(60, 10, "Item1"),  # удельная стоимость: 6.0
        Item(100, 20, "Item2"),  # удельная стоимость: 5.0
        Item(120, 30, "Item3"),  # удельная стоимость: 4.0
    ]

    # Сравнение методов
    greedy_val, exact_val = KnapsackSolver.compare_knapsack_methods(capacity, items)

    # Демонстрация случая, когда жадный алгоритм не оптимален для 0-1 рюкзака
    print("\n--- Пример неоптимальности жадного подхода для 0-1 рюкзака ---")

    capacity_small = 10
    items_tricky = [
        Item(60, 6, "X"),  # удельная стоимость: 10.0
        Item(50, 5, "Y"),  # удельная стоимость: 10.0
        Item(50, 5, "Z"),  # удельная стоимость: 10.0
    ]

    KnapsackSolver.compare_knapsack_methods(capacity_small, items_tricky)

    # Измерение производительности
    sizes = [10, 20, 50, 100]
    fractional_times = []
    zero_one_times = []

    print("\nИзмерение производительности:")
    for size in sizes:
        # Генерация случайных предметов
        test_items = []
        for i in range(size):
            weight = random.randint(1, 20)
            value = random.randint(1, 100)
            test_items.append(Item(value, weight, f"Item_{i}"))

        capacity_test = size * 5

        # Непрерывный рюкзак
        start_time = time.perf_counter()
        GreedyAlgorithms.fractional_knapsack(capacity_test, test_items)
        end_time = time.perf_counter()
        fractional_times.append((end_time - start_time) * 1000)

        # 0-1 рюкзак (только для маленьких размеров)
        if size <= 20:
            start_time = time.perf_counter()
            KnapsackSolver.brute_force_01_knapsack(capacity_test, test_items)
            end_time = time.perf_counter()
            zero_one_times.append((end_time - start_time) * 1000)
        else:
            zero_one_times.append(None)

        print(f"  Размер {size}: непрерывный={fractional_times[-1]:.3f} мс, "
              f"0-1={zero_one_times[-1] if zero_one_times[-1] else 'N/A'} мс")

    return sizes, fractional_times, zero_one_times


def analyze_huffman_coding():
    """
    Анализ алгоритма Хаффмана.
    """
    print("\n=== АНАЛИЗ АЛГОРИТМА ХАФФМАНА ===\n")

    # Тестовые данные
    test_text = "this is an example for huffman encoding"

    print(f"Исходный текст: '{test_text}'")
    print(f"Длина текста: {len(test_text)} символов")
    print(f"Размер в ASCII: {len(test_text) * 8} бит")

    # Кодирование Хаффмана
    codes, encoded_text, tree = GreedyAlgorithms.huffman_coding(test_text)

    print(f"\nЗакодированный текст: {encoded_text}")
    print(f"Длина закодированного текста: {len(encoded_text)} бит")
    print(f"Коэффициент сжатия: {len(encoded_text) / (len(test_text) * 8):.2%}")

    print("\nКоды символов:")
    for char, code in sorted(codes.items()):
        print(f"  '{char}': {code}")

    # Визуализация дерева (простая текстовая)
    def print_tree(node, prefix="", is_left=True):
        if node is None:
            return ""

        result = ""
        if node.right:
            result += print_tree(node.right, prefix + ("│   " if is_left else "    "), False)

        char_repr = f"'{node.char}'" if node.char else "internal"
        result += prefix + ("└── " if is_left else "┌── ") + f"{char_repr}({node.freq})\n"

        if node.left:
            result += print_tree(node.left, prefix + ("    " if is_left else "│   "), True)

        return result

    print("\nДерево Хаффмана:")
    print(print_tree(tree))

    # Измерение производительности
    sizes = [100, 500, 1000, 5000, 10000]
    times = []
    compression_ratios = []

    print("\nИзмерение производительности:")
    for size in sizes:
        # Генерация случайного текста
        text = ''.join(random.choices(string.ascii_letters + string.digits + ' ', k=size))

        start_time = time.perf_counter()
        codes, encoded, _ = GreedyAlgorithms.huffman_coding(text)
        end_time = time.perf_counter()

        elapsed = (end_time - start_time) * 1000
        compression_ratio = len(encoded) / (len(text) * 8)

        times.append(elapsed)
        compression_ratios.append(compression_ratio)

        print(f"  Размер {size}: время={elapsed:.3f} мс, сжатие={compression_ratio:.2%}")

    return sizes, times, compression_ratios


def analyze_prim_algorithm():
    """
    Анализ алгоритма Прима.
    """
    print("\n=== АНАЛИЗ АЛГОРИТМА ПРИМА ===\n")

    # Простой тестовый граф
    vertices = ['A', 'B', 'C', 'D']
    edges = [
        ('A', 'B', 1),
        ('A', 'C', 3),
        ('B', 'C', 2),
        ('B', 'D', 4),
        ('C', 'D', 5),
    ]

    print("Граф:")
    for u, v, weight in edges:
        print(f"  {u} -- {v} (вес: {weight})")

    mst_edges = GreedyAlgorithms.prim_algorithm(vertices, edges)

    print("\nМинимальное остовное дерево (алгоритм Прима):")
    total_weight = 0
    for u, v, weight in mst_edges:
        print(f"  {u} -- {v} (вес: {weight})")
        total_weight += weight

    print(f"Общий вес MST: {total_weight}")

    return total_weight, mst_edges


def run_comprehensive_analysis():
    """
    Запуск комплексного анализа всех алгоритмов.
    """
    print("=== КОМПЛЕКСНЫЙ АНАЛИЗ ЖАДНЫХ АЛГОРИТМОВ ===\n")

    # Характеристики тестовой машины
    import platform
    import psutil

    print("Характеристики тестовой машины:")
    print(f"Процессор: {platform.processor()}")
    print(f"Память: {psutil.virtual_memory().total // (1024 ** 3)} GB")
    print(f"ОС: {platform.system()} {platform.release()}")
    print()

    # Запуск анализов
    interval_sizes, interval_times = analyze_interval_scheduling()
    knapsack_sizes, fractional_times, zero_one_times = analyze_knapsack_problems()
    huffman_sizes, huffman_times, compression_ratios = analyze_huffman_coding()
    mst_weight, mst_edges = analyze_prim_algorithm()

    # Построение графиков
    plt.figure(figsize=(15, 10))

    # График 1: Производительность алгоритмов
    plt.subplot(2, 2, 1)
    plt.plot(interval_sizes, interval_times, 'o-', label='Выбор заявок', linewidth=2)
    plt.plot(knapsack_sizes, fractional_times, 's-', label='Непрерывный рюкзак', linewidth=2)
    plt.plot(huffman_sizes[:len(huffman_times)], huffman_times, '^-', label='Хаффман', linewidth=2)

    # Добавляем 0-1 рюкзак только для доступных размеров
    available_sizes = [size for size, time_val in zip(knapsack_sizes, zero_one_times) if time_val is not None]
    available_times = [time_val for time_val in zero_one_times if time_val is not None]
    if available_sizes:
        plt.plot(available_sizes, available_times, 'd-', label='0-1 рюкзак (перебор)', linewidth=2)

    plt.xlabel('Размер входных данных')
    plt.ylabel('Время (миллисекунды)')
    plt.title('Производительность жадных алгоритмов')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.yscale('log')  # Логарифмическая шкала для наглядности

    # График 2: Эффективность сжатия Хаффмана
    plt.subplot(2, 2, 2)
    plt.plot(huffman_sizes, compression_ratios, 'o-', color='green', linewidth=2)
    plt.xlabel('Размер текста')
    plt.ylabel('Коэффициент сжатия')
    plt.title('Эффективность сжатия алгоритмом Хаффмана')
    plt.grid(True, alpha=0.3)

    # График 3: Сравнение непрерывного и 0-1 рюкзака
    plt.subplot(2, 2, 3)
    x_pos = range(len(knapsack_sizes))
    plt.bar([x - 0.2 for x in x_pos], fractional_times, 0.4, label='Непрерывный', alpha=0.8)

    # Только для доступных размеров
    zero_one_available = [t if t else 0 for t in zero_one_times]
    plt.bar([x + 0.2 for x in x_pos], zero_one_available, 0.4, label='0-1 (перебор)', alpha=0.8)

    plt.xlabel('Размер задачи')
    plt.ylabel('Время (миллисекунды)')
    plt.title('Сравнение времени решения задач о рюкзаке')
    plt.xticks(x_pos, knapsack_sizes)
    plt.legend()
    plt.grid(True, alpha=0.3)

    # График 4: Количество выбранных интервалов
    plt.subplot(2, 2, 4)
    # Генерируем данные для демонстрации
    demo_sizes = [10, 20, 50, 100]
    selected_counts = []

    for size in demo_sizes:
        test_intervals = []
        for i in range(size):
            start = random.randint(0, size * 2)
            end = start + random.randint(1, 10)
            test_intervals.append(Interval(start, end, f"Task_{i}"))

        selected = GreedyAlgorithms.interval_scheduling(test_intervals)
        selected_counts.append(len(selected))

    plt.plot(demo_sizes, selected_counts, 'o-', color='purple', linewidth=2)
    plt.xlabel('Общее количество интервалов')
    plt.ylabel('Количество выбранных интервалов')
    plt.title('Эффективность выбора заявок')
    plt.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('greedy_algorithms_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()

    print("\nАнализ завершен! Графики сохранены в 'greedy_algorithms_analysis.png'")


if __name__ == "__main__":
    random.seed(42)  # Для воспроизводимости результатов
    run_comprehensive_analysis()