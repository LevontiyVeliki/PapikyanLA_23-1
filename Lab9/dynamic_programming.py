"""
Реализация классических алгоритмов динамического программирования.
"""

import time
from functools import lru_cache
from typing import List, Tuple, Dict, Any
import sys


class FibonacciDP:
    """
    Реализации вычисления чисел Фибоначчи различными методами.
    """

    @staticmethod
    def fibonacci_naive(n: int) -> int:
        """
        Наивная рекурсивная реализация.

        Args:
            n: Номер числа Фибоначчи

        Returns:
            n-е число Фибоначчи

        Сложность: O(2^n) времени, O(n) памяти (глубина стека)
        """
        if n <= 1:
            return n
        return FibonacciDP.fibonacci_naive(n - 1) + FibonacciDP.fibonacci_naive(n - 2)

    @staticmethod
    def fibonacci_memo(n: int) -> int:
        """
        Рекурсивная реализация с мемоизацией (нисходящее ДП).
        Защита от глубокой рекурсии для больших n.

        Args:
            n: Номер числа Фибоначчи

        Returns:
            n-е число Фибоначчи

        Сложность: O(n) времени, O(n) памяти
        """
        # Увеличиваем лимит рекурсии для больших n
        if n > 1000:
            old_limit = sys.getrecursionlimit()
            sys.setrecursionlimit(max(old_limit, n + 100))

        @lru_cache(maxsize=None)
        def _fib_memo(x):
            if x <= 1:
                return x
            return _fib_memo(x - 1) + _fib_memo(x - 2)

        try:
            return _fib_memo(n)
        finally:
            # Восстанавливаем оригинальный лимит
            if n > 1000:
                sys.setrecursionlimit(old_limit)

    @staticmethod
    def fibonacci_bottom_up(n: int) -> int:
        """
        Итеративная реализация (восходящее ДП).

        Args:
            n: Номер числа Фибоначчи

        Returns:
            n-е число Фибоначчи

        Сложность: O(n) времени, O(n) памяти
        """
        if n <= 1:
            return n

        dp = [0] * (n + 1)
        dp[1] = 1

        for i in range(2, n + 1):
            dp[i] = dp[i - 1] + dp[i - 2]

        return dp[n]

    @staticmethod
    def fibonacci_optimized(n: int) -> int:
        """
        Оптимизированная версия с O(1) памятью.

        Args:
            n: Номер числа Фибоначчи

        Returns:
            n-е число Фибоначчи

        Сложность: O(n) времени, O(1) памяти
        """
        if n <= 1:
            return n

        prev, curr = 0, 1
        for _ in range(2, n + 1):
            prev, curr = curr, prev + curr

        return curr

    @staticmethod
    def fibonacci_matrix(n: int) -> int:
        """
        Вычисление с помощью матричного возведения в степень (O(log n)).

        Args:
            n: Номер числа Фибоначчи

        Returns:
            n-е число Фибоначчи

        Сложность: O(log n) времени, O(1) памяти
        """
        def matrix_mult(a: List[List[int]], b: List[List[int]]) -> List[List[int]]:
            return [
                [a[0][0]*b[0][0] + a[0][1]*b[1][0], a[0][0]*b[0][1] + a[0][1]*b[1][1]],
                [a[1][0]*b[0][0] + a[1][1]*b[1][0], a[1][0]*b[0][1] + a[1][1]*b[1][1]]
            ]

        def matrix_power(matrix: List[List[int]], power: int) -> List[List[int]]:
            result = [[1, 0], [0, 1]]  # Единичная матрица
            while power > 0:
                if power % 2 == 1:
                    result = matrix_mult(result, matrix)
                matrix = matrix_mult(matrix, matrix)
                power //= 2
            return result

        if n <= 1:
            return n

        base = [[1, 1], [1, 0]]
        result_matrix = matrix_power(base, n - 1)
        return result_matrix[0][0]


class KnapsackDP:
    """
    Реализация задачи о рюкзаке 0-1 с помощью динамического программирования.
    """

    @staticmethod
    def knapsack_01_bottom_up(weights: List[int], values: List[int], capacity: int) -> Tuple[int, List[int]]:
        """
        Решение задачи о рюкзаке 0-1 восходящим методом.

        Args:
            weights: Веса предметов
            values: Стоимости предметов
            capacity: Вместимость рюкзака

        Returns:
            tuple: (максимальная стоимость, список выбранных предметов)

        Сложность: O(n * W) времени, O(n * W) памяти
        """
        n = len(weights)
        # Создаем таблицу DP
        dp = [[0] * (capacity + 1) for _ in range(n + 1)]

        # Заполняем таблицу
        for i in range(1, n + 1):
            for w in range(1, capacity + 1):
                if weights[i-1] <= w:
                    dp[i][w] = max(dp[i-1][w], values[i-1] + dp[i-1][w - weights[i-1]])
                else:
                    dp[i][w] = dp[i-1][w]

        # Восстановление решения
        max_value = dp[n][capacity]
        selected_items = []
        w = capacity

        for i in range(n, 0, -1):
            if dp[i][w] != dp[i-1][w]:
                selected_items.append(i-1)
                w -= weights[i-1]

        selected_items.reverse()
        return max_value, selected_items

    @staticmethod
    def knapsack_01_optimized(weights: List[int], values: List[int], capacity: int) -> int:
        """
        Оптимизированная версия с O(W) памятью.

        Args:
            weights: Веса предметов
            values: Стоимости предметов
            capacity: Вместимость рюкзака

        Returns:
            int: Максимальная стоимость

        Сложность: O(n * W) времени, O(W) памяти
        """
        n = len(weights)
        dp = [0] * (capacity + 1)

        for i in range(n):
            # Проходим справа налево чтобы избежать перезаписи
            for w in range(capacity, weights[i] - 1, -1):
                dp[w] = max(dp[w], values[i] + dp[w - weights[i]])

        return dp[capacity]

    @staticmethod
    def knapsack_01_top_down(i: int, capacity: int, weights: Tuple[int], values: Tuple[int]) -> int:
        """
        Решение задачи о рюкзаке 0-1 нисходящим методом с мемоизацией.

        Args:
            i: Текущий индекс предмета
            capacity: Оставшаяся вместимость
            weights: Веса предметов (кортеж для хеширования)
            values: Стоимости предметов (кортеж для хеширования)

        Returns:
            int: Максимальная стоимость

        Сложность: O(n * W) времени, O(n * W) памяти
        """
        if i == 0 or capacity == 0:
            return 0

        if weights[i-1] > capacity:
            return KnapsackDP.knapsack_01_top_down(i-1, capacity, weights, values)

        return max(
            KnapsackDP.knapsack_01_top_down(i-1, capacity, weights, values),
            values[i-1] + KnapsackDP.knapsack_01_top_down(i-1, capacity - weights[i-1], weights, values)
        )


class LCSDP:
    """
    Реализация поиска наибольшей общей подпоследовательности.
    """

    @staticmethod
    def lcs_length(x: str, y: str) -> Tuple[int, List[List[int]]]:
        """
        Вычисление длины LCS и построение таблицы DP.

        Args:
            x: Первая строка
            y: Вторая строка

        Returns:
            tuple: (длина LCS, таблица DP)

        Сложность: O(m * n) времени и памяти
        """
        m, n = len(x), len(y)
        dp = [[0] * (n + 1) for _ in range(m + 1)]

        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if x[i-1] == y[j-1]:
                    dp[i][j] = dp[i-1][j-1] + 1
                else:
                    dp[i][j] = max(dp[i-1][j], dp[i][j-1])

        return dp[m][n], dp

    @staticmethod
    def lcs_sequence(x: str, y: str) -> str:
        """
        Восстановление самой LCS.

        Args:
            x: Первая строка
            y: Вторая строка

        Returns:
            str: Наибольшая общая подпоследовательность

        Сложность: O(m * n) времени и памяти
        """
        _, dp = LCSDP.lcs_length(x, y)
        m, n = len(x), len(y)
        lcs = []

        i, j = m, n
        while i > 0 and j > 0:
            if x[i-1] == y[j-1]:
                lcs.append(x[i-1])
                i -= 1
                j -= 1
            elif dp[i-1][j] > dp[i][j-1]:
                i -= 1
            else:
                j -= 1

        return ''.join(reversed(lcs))

    @staticmethod
    def lcs_optimized(x: str, y: str) -> int:
        """
        Оптимизированная версия с O(min(m, n)) памятью.

        Args:
            x: Первая строка
            y: Вторая строка

        Returns:
            int: Длина LCS

        Сложность: O(m * n) времени, O(min(m, n)) памяти
        """
        if len(x) < len(y):
            x, y = y, x  # Гарантируем, что y - более короткая строка

        m, n = len(x), len(y)
        prev = [0] * (n + 1)
        curr = [0] * (n + 1)

        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if x[i-1] == y[j-1]:
                    curr[j] = prev[j-1] + 1
                else:
                    curr[j] = max(prev[j], curr[j-1])
            prev, curr = curr, prev

        return prev[n]


class LevenshteinDP:
    """
    Реализация расстояния Левенштейна (редакционного расстояния).
    """

    @staticmethod
    def levenshtein_distance(s1: str, s2: str) -> Tuple[int, List[List[int]]]:
        """
        Вычисление расстояния Левенштейна между двумя строками.

        Args:
            s1: Первая строка
            s2: Вторая строка

        Returns:
            tuple: (расстояние, таблица DP)

        Сложность: O(m * n) времени и памяти
        """
        m, n = len(s1), len(s2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]

        # Инициализация
        for i in range(m + 1):
            dp[i][0] = i
        for j in range(n + 1):
            dp[0][j] = j

        # Заполнение таблицы
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if s1[i-1] == s2[j-1]:
                    dp[i][j] = dp[i-1][j-1]
                else:
                    dp[i][j] = min(
                        dp[i-1][j] + 1,    # Удаление
                        dp[i][j-1] + 1,    # Вставка
                        dp[i-1][j-1] + 1   # Замена
                    )

        return dp[m][n], dp

    @staticmethod
    def levenshtein_optimized(s1: str, s2: str) -> int:
        """
        Оптимизированная версия с O(min(m, n)) памятью.

        Args:
            s1: Первая строка
            s2: Вторая строка

        Returns:
            int: Расстояние Левенштейна

        Сложность: O(m * n) времени, O(min(m, n)) памяти
        """
        if len(s1) < len(s2):
            s1, s2 = s2, s1

        m, n = len(s1), len(s2)
        prev = list(range(n + 1))
        curr = [0] * (n + 1)

        for i in range(1, m + 1):
            curr[0] = i
            for j in range(1, n + 1):
                if s1[i-1] == s2[j-1]:
                    curr[j] = prev[j-1]
                else:
                    curr[j] = min(prev[j] + 1, curr[j-1] + 1, prev[j-1] + 1)
            prev, curr = curr, prev

        return prev[n]


class CoinChangeDP:
    """
    Реализация задачи о размене монет.
    """

    @staticmethod
    def coin_change_min_coins(coins: List[int], amount: int) -> int:
        """
        Минимальное количество монет для размена суммы.

        Args:
            coins: Доступные номиналы монет
            amount: Сумма для размена

        Returns:
            int: Минимальное количество монет или -1 если невозможно

        Сложность: O(n * amount) времени, O(amount) памяти
        """
        dp = [float('inf')] * (amount + 1)
        dp[0] = 0

        for coin in coins:
            for i in range(coin, amount + 1):
                dp[i] = min(dp[i], dp[i - coin] + 1)

        return dp[amount] if dp[amount] != float('inf') else -1

    @staticmethod
    def coin_change_ways(coins: List[int], amount: int) -> int:
        """
        Количество способов размена суммы.

        Args:
            coins: Доступные номиналы монет
            amount: Сумма для размена

        Returns:
            int: Количество способов размена

        Сложность: O(n * amount) времени, O(amount) памяти
        """
        dp = [0] * (amount + 1)
        dp[0] = 1

        for coin in coins:
            for i in range(coin, amount + 1):
                dp[i] += dp[i - coin]

        return dp[amount]


class LISDP:
    """
    Реализация поиска наибольшей возрастающей подпоследовательности.
    """

    @staticmethod
    def longest_increasing_subsequence(nums: List[int]) -> Tuple[int, List[int]]:
        """
        Поиск наибольшей возрастающей подпоследовательности.

        Args:
            nums: Последовательность чисел

        Returns:
            tuple: (длина LIS, сама подпоследовательность)

        Сложность: O(n^2) времени, O(n) памяти
        """
        if not nums:
            return 0, []

        n = len(nums)
        dp = [1] * n  # dp[i] - длина LIS, заканчивающейся на nums[i]
        prev = [-1] * n  # Для восстановления последовательности

        for i in range(n):
            for j in range(i):
                if nums[j] < nums[i] and dp[j] + 1 > dp[i]:
                    dp[i] = dp[j] + 1
                    prev[i] = j

        # Находим максимальную длину и её позицию
        max_length = max(dp)
        max_index = dp.index(max_length)

        # Восстанавливаем последовательность
        lis = []
        while max_index != -1:
            lis.append(nums[max_index])
            max_index = prev[max_index]

        return max_length, lis[::-1]

    @staticmethod
    def lis_optimized(nums: List[int]) -> int:
        """
        Оптимизированная версия с O(n log n) временем.

        Args:
            nums: Последовательность чисел

        Returns:
            int: Длина LIS

        Сложность: O(n log n) времени, O(n) памяти
        """
        if not nums:
            return 0

        tails = []
        for num in nums:
            # Бинарный поиск позиции для вставки
            left, right = 0, len(tails)
            while left < right:
                mid = (left + right) // 2
                if tails[mid] < num:
                    left = mid + 1
                else:
                    right = mid

            if left == len(tails):
                tails.append(num)
            else:
                tails[left] = num

        return len(tails)


class DPVisualizer:
    """
    Класс для визуализации таблиц динамического программирования.
    """

    @staticmethod
    def print_dp_table(dp: List[List[Any]], row_labels: List[str] = None,
                      col_labels: List[str] = None, title: str = "DP Table"):
        """
        Красивая печать таблицы DP.

        Args:
            dp: Таблица DP
            row_labels: Метки строк
            col_labels: Метки столбцов
            title: Заголовок таблицы
        """
        print(f"\n{title}")
        print("=" * 50)

        if col_labels:
            print("     " + " ".join(f"{label:>5}" for label in col_labels))
            print("    " + "-" * (6 * len(col_labels)))

        for i, row in enumerate(dp):
            prefix = f"{row_labels[i]:>3} |" if row_labels else "    "
            print(prefix + " ".join(f"{cell:>5}" for cell in row))

    @staticmethod
    def visualize_knapsack_dp(weights: List[int], values: List[int], capacity: int):
        """Визуализация таблицы DP для задачи о рюкзаке."""
        n = len(weights)
        dp = [[0] * (capacity + 1) for _ in range(n + 1)]

        # Заполняем таблицу
        for i in range(1, n + 1):
            for w in range(1, capacity + 1):
                if weights[i-1] <= w:
                    dp[i][w] = max(dp[i-1][w], values[i-1] + dp[i-1][w - weights[i-1]])
                else:
                    dp[i][w] = dp[i-1][w]

        col_labels = [str(i) for i in range(capacity + 1)]
        row_labels = ["0"] + [f"i={i}" for i in range(1, n + 1)]

        DPVisualizer.print_dp_table(dp, row_labels, col_labels, "Knapsack DP Table")

        return dp