"""
Демонстрация работы алгоритмов динамического программирования на практических примерах.
"""

from dynamic_programming import *
import time


def demonstrate_fibonacci():
    """Демонстрация вычисления чисел Фибоначчи."""
    print("=== ДЕМОНСТРАЦИЯ: ЧИСЛА ФИБОНАЧЧИ ===\n")

    n = 30
    print(f"Вычисление F({n}) различными методами:")

    # Наивный метод (только для демонстрации)
    if n <= 35:
        start = time.perf_counter()
        result_naive = FibonacciDP.fibonacci_naive(n)
        time_naive = time.perf_counter() - start
        print(f"  Наивный рекурсивный: {result_naive} ({time_naive:.6f} сек)")

    # Мемоизация
    FibonacciDP.fibonacci_memo.cache_clear()
    start = time.perf_counter()
    result_memo = FibonacciDP.fibonacci_memo(n)
    time_memo = time.perf_counter() - start
    print(f"  С мемоизацией: {result_memo} ({time_memo:.6f} сек)")

    # Восходящий ДП
    start = time.perf_counter()
    result_bottom_up = FibonacciDP.fibonacci_bottom_up(n)
    time_bottom_up = time.perf_counter() - start
    print(f"  Восходящий ДП: {result_bottom_up} ({time_bottom_up:.6f} сек)")

    # Оптимизированный
    start = time.perf_counter()
    result_optimized = FibonacciDP.fibonacci_optimized(n)
    time_optimized = time.perf_counter() - start
    print(f"  Оптимизированный: {result_optimized} ({time_optimized:.6f} сек)")

    # Матричный
    start = time.perf_counter()
    result_matrix = FibonacciDP.fibonacci_matrix(n)
    time_matrix = time.perf_counter() - start
    print(f"  Матричный: {result_matrix} ({time_matrix:.6f} сек)")

    # Демонстрация для больших n
    print(f"\nF(100) = {FibonacciDP.fibonacci_optimized(100)}")
    print(f"F(1000) = ... (очень большое число)")


def demonstrate_knapsack():
    """Демонстрация задачи о рюкзаке."""
    print("\n=== ДЕМОНСТРАЦИЯ: ЗАДАЧА О РЮКЗАКЕ 0-1 ===\n")

    weights = [2, 3, 4, 5, 9]
    values = [3, 4, 5, 8, 10]
    capacity = 20

    print("Предметы:")
    for i, (w, v) in enumerate(zip(weights, values)):
        print(f"  Предмет {i}: вес={w}, стоимость={v}, удельная стоимость={v / w:.2f}")

    print(f"\nВместимость рюкзака: {capacity}")

    max_value, selected_items = KnapsackDP.knapsack_01_bottom_up(weights, values, capacity)

    print(f"\nМаксимальная стоимость: {max_value}")
    print("Выбранные предметы:")
    total_weight = 0
    for idx in selected_items:
        print(f"  Предмет {idx}: вес {weights[idx]}, стоимость {values[idx]}")
        total_weight += weights[idx]

    print(f"Общий вес: {total_weight}")

    # Визуализация таблицы ДП для упрощенного случая
    print("\nВизуализация таблицы ДП для меньшего примера:")
    small_weights = [2, 3, 4]
    small_values = [3, 4, 5]
    small_capacity = 5

    DPVisualizer.visualize_knapsack_dp(small_weights, small_values, small_capacity)


def demonstrate_lcs():
    """Демонстрация поиска наибольшей общей подпоследовательности."""
    print("\n=== ДЕМОНСТРАЦИЯ: НАИБОЛЬШАЯ ОБЩАЯ ПОДПОСЛЕДОВАТЕЛЬНОСТЬ ===\n")

    x = "ABCDGH"
    y = "AEDFHR"

    print(f"Строка 1: '{x}'")
    print(f"Строка 2: '{y}'")

    length, dp_table = LCSDP.lcs_length(x, y)
    sequence = LCSDP.lcs_sequence(x, y)

    print(f"Длина LCS: {length}")
    print(f"LCS: '{sequence}'")

    # Визуализация таблицы ДП
    print("\nТаблица ДП для LCS:")
    row_labels = [''] + list(x)
    col_labels = [''] + list(y)
    DPVisualizer.print_dp_table(dp_table, row_labels, col_labels, "LCS DP Table")

    # Практический пример
    print("\nПрактический пример:")
    dna1 = "ACCGGTCGAGTGCGCGGAAGCCGGCCGAA"
    dna2 = "GTCGTTCGGAATGCCGTTGCTCTGTAAA"

    lcs_length_result = LCSDP.lcs_optimized(dna1, dna2)
    print(f"Длина LCS для DNA последовательностей: {lcs_length_result}")


def demonstrate_levenshtein():
    """Демонстрация расстояния Левенштейна."""
    print("\n=== ДЕМОНСТРАЦИЯ: РАССТОЯНИЕ ЛЕВЕНШТЕЙНА ===\n")

    s1 = "kitten"
    s2 = "sitting"

    print(f"Строка 1: '{s1}'")
    print(f"Строка 2: '{s2}'")

    distance, dp_table = LevenshteinDP.levenshtein_distance(s1, s2)

    print(f"Редакционное расстояние: {distance}")
    print("Операции:")
    print("  k → s (замена)")
    print("  - (вставка i)")
    print("  e → i (замена)")
    print("  - (вставка g)")

    # Визуализация таблицы ДП
    print("\nТаблица ДП для расстояния Левенштейна:")
    row_labels = [''] + list(s1)
    col_labels = [''] + list(s2)
    DPVisualizer.print_dp_table(dp_table, row_labels, col_labels, "Levenshtein DP Table")

    # Практический пример
    print("\nПрактический пример (проверка орфографии):")
    word = "accomodation"
    corrections = ["accommodation", "accomodation", "acumodation"]

    for correction in corrections:
        dist = LevenshteinDP.levenshtein_optimized(word, correction)
        print(f"  '{word}' → '{correction}': расстояние = {dist}")


def demonstrate_coin_change():
    """Демонстрация задачи о размене монет."""
    print("\n=== ДЕМОНСТРАЦИЯ: ЗАДАЧА О РАЗМЕНЕ МОНЕТ ===\n")

    coins = [1, 2, 5, 10, 20, 50]
    amount = 137

    print(f"Доступные монеты: {coins}")
    print(f"Сумма для размена: {amount}")

    min_coins = CoinChangeDP.coin_change_min_coins(coins, amount)
    ways = CoinChangeDP.coin_change_ways(coins, amount)

    print(f"Минимальное количество монет: {min_coins}")
    print(f"Количество способов размена: {ways}")

    # Восстановление решения для минимального количества
    if min_coins != -1:
        print("Оптимальный размен:")
        remaining = amount
        coin_count = {}

        for coin in sorted(coins, reverse=True):
            count = remaining // coin
            if count > 0:
                coin_count[coin] = count
                remaining -= coin * count

        for coin, count in sorted(coin_count.items()):
            print(f"  Монета {coin}: {count} шт")


def demonstrate_lis():
    """Демонстрация поиска наибольшей возрастающей подпоследовательности."""
    print("\n=== ДЕМОНСТРАЦИЯ: НАИБОЛЬШАЯ ВОЗРАСТАЮЩАЯ ПОДПОСЛЕДОВАТЕЛЬНОСТЬ ===\n")

    # Пример с ценами акций
    prices = [100, 113, 110, 85, 105, 102, 86, 63, 81, 101, 94, 106, 101, 79, 94, 90, 97]

    print("История цен акций:")
    for i, price in enumerate(prices):
        print(f"  День {i + 1:2}: ${price}")

    length, sequence = LISDP.longest_increasing_subsequence(prices)

    print(f"\nНаибольшая возрастающая подпоследовательность:")
    print(f"  Длина: {length}")
    print(f"  Последовательность: {sequence}")

    # Поиск наибольшего роста
    max_increase = 0
    best_start = 0
    best_end = 0

    for i in range(len(prices)):
        for j in range(i + 1, len(prices)):
            increase = prices[j] - prices[i]
            if increase > max_increase:
                max_increase = increase
                best_start = i
                best_end = j

    print(f"\nНаибольший рост: ${prices[best_start]} → ${prices[best_end]} "
          f"(прибыль: ${max_increase})")


def demonstrate_dp_optimization():
    """Демонстрация оптимизации использования памяти."""
    print("\n=== ДЕМОНСТРАЦИЯ: ОПТИМИЗАЦИЯ ПАМЯТИ В ДП ===\n")

    # Сравнение оптимизированных и неоптимизированных версий
    print("Сравнение использования памяти:")

    # Рюкзак
    weights = [i % 10 + 1 for i in range(100)]
    values = [i * 2 + 1 for i in range(100)]
    capacity = 200

    print("Задача о рюкзаке:")
    print("  Стандартная версия: O(n*W) память")
    print("  Оптимизированная версия: O(W) память")

    # LCS
    str1 = "A" * 1000 + "B" * 1000
    str2 = "B" * 1000 + "A" * 1000

    print("\nЗадача LCS:")
    print("  Стандартная версия: O(m*n) память")
    print("  Оптимизированная версия: O(min(m,n)) память")

    # Фибоначчи
    print("\nЧисла Фибоначчи:")
    print("  Наивная рекурсия: O(n) память (стек)")
    print("  Мемоизация: O(n) память")
    print("  Восходящий ДП: O(n) память")
    print("  Оптимизированный: O(1) память")
    print("  Матричный: O(1) память")


if __name__ == "__main__":
    demonstrate_fibonacci()
    demonstrate_knapsack()
    demonstrate_lcs()
    demonstrate_levenshtein()
    demonstrate_coin_change()
    demonstrate_lis()
    demonstrate_dp_optimization()