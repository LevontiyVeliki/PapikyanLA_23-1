"""
Реализация Z-функции и алгоритмов на её основе.
"""

from typing import List, Tuple


class ZFunction:
    """
    Класс для работы с Z-функцией.
    """

    @staticmethod
    def compute_z_function(string: str) -> List[int]:
        """
        Вычисление Z-функции для строки.

        Z-функция z[i] - длина наибольшего общего префикса
        строки string и суффикса string[i..n-1].

        Args:
            string: Строка для вычисления Z-функции

        Returns:
            Список значений Z-функции

        Сложность: O(n) времени, O(n) памяти
        """
        n = len(string)
        if n == 0:
            return []

        z = [0] * n
        z[0] = n  # По определению

        # Границы текущего Z-блока
        left = right = 0

        for i in range(1, n):
            if i <= right:
                # Используем ранее вычисленные значения
                z[i] = min(right - i + 1, z[i - left])
            else:
                z[i] = 0

            # Пытаемся увеличить z[i]
            while i + z[i] < n and string[z[i]] == string[i + z[i]]:
                z[i] += 1

            # Обновляем границы Z-блока
            if i + z[i] - 1 > right:
                left = i
                right = i + z[i] - 1

        return z

    @staticmethod
    def z_search(text: str, pattern: str) -> List[int]:
        """
        Поиск подстроки с использованием Z-функции.

        Args:
            text: Текст для поиска
            pattern: Подстрока для поиска

        Returns:
            Список позиций начала вхождений

        Сложность: O(n + m) времени, O(n + m) памяти
        """
        if not pattern:
            return list(range(len(text) + 1))

        m, n = len(pattern), len(text)
        if m > n:
            return []

        # Создаем строку pattern + '$' + text
        combined = pattern + '$' + text
        z = ZFunction.compute_z_function(combined)

        positions = []
        for i in range(m + 1, len(combined)):
            if z[i] == m:
                positions.append(i - m - 1)

        return positions

    @staticmethod
    def compute_z_function_verbose(string: str) -> Tuple[List[int], List[str]]:
        """
        Вычисление Z-функции с подробным выводом процесса.

        Args:
            string: Строка для вычисления Z-функции

        Returns:
            Кортеж (Z-функция, список шагов)
        """
        n = len(string)
        z = [0] * n
        steps = []

        if n == 0:
            return z, steps

        z[0] = n
        left = right = 0

        for i in range(1, n):
            step_info = f"i={i}, символ '{string[i]}', [L,R]=[{left},{right}]"

            if i <= right:
                z[i] = min(right - i + 1, z[i - left])
                step_info += f", i в Z-блоке, z[{i}] = min({right - i + 1}, z[{i - left}]={z[i - left]}) = {z[i]}"
            else:
                z[i] = 0
                step_info += f", i вне Z-блока, z[{i}] = 0"

            # Пытаемся увеличить z[i]
            while i + z[i] < n and string[z[i]] == string[i + z[i]]:
                step_info += f", совпадение: string[{z[i]}]='{string[z[i]]}' == string[{i + z[i]}]='{string[i + z[i]]}', z[{i}]++"
                z[i] += 1

            # Обновляем границы Z-блока
            if i + z[i] - 1 > right:
                old_left, old_right = left, right
                left = i
                right = i + z[i] - 1
                step_info += f", обновлен Z-блок: [{old_left},{old_right}] -> [{left},{right}]"
            else:
                step_info += f", Z-блок не изменился"

            steps.append(step_info)

        return z, steps

    @staticmethod
    def find_distinct_substrings_count(string: str) -> int:
        """
        Нахождение количества различных подстрок в строке с использованием Z-функции.

        Args:
            string: Строка для анализа

        Returns:
            Количество различных подстрок

        Сложность: O(n²)
        """
        n = len(string)
        count = 0

        # Для каждого префикса
        for i in range(n + 1):
            prefix = string[:i]
            if not prefix:
                continue

            # Вычисляем Z-функцию для текущего префикса
            z = ZFunction.compute_z_function(prefix)

            # Находим максимальное значение Z-функции (кроме z[0])
            max_z = max(z[1:]) if len(z) > 1 else 0

            # Количество новых подстрок = длина префикса - максимальная длина бордера
            new_substrings = i - max_z
            count += new_substrings

        return count

    @staticmethod
    def find_palindromic_substrings(string: str) -> List[str]:
        """
        Поиск всех палиндромных подстрок с использованием Z-функции.

        Args:
            string: Строка для анализа

        Returns:
            Список палиндромных подстрок

        Сложность: O(n²)
        """
        n = len(string)
        palindromes = set()

        # Для каждой возможной центральной позиции
        for center in range(n):
            # Нечетная длина
            left = right = center
            while left >= 0 and right < n and string[left] == string[right]:
                palindromes.add(string[left:right + 1])
                left -= 1
                right += 1

            # Четная длина
            left, right = center, center + 1
            while left >= 0 and right < n and string[left] == string[right]:
                palindromes.add(string[left:right + 1])
                left -= 1
                right += 1

        return sorted(palindromes, key=lambda x: (len(x), x))


def demonstrate_z_function():
    """
    Демонстрация работы Z-функции.
    """
    print("=== ДЕМОНСТРАЦИЯ Z-ФУНКЦИИ ===\n")

    test_strings = [
        "aaa",
        "abcabc",
        "aabaab",
        "abacaba"
    ]

    for string in test_strings:
        z, steps = ZFunction.compute_z_function_verbose(string)

        print(f"Строка: '{string}'")
        print("Z-функция:", z)
        print("Процесс вычисления:")
        for step in steps[:5]:  # Показываем только первые 5 шагов для краткости
            print("  ", step)
        if len(steps) > 5:
            print("  ...")

        distinct_count = ZFunction.find_distinct_substrings_count(string)
        print(f"Количество различных подстрок: {distinct_count}")

        palindromes = ZFunction.find_palindromic_substrings(string)
        print(f"Палиндромные подстроки: {palindromes[:5]}{'...' if len(palindromes) > 5 else ''}")
        print()


if __name__ == "__main__":
    demonstrate_z_function()