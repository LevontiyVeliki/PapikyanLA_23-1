"""
Unit-тесты для проверки корректности алгоритмов на строках.
"""

import unittest
from prefix_function import PrefixFunction, NaiveStringSearch
from z_function import ZFunction
from string_matching import BoyerMoore, RabinKarp, StringAlgorithmsComparison


class TestPrefixFunction(unittest.TestCase):
    """Тесты префикс-функции и алгоритма KMP."""

    def test_prefix_function_basic(self):
        """Базовые тесты префикс-функции."""
        test_cases = [
            ("abcabcd", [0, 0, 0, 1, 2, 3, 0]),
            ("aabaabaaa", [0, 1, 0, 1, 2, 3, 4, 5, 2]),
            ("abacaba", [0, 0, 1, 0, 1, 2, 3]),
            ("", []),
            ("a", [0]),
        ]

        for pattern, expected in test_cases:
            with self.subTest(pattern=pattern):
                result = PrefixFunction.compute_prefix_function(pattern)
                self.assertEqual(result, expected)

    def test_kmp_search(self):
        """Тесты алгоритма KMP."""
        text = "ababcabcabababd"
        pattern = "ababd"

        result = PrefixFunction.kmp_search(text, pattern)
        self.assertEqual(result, [10])

        # Несколько вхождений
        result = PrefixFunction.kmp_search("abcabcabc", "abc")
        self.assertEqual(result, [0, 3, 6])

        # Отсутствие паттерна
        result = PrefixFunction.kmp_search("abcdef", "xyz")
        self.assertEqual(result, [])

        # Пустой паттерн
        result = PrefixFunction.kmp_search("abc", "")
        self.assertEqual(result, [0, 1, 2, 3])

    def test_period_detection(self):
        """Тесты поиска периода строки."""
        test_cases = [
            ("abcabcabc", 3),
            ("aaaa", 1),
            ("ababab", 2),
            ("abcde", 0),  # Непериодическая
            ("a", 1),
        ]

        for string, expected_period in test_cases:
            with self.subTest(string=string):
                result = PrefixFunction.find_period(string)
                self.assertEqual(result, expected_period)

    def test_rotation_check(self):
        """Тесты проверки циклического сдвига."""
        self.assertTrue(PrefixFunction.is_rotation("abcde", "cdeab"))
        self.assertTrue(PrefixFunction.is_rotation("abcde", "eabcd"))
        self.assertFalse(PrefixFunction.is_rotation("abc", "abd"))
        self.assertFalse(PrefixFunction.is_rotation("abc", "abcd"))


class TestZFunction(unittest.TestCase):
    """Тесты Z-функции."""

    def test_z_function_basic(self):
        """Базовые тесты Z-функции."""
        test_cases = [
            ("aaa", [3, 2, 1]),
            ("abcabc", [6, 0, 0, 3, 0, 0]),
            ("aabaab", [6, 1, 0, 3, 1, 0]),
            ("", []),
            ("a", [1]),
        ]

        for string, expected in test_cases:
            with self.subTest(string=string):
                result = ZFunction.compute_z_function(string)
                self.assertEqual(result, expected)

    def test_z_search(self):
        """Тесты поиска с использованием Z-функции."""
        text = "ababcabcabababd"
        pattern = "ababd"

        result = ZFunction.z_search(text, pattern)
        self.assertEqual(result, [10])

        # Несколько вхождений
        result = ZFunction.z_search("abcabcabc", "abc")
        self.assertEqual(result, [0, 3, 6])

        # Отсутствие паттерна
        result = ZFunction.z_search("abcdef", "xyz")
        self.assertEqual(result, [])

    def test_distinct_substrings(self):
        """Тесты подсчета различных подстрок."""
        self.assertEqual(ZFunction.find_distinct_substrings_count("aaa"), 3)
        self.assertEqual(ZFunction.find_distinct_substrings_count("abc"), 6)
        self.assertEqual(ZFunction.find_distinct_substrings_count("ab"), 3)
        self.assertEqual(ZFunction.find_distinct_substrings_count(""), 0)


class TestBoyerMoore(unittest.TestCase):
    """Тесты алгоритма Бойера-Мура."""

    def test_bad_char_table(self):
        """Тесты таблицы плохого символа."""
        table = BoyerMoore.build_bad_char_table("abc")
        self.assertEqual(table.get('a', 3), 2)
        self.assertEqual(table.get('b', 3), 1)
        self.assertEqual(table.get('c', 3), 3)  # Для последнего символа не сохраняем
        self.assertEqual(table.get('x', 3), 3)

    def test_boyer_moore_search(self):
        """Тесты алгоритма Бойера-Мура."""
        text = "ababcabcabababd"
        pattern = "ababd"

        result = BoyerMoore.boyer_moore_search(text, pattern)
        self.assertEqual(result, [10])

        # Несколько вхождений
        result = BoyerMoore.boyer_moore_search("abcabcabc", "abc")
        self.assertEqual(result, [0, 3, 6])

        # Отсутствие паттерна
        result = BoyerMoore.boyer_moore_search("abcdef", "xyz")
        self.assertEqual(result, [])


class TestRabinKarp(unittest.TestCase):
    """Тесты алгоритма Рабина-Карпа."""

    def test_polynomial_hash(self):
        """Тесты полиномиального хеширования."""
        hash1 = RabinKarp.polynomial_hash("abc")
        hash2 = RabinKarp.polynomial_hash("abc")
        hash3 = RabinKarp.polynomial_hash("abd")

        self.assertEqual(hash1, hash2)
        self.assertNotEqual(hash1, hash3)

    def test_rabin_karp_search(self):
        """Тесты алгоритма Рабина-Карпа."""
        text = "ababcabcabababd"
        pattern = "ababd"

        result = RabinKarp.rabin_karp_search(text, pattern)
        self.assertEqual(result, [10])

        # Несколько вхождений
        result = RabinKarp.rabin_karp_search("abcabcabc", "abc")
        self.assertEqual(result, [0, 3, 6])

        # Отсутствие паттерна
        result = RabinKarp.rabin_karp_search("abcdef", "xyz")
        self.assertEqual(result, [])

    def test_multiple_patterns(self):
        """Тесты поиска нескольких паттернов."""
        text = "abcde fghij abc fgh"
        patterns = ["abc", "fgh"]

        result = RabinKarp.rabin_karp_multiple_patterns(text, patterns)

        self.assertEqual(result["abc"], [0, 11])
        self.assertEqual(result["fgh"], [6, 15])


class TestAlgorithmsComparison(unittest.TestCase):
    """Тесты сравнения алгоритмов."""

    def test_algorithms_consistency(self):
        """Тест согласованности результатов всех алгоритмов."""
        test_cases = [
            ("ababcabcabababd", "ababd"),
            ("abcabcabc", "abc"),
            ("abcdef", "xyz"),
            ("abc", ""),
            ("aaa", "aa"),
        ]

        for text, pattern in test_cases:
            with self.subTest(text=text, pattern=pattern):
                results = StringAlgorithmsComparison.compare_algorithms(text, pattern)
                is_consistent = StringAlgorithmsComparison.verify_results(results)
                self.assertTrue(is_consistent, f"Несогласованность для text='{text}', pattern='{pattern}'")


class TestPerformanceScenarios(unittest.TestCase):
    """Тесты производительности в различных сценариях."""

    def test_worst_case_naive(self):
        """Тест худшего случая для наивного алгоритма."""
        # Худший случай: текст "aaa...a", паттерн "aaa...b"
        text = "a" * 1000
        pattern = "a" * 500 + "b"

        # Должен работать быстрее с KMP
        import time
        start = time.perf_counter()
        PrefixFunction.kmp_search(text, pattern)
        kmp_time = time.perf_counter() - start

        start = time.perf_counter()
        NaiveStringSearch.naive_search(text, pattern)
        naive_time = time.perf_counter() - start

        # KMP должен быть быстрее в худшем случае
        self.assertLess(kmp_time, naive_time * 10)  # KMP хотя бы в 10 раз быстрее

    def test_best_case_boyer_moore(self):
        """Тест лучшего случая для Бойера-Мура."""
        # Лучший случай для Бойера-Мура: символы паттерна не встречаются в тексте
        text = "x" * 1000
        pattern = "abcde"

        import time
        start = time.perf_counter()
        BoyerMoore.boyer_moore_search(text, pattern)
        bm_time = time.perf_counter() - start

        start = time.perf_counter()
        NaiveStringSearch.naive_search(text, pattern)
        naive_time = time.perf_counter() - start

        # Бойер-Мур должен быть значительно быстрее
        self.assertLess(bm_time, naive_time)


if __name__ == "__main__":
    unittest.main()