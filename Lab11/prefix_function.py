"""
Реализация префикс-функции и алгоритма Кнута-Морриса-Пратта (KMP).
"""

from typing import List, Tuple
import time


class PrefixFunction:
    """
    Класс для работы с префикс-функцией и алгоритмом KMP.
    """

    @staticmethod
    def compute_prefix_function(pattern: str) -> List[int]:
        """
        Вычисление префикс-функции для строки.

        Префикс-функция π[i] - длина наибольшего собственного префикса,
        который является суффиксом подстроки pattern[0..i].

        Args:
            pattern: Строка для вычисления префикс-функции

        Returns:
            Список значений префикс-функции

        Сложность: O(n) времени, O(n) памяти
        """
        n = len(pattern)
        pi = [0] * n

        if n == 0:
            return pi

        # π[0] всегда 0
        k = 0  # Длина текущего наибольшего бордера

        for i in range(1, n):
            # Уменьшаем k пока не найдем бордер или не дойдем до 0
            while k > 0 and pattern[k] != pattern[i]:
                k = pi[k - 1]

            # Если символы совпадают, увеличиваем длину бордера
            if pattern[k] == pattern[i]:
                k += 1

            pi[i] = k

        return pi

    @staticmethod
    def kmp_search(text: str, pattern: str) -> List[int]:
        """
        Алгоритм Кнута-Морриса-Пратта для поиска всех вхождений подстроки.

        Args:
            text: Текст для поиска
            pattern: Подстрока для поиска

        Returns:
            Список позиций начала вхождений

        Сложность: O(n + m) времени, O(m) памяти
        """
        if not pattern:
            return list(range(len(text) + 1))

        n, m = len(text), len(pattern)
        if m > n:
            return []

        pi = PrefixFunction.compute_prefix_function(pattern)
        positions = []
        q = 0  # Количество совпавших символов

        for i in range(n):
            # Уменьшаем q пока не найдем префикс или не дойдем до 0
            while q > 0 and pattern[q] != text[i]:
                q = pi[q - 1]

            # Если символы совпадают, увеличиваем счетчик
            if pattern[q] == text[i]:
                q += 1

            # Если нашли полное совпадение
            if q == m:
                positions.append(i - m + 1)
                q = pi[q - 1]  # Продолжаем поиск

        return positions

    @staticmethod
    def compute_prefix_function_verbose(pattern: str) -> Tuple[List[int], List[str]]:
        """
        Вычисление префикс-функции с подробным выводом процесса.

        Args:
            pattern: Строка для вычисления префикс-функции

        Returns:
            Кортеж (префикс-функция, список шагов)
        """
        n = len(pattern)
        pi = [0] * n
        steps = []

        if n == 0:
            return pi, steps

        k = 0

        for i in range(1, n):
            step_info = f"i={i}, символ '{pattern[i]}', текущий k={k}"

            # Уменьшаем k пока не найдем бордер или не дойдем до 0
            while k > 0 and pattern[k] != pattern[i]:
                step_info += f", несовпадение: pattern[{k}]='{pattern[k]}' != pattern[{i}]='{pattern[i]}', k = pi[{k - 1}]={pi[k - 1]}"
                k = pi[k - 1]

            # Если символы совпадают, увеличиваем длину бордера
            if pattern[k] == pattern[i]:
                k += 1
                step_info += f", совпадение: k увеличивается до {k}"
            else:
                step_info += f", k остается {k}"

            pi[i] = k
            step_info += f", π[{i}] = {k}"
            steps.append(step_info)

        return pi, steps

    @staticmethod
    def find_period(pattern: str) -> int:
        """
        Нахождение минимального периода строки с использованием префикс-функции.

        Args:
            pattern: Строка для анализа

        Returns:
            Длина минимального периода или 0 если строка непериодическая

        Сложность: O(n)
        """
        if not pattern:
            return 0

        pi = PrefixFunction.compute_prefix_function(pattern)
        n = len(pattern)

        # Период = n - π[n-1], если n делится на период
        period = n - pi[n - 1]

        if n % period == 0:
            return period
        else:
            return 0

    @staticmethod
    def is_rotation(s1: str, s2: str) -> bool:
        """
        Проверка, является ли одна строка циклическим сдвигом другой.

        Args:
            s1: Первая строка
            s2: Вторая строка

        Returns:
            True если s2 является циклическим сдвигом s1

        Сложность: O(n)
        """
        if len(s1) != len(s2):
            return False

        # Если s2 - циклический сдвиг s1, то s2 содержится в s1 + s1
        return len(PrefixFunction.kmp_search(s1 + s1, s2)) > 0


class NaiveStringSearch:
    """
    Наивный алгоритм поиска подстроки для сравнения.
    """

    @staticmethod
    def naive_search(text: str, pattern: str) -> List[int]:
        """
        Наивный алгоритм поиска подстроки.

        Args:
            text: Текст для поиска
            pattern: Подстрока для поиска

        Returns:
            Список позиций начала вхождений

        Сложность: O(n*m) в худшем случае, O(n) в лучшем
        """
        if not pattern:
            return list(range(len(text) + 1))

        n, m = len(text), len(pattern)
        positions = []

        for i in range(n - m + 1):
            match = True
            for j in range(m):
                if text[i + j] != pattern[j]:
                    match = False
                    break

            if match:
                positions.append(i)

        return positions


def demonstrate_prefix_function():
    """
    Демонстрация работы префикс-функции.
    """
    print("=== ДЕМОНСТРАЦИЯ ПРЕФИКС-ФУНКЦИИ ===\n")

    test_patterns = [
        "abcabcd",
        "aabaabaaa",
        "abacaba",
        "aaaaa"
    ]

    for pattern in test_patterns:
        pi, steps = PrefixFunction.compute_prefix_function_verbose(pattern)

        print(f"Строка: '{pattern}'")
        print("Префикс-функция:", pi)
        print("Процесс вычисления:")
        for step in steps:
            print("  ", step)

        period = PrefixFunction.find_period(pattern)
        if period > 0:
            print(f"Минимальный период: {period}")
        else:
            print("Строка непериодическая")
        print()


if __name__ == "__main__":
    demonstrate_prefix_function()