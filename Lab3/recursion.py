"""
Базовые рекурсивные алгоритмы
"""

def factorial(n):
    """
    Вычисление факториала числа n рекурсивным способом.

    Args:
        n (int): Неотрицательное целое число

    Returns:
        int: Факториал числа n

    Временная сложность: O(n)
    Глубина рекурсии: O(n)
    """
    # Базовый случай
    if n == 0 or n == 1:
        return 1
    # Рекурсивный шаг
    return n * factorial(n - 1)


def fibonacci_naive(n):
    """
    Наивное вычисление n-го числа Фибоначчи.

    Args:
        n (int): Порядковый номер числа Фибоначчи

    Returns:
        int: n-е число Фибоначчи

    Временная сложность: O(2^n) - экспоненциальная
    Глубина рекурсии: O(n)
    """
    # Базовые случаи
    if n == 0:
        return 0
    if n == 1:
        return 1
    # Рекурсивный шаг
    return fibonacci_naive(n - 1) + fibonacci_naive(n - 2)


def fast_power(a, n):
    """
    Быстрое возведение числа a в степень n через степень двойки.

    Args:
        a (float): Основание
        n (int): Показатель степени (неотрицательный)

    Returns:
        float: a в степени n

    Временная сложность: O(log n)
    Глубина рекурсии: O(log n)
    """
    # Базовые случаи
    if n == 0:
        return 1
    if n == 1:
        return a

    # Рекурсивный шаг
    half_power = fast_power(a, n // 2)

    if n % 2 == 0:
        # Если степень четная
        return half_power * half_power
    else:
        # Если степень нечетная
        return a * half_power * half_power


# Демонстрация работы функций
if __name__ == "__main__":
    print("Факториал 5:", factorial(5))
    print("10-е число Фибоначчи:", fibonacci_naive(10))
    print("2^10 =", fast_power(2, 10))