"""
Реализация дополнительных алгоритмов поиска подстрок.
"""

from typing import List, Dict
import hashlib


class BoyerMoore:
    """
    Реализация алгоритма Бойера-Мура для поиска подстроки.
    """

    @staticmethod
    def build_bad_char_table(pattern: str) -> Dict[str, int]:
        """
        Построение таблицы плохого символа.

        Args:
            pattern: Подстрока для поиска

        Returns:
            Таблица сдвигов для каждого символа
        """
        table = {}
        m = len(pattern)

        # Для символов, не входящих в паттерн, сдвиг = длина паттерна
        # Для символов в паттерне - расстояние от конца
        for i in range(m - 1):
            table[pattern[i]] = m - 1 - i

        return table

    @staticmethod
    def build_good_suffix_table(pattern: str) -> List[int]:
        """
        Построение таблицы хорошего суффикса.

        Args:
            pattern: Подстрока для поиска

        Returns:
            Таблица сдвигов для суффиксов
        """
        m = len(pattern)
        good_suffix = [0] * (m + 1)

        # Вычисляем Z-функцию для обратной строки
        reversed_pattern = pattern[::-1]
        z = [0] * m
        z[0] = m

        left = right = 0
        for i in range(1, m):
            if i <= right:
                z[i] = min(right - i + 1, z[i - left])
            while i + z[i] < m and reversed_pattern[z[i]] == reversed_pattern[i + z[i]]:
                z[i] += 1
            if i + z[i] - 1 > right:
                left = i
                right = i + z[i] - 1

        # Заполняем таблицу хорошего суффикса
        for p in range(m - 1):
            j = m - 1 - z[p]
            if j >= 0:
                good_suffix[j] = p + 1

        return good_suffix

    @staticmethod
    def boyer_moore_search(text: str, pattern: str) -> List[int]:
        """
        Алгоритм Бойера-Мура для поиска подстроки.

        Args:
            text: Текст для поиска
            pattern: Подстрока для поиска

        Returns:
            Список позиций начала вхождений

        Сложность: O(n/m) в лучшем случае, O(n*m) в худшем
        """
        if not pattern:
            return list(range(len(text) + 1))

        n, m = len(text), len(pattern)
        if m > n:
            return []

        bad_char = BoyerMoore.build_bad_char_table(pattern)
        good_suffix = BoyerMoore.build_good_suffix_table(pattern)
        positions = []

        i = 0
        while i <= n - m:
            j = m - 1

            # Сравниваем с конца
            while j >= 0 and pattern[j] == text[i + j]:
                j -= 1

            if j < 0:
                # Нашли совпадение
                positions.append(i)
                i += good_suffix[0] if m > 1 else 1
            else:
                # Вычисляем сдвиг на основе обеих эвристик
                bad_char_shift = bad_char.get(text[i + j], m)
                good_suffix_shift = good_suffix[j + 1]

                i += max(bad_char_shift, good_suffix_shift)

        return positions


class RabinKarp:
    """
    Реализация алгоритма Рабина-Карпа для поиска подстроки.
    """

    @staticmethod
    def polynomial_hash(s: str, base: int = 257, modulus: int = 10 ** 9 + 7) -> int:
        """
        Вычисление полиномиального хеша для строки.

        Args:
            s: Строка для хеширования
            base: Основание полинома
            modulus: Модуль для избежания переполнения

        Returns:
            Хеш-значение строки
        """
        hash_value = 0
        for char in s:
            hash_value = (hash_value * base + ord(char)) % modulus
        return hash_value

    @staticmethod
    def rabin_karp_search(text: str, pattern: str, base: int = 257, modulus: int = 10 ** 9 + 7) -> List[int]:
        """
        Алгоритм Рабина-Карпа для поиска подстроки.

        Args:
            text: Текст для поиска
            pattern: Подстрока для поиска
            base: Основание полинома
            modulus: Модуль для хеширования

        Returns:
            Список позиций начала вхождений

        Сложность: O(n + m) в среднем, O(n*m) в худшем
        """
        if not pattern:
            return list(range(len(text) + 1))

        n, m = len(text), len(pattern)
        if m > n:
            return []

        positions = []

        # Вычисляем хеш паттерна и первого окна
        pattern_hash = RabinKarp.polynomial_hash(pattern, base, modulus)
        window_hash = RabinKarp.polynomial_hash(text[:m], base, modulus)

        # Вычисляем base^(m-1) mod modulus для эффективного обновления хеша
        power = 1
        for _ in range(m - 1):
            power = (power * base) % modulus

        # Сканируем текст
        for i in range(n - m + 1):
            if pattern_hash == window_hash:
                # Проверяем на коллизию
                if text[i:i + m] == pattern:
                    positions.append(i)

            # Обновляем хеш для следующего окна
            if i < n - m:
                window_hash = (window_hash - ord(text[i]) * power) % modulus
                window_hash = (window_hash * base + ord(text[i + m])) % modulus
                window_hash = (window_hash + modulus) % modulus  # Убеждаемся, что не отрицательный

        return positions

    @staticmethod
    def rabin_karp_multiple_patterns(text: str, patterns: List[str]) -> Dict[str, List[int]]:
        """
        Поиск нескольких паттернов одновременно с использованием алгоритма Рабина-Карпа.

        Args:
            text: Текст для поиска
            patterns: Список подстрок для поиска

        Returns:
            Словарь {паттерн: позиции}

        Сложность: O(n * k + m) где k - количество паттернов, m - суммарная длина паттернов
        """
        result = {}
        base = 257
        modulus = 10 ** 9 + 7

        # Вычисляем хеши всех паттернов
        pattern_hashes = {}
        for pattern in patterns:
            if pattern not in pattern_hashes:
                pattern_hashes[pattern] = RabinKarp.polynomial_hash(pattern, base, modulus)
                result[pattern] = []

        # Находим максимальную длину паттерна
        max_len = max(len(p) for p in patterns) if patterns else 0
        if max_len == 0 or max_len > len(text):
            return result

        # Вычисляем хеши всех окон текста
        window_hashes = {}
        for length in set(len(p) for p in patterns):
            if length > len(text):
                continue

            window_hash = RabinKarp.polynomial_hash(text[:length], base, modulus)
            window_hashes[length] = [window_hash]

            power = 1
            for _ in range(length - 1):
                power = (power * base) % modulus

            for i in range(1, len(text) - length + 1):
                window_hash = (window_hash - ord(text[i - 1]) * power) % modulus
                window_hash = (window_hash * base + ord(text[i + length - 1])) % modulus
                window_hash = (window_hash + modulus) % modulus
                window_hashes[length].append(window_hash)

        # Ищем совпадения
        for pattern in patterns:
            pattern_len = len(pattern)
            if pattern_len not in window_hashes:
                continue

            pattern_hash = pattern_hashes[pattern]
            for i, window_hash in enumerate(window_hashes[pattern_len]):
                if pattern_hash == window_hash and text[i:i + pattern_len] == pattern:
                    result[pattern].append(i)

        return result


class StringAlgorithmsComparison:
    """
    Класс для сравнения различных алгоритмов поиска подстрок.
    """

    @staticmethod
    def compare_algorithms(text: str, pattern: str) -> Dict[str, List[int]]:
        """
        Сравнение различных алгоритмов поиска подстрок.

        Args:
            text: Текст для поиска
            pattern: Подстрока для поиска

        Returns:
            Словарь {алгоритм: позиции}
        """
        from prefix_function import PrefixFunction, NaiveStringSearch
        from z_function import ZFunction

        results = {}

        # Наивный поиск
        results["Naive"] = NaiveStringSearch.naive_search(text, pattern)

        # KMP
        results["KMP"] = PrefixFunction.kmp_search(text, pattern)

        # Z-функция
        results["Z-Function"] = ZFunction.z_search(text, pattern)

        # Бойер-Мур
        results["Boyer-Moore"] = BoyerMoore.boyer_moore_search(text, pattern)

        # Рабин-Карп
        results["Rabin-Karp"] = RabinKarp.rabin_karp_search(text, pattern)

        return results

    @staticmethod
    def verify_results(results: Dict[str, List[int]]) -> bool:
        """
        Проверка корректности результатов всех алгоритмов.

        Args:
            results: Результаты работы алгоритмов

        Returns:
            True если все алгоритмы дали одинаковый результат
        """
        if not results:
            return True

        # Берем первый алгоритм как эталон
        reference = None
        for algo, positions in results.items():
            if positions is not None:
                reference = sorted(positions)
                break

        if reference is None:
            return True

        # Проверяем остальные алгоритмы
        for algo, positions in results.items():
            if positions is not None and sorted(positions) != reference:
                return False

        return True


def demonstrate_string_algorithms():
    """
    Демонстрация работы различных алгоритмов поиска подстрок.
    """
    print("=== ДЕМОНСТРАЦИЯ АЛГОРИТМОВ ПОИСКА ПОДСТРОК ===\n")

    test_cases = [
        ("ababcabcabababd", "ababd"),  # Обычный случай
        ("aaaaaa", "aaa"),  # Множественные вхождения
        ("abcdefgh", "xyz"),  # Отсутствие паттерна
        ("abc", ""),  # Пустой паттерн
    ]

    for text, pattern in test_cases:
        print(f"Текст: '{text}'")
        print(f"Паттерн: '{pattern}'")

        results = StringAlgorithmsComparison.compare_algorithms(text, pattern)

        for algo, positions in results.items():
            print(f"  {algo:12}: {positions}")

        is_correct = StringAlgorithmsComparison.verify_results(results)
        print(f"  Корректность: {'✓' if is_correct else '✗'}")
        print()


if __name__ == "__main__":
    demonstrate_string_algorithms()