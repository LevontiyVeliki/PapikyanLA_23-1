"""
Unit-тесты для проверки корректности жадных алгоритмов.
"""

import unittest
from greedy_algorithms import GreedyAlgorithms, KnapsackSolver, Interval, Item


class TestGreedyAlgorithms(unittest.TestCase):
    """Тесты жадных алгоритмов."""

    def test_interval_scheduling(self):
        """Тест задачи о выборе заявок."""
        intervals = [
            Interval(1, 3, "A"),
            Interval(2, 5, "B"),
            Interval(4, 7, "C"),
            Interval(6, 9, "D"),
            Interval(8, 10, "E"),
        ]

        selected = GreedyAlgorithms.interval_scheduling(intervals)

        # Проверяем, что интервалы не пересекаются
        for i in range(len(selected) - 1):
            self.assertLessEqual(selected[i].end, selected[i + 1].start)

        # Проверяем количество выбранных интервалов
        self.assertEqual(len(selected), 3)  # A, C, E

    def test_fractional_knapsack(self):
        """Тест непрерывного рюкзака."""
        items = [
            Item(60, 10, "Item1"),
            Item(100, 20, "Item2"),
            Item(120, 30, "Item3"),
        ]
        capacity = 50

        value, selection = GreedyAlgorithms.fractional_knapsack(capacity, items)

        # Проверяем, что стоимость корректна
        expected_value = 60 + 100 + (120 * 20 / 30)  # 60 + 100 + 80 = 240
        self.assertAlmostEqual(value, expected_value, places=2)

        # Проверяем, что вес не превышает вместимость
        total_weight = 0
        for item, fraction in selection:
            total_weight += item.weight * fraction

        self.assertLessEqual(total_weight, capacity)

    def test_huffman_coding(self):
        """Тест алгоритма Хаффмана."""
        text = "abracadabra"

        codes, encoded, tree = GreedyAlgorithms.huffman_coding(text)

        # Проверяем, что все символы имеют коды
        unique_chars = set(text)
        self.assertEqual(set(codes.keys()), unique_chars)

        # Проверяем, что коды являются префиксными
        all_codes = list(codes.values())
        for i, code1 in enumerate(all_codes):
            for j, code2 in enumerate(all_codes):
                if i != j:
                    self.assertFalse(code1.startswith(code2))
                    self.assertFalse(code2.startswith(code1))

        # Проверяем, что можно декодировать
        decoded_chars = []
        current_code = ""
        for bit in encoded:
            current_code += bit
            if current_code in codes.values():
                for char, code in codes.items():
                    if code == current_code:
                        decoded_chars.append(char)
                        current_code = ""
                        break

        decoded_text = "".join(decoded_chars)
        self.assertEqual(decoded_text, text)

    def test_coin_change(self):
        """Тест задачи о сдаче."""
        coins = [25, 10, 5, 1]  # Американская система
        amount = 67

        result = GreedyAlgorithms.coin_change(amount, coins)

        # Проверяем сумму
        total = sum(coin * count for coin, count in result.items())
        self.assertEqual(total, amount)

        # Проверяем оптимальность для канонической системы
        total_coins = sum(result.values())
        self.assertEqual(total_coins, 6)  # 2*25 + 1*10 + 1*5 + 2*1 = 6 монет

    def test_prim_algorithm(self):
        """Тест алгоритма Прима."""
        vertices = ['A', 'B', 'C', 'D']
        edges = [
            ('A', 'B', 1),
            ('A', 'C', 3),
            ('B', 'C', 2),
            ('B', 'D', 4),
            ('C', 'D', 5),
        ]

        mst_edges = GreedyAlgorithms.prim_algorithm(vertices, edges)

        # Проверяем количество ребер в MST
        self.assertEqual(len(mst_edges), len(vertices) - 1)

        # Проверяем общий вес
        total_weight = sum(weight for _, _, weight in mst_edges)
        self.assertEqual(total_weight, 7)  # 1 + 2 + 4 = 7

        # Проверяем, что все вершины соединены
        connected_vertices = set()
        for u, v, _ in mst_edges:
            connected_vertices.add(u)
            connected_vertices.add(v)

        self.assertEqual(connected_vertices, set(vertices))


class TestKnapsackSolver(unittest.TestCase):
    """Тесты решателя задач о рюкзаке."""

    def test_brute_force_01_knapsack(self):
        """Тест точного решения 0-1 рюкзака."""
        items = [
            Item(60, 10, "Item1"),
            Item(100, 20, "Item2"),
            Item(120, 30, "Item3"),
        ]
        capacity = 50

        value, selection = KnapsackSolver.brute_force_01_knapsack(capacity, items)

        # Проверяем, что вес не превышает вместимость
        total_weight = sum(item.weight for item in selection)
        self.assertLessEqual(total_weight, capacity)

        # Проверяем оптимальность
        self.assertEqual(value, 220)  # Item2 + Item3 = 100 + 120 = 220

    def test_knapsack_comparison(self):
        """Тест сравнения методов."""
        items = [
            Item(60, 10, "Item1"),
            Item(100, 20, "Item2"),
        ]
        capacity = 25

        greedy_val, exact_val = KnapsackSolver.compare_knapsack_methods(capacity, items)

        # Для этого примера оба метода должны дать одинаковый результат
        self.assertAlmostEqual(greedy_val, exact_val, places=2)


if __name__ == "__main__":
    unittest.main()