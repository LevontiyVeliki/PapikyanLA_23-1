"""
Unit-тесты для проверки корректности алгоритмов динамического программирования.
"""

import unittest
from dynamic_programming import *


class TestFibonacciDP(unittest.TestCase):
    """Тесты для вычисления чисел Фибоначчи."""

    def test_fibonacci_base_cases(self):
        """Тест базовых случаев."""
        self.assertEqual(FibonacciDP.fibonacci_naive(0), 0)
        self.assertEqual(FibonacciDP.fibonacci_naive(1), 1)
        self.assertEqual(FibonacciDP.fibonacci_memo(0), 0)
        self.assertEqual(FibonacciDP.fibonacci_memo(1), 1)
        self.assertEqual(FibonacciDP.fibonacci_bottom_up(0), 0)
        self.assertEqual(FibonacciDP.fibonacci_bottom_up(1), 1)
        self.assertEqual(FibonacciDP.fibonacci_optimized(0), 0)
        self.assertEqual(FibonacciDP.fibonacci_optimized(1), 1)
        self.assertEqual(FibonacciDP.fibonacci_matrix(0), 0)
        self.assertEqual(FibonacciDP.fibonacci_matrix(1), 1)

    def test_fibonacci_consistency(self):
        """Тест согласованности различных методов."""
        test_values = [2, 5, 10, 15]

        for n in test_values:
            with self.subTest(n=n):
                naive = FibonacciDP.fibonacci_naive(n)
                memo = FibonacciDP.fibonacci_memo(n)
                bottom_up = FibonacciDP.fibonacci_bottom_up(n)
                optimized = FibonacciDP.fibonacci_optimized(n)
                matrix = FibonacciDP.fibonacci_matrix(n)

                self.assertEqual(naive, memo)
                self.assertEqual(memo, bottom_up)
                self.assertEqual(bottom_up, optimized)
                self.assertEqual(optimized, matrix)


class TestKnapsackDP(unittest.TestCase):
    """Тесты для задачи о рюкзаке."""

    def test_knapsack_basic(self):
        """Базовый тест рюкзака."""
        weights = [1, 3, 4, 5]
        values = [1, 4, 5, 7]
        capacity = 7

        max_value, selected = KnapsackDP.knapsack_01_bottom_up(weights, values, capacity)

        self.assertEqual(max_value, 9)
        self.assertEqual(set(selected), {1, 2})  # Предметы с индексами 1 и 2

    def test_knapsack_empty(self):
        """Тест пустого рюкзака."""
        weights = []
        values = []
        capacity = 10

        max_value, selected = KnapsackDP.knapsack_01_bottom_up(weights, values, capacity)

        self.assertEqual(max_value, 0)
        self.assertEqual(selected, [])

    def test_knapsack_optimized_consistency(self):
        """Тест согласованности оптимизированной версии."""
        weights = [2, 3, 4, 5]
        values = [3, 4, 5, 6]
        capacity = 5

        bottom_up_value, _ = KnapsackDP.knapsack_01_bottom_up(weights, values, capacity)
        optimized_value = KnapsackDP.knapsack_01_optimized(weights, values, capacity)

        self.assertEqual(bottom_up_value, optimized_value)


class TestLCSDP(unittest.TestCase):
    """Тесты для наибольшей общей подпоследовательности."""

    def test_lcs_basic(self):
        """Базовый тест LCS."""
        x = "ABCDGH"
        y = "AEDFHR"

        length, _ = LCSDP.lcs_length(x, y)
        sequence = LCSDP.lcs_sequence(x, y)

        self.assertEqual(length, 3)
        self.assertEqual(sequence, "ADH")

    def test_lcs_empty(self):
        """Тест пустых строк."""
        x = ""
        y = "ABC"

        length, _ = LCSDP.lcs_length(x, y)
        sequence = LCSDP.lcs_sequence(x, y)

        self.assertEqual(length, 0)
        self.assertEqual(sequence, "")

    def test_lcs_identical(self):
        """Тест идентичных строк."""
        x = "ABCD"
        y = "ABCD"

        length, _ = LCSDP.lcs_length(x, y)
        sequence = LCSDP.lcs_sequence(x, y)

        self.assertEqual(length, 4)
        self.assertEqual(sequence, "ABCD")


class TestLevenshteinDP(unittest.TestCase):
    """Тесты для расстояния Левенштейна."""

    def test_levenshtein_basic(self):
        """Базовый тест расстояния Левенштейна."""
        s1 = "kitten"
        s2 = "sitting"

        distance, _ = LevenshteinDP.levenshtein_distance(s1, s2)

        self.assertEqual(distance, 3)

    def test_levenshtein_identical(self):
        """Тест идентичных строк."""
        s1 = "abc"
        s2 = "abc"

        distance, _ = LevenshteinDP.levenshtein_distance(s1, s2)

        self.assertEqual(distance, 0)

    def test_levenshtein_empty(self):
        """Тест пустых строк."""
        s1 = ""
        s2 = "abc"

        distance, _ = LevenshteinDP.levenshtein_distance(s1, s2)

        self.assertEqual(distance, 3)


class TestCoinChangeDP(unittest.TestCase):
    """Тесты для задачи о размене монет."""

    def test_coin_change_min_coins(self):
        """Тест минимального количества монет."""
        coins = [1, 2, 5]
        amount = 11

        result = CoinChangeDP.coin_change_min_coins(coins, amount)

        self.assertEqual(result, 3)  # 5 + 5 + 1

    def test_coin_change_impossible(self):
        """Тест невозможного размена."""
        coins = [2, 5]
        amount = 3

        result = CoinChangeDP.coin_change_min_coins(coins, amount)

        self.assertEqual(result, -1)

    def test_coin_change_ways(self):
        """Тест количества способов размена."""
        coins = [1, 2, 5]
        amount = 5

        result = CoinChangeDP.coin_change_ways(coins, amount)

        self.assertEqual(result, 4)  # 5, 2+2+1, 2+1+1+1, 1+1+1+1+1


class TestLISDP(unittest.TestCase):
    """Тесты для наибольшей возрастающей подпоследовательности."""

    def test_lis_basic(self):
        """Базовый тест LIS."""
        nums = [10, 9, 2, 5, 3, 7, 101, 18]

        length, sequence = LISDP.longest_increasing_subsequence(nums)

        self.assertEqual(length, 4)
        self.assertEqual(sequence, [2, 5, 7, 101])

    def test_lis_sorted(self):
        """Тест отсортированной последовательности."""
        nums = [1, 2, 3, 4, 5]

        length, sequence = LISDP.longest_increasing_subsequence(nums)

        self.assertEqual(length, 5)
        self.assertEqual(sequence, [1, 2, 3, 4, 5])

    def test_lis_optimized_consistency(self):
        """Тест согласованности оптимизированной версии."""
        nums = [10, 9, 2, 5, 3, 7, 101, 18]

        length_dp, _ = LISDP.longest_increasing_subsequence(nums)
        length_optimized = LISDP.lis_optimized(nums)

        self.assertEqual(length_dp, length_optimized)


if __name__ == "__main__":
    unittest.main()