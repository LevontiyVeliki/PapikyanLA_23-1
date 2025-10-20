"""
Оптимизация рекурсивных алгоритмов с помощью мемоизации
"""
import time
from recursion import fibonacci_naive

# Глобальная переменная для подсчета вызовов
call_count = {
    'naive': 0,
    'memo': 0
}

def fibonacci_memoized(n, memo=None):
    """
    Вычисление n-го числа Фибоначчи с мемоизацией.

    Args:
        n (int): Порядковый номер числа Фибоначчи
        memo (dict): Словарь для хранения вычисленных значений

    Returns:
        int: n-е число Фибоначчи

    Временная сложность: O(n)
    Глубина рекурсии: O(n)
    """
    global call_count
    call_count['memo'] += 1

    # Инициализация словаря мемоизации при первом вызове
    if memo is None:
        memo = {}

    # Базовые случаи
    if n == 0:
        return 0
    if n == 1:
        return 1

    # Проверяем, не вычисляли ли мы уже это значение
    if n in memo:
        return memo[n]

    # Рекурсивный шаг с сохранением результата
    memo[n] = fibonacci_memoized(n - 1, memo) + fibonacci_memoized(n - 2, memo)
    return memo[n]

def fibonacci_naive_counted(n):
    """
    Наивная версия Фибоначчи с подсчетом вызовов.
    """
    global call_count
    call_count['naive'] += 1

    if n == 0:
        return 0
    if n == 1:
        return 1
    return fibonacci_naive_counted(n - 1) + fibonacci_naive_counted(n - 2)

def measure_time(func, *args, repetitions=1):
    """
    Точное измерение времени выполнения функции.

    Args:
        func: Функция для измерения
        *args: Аргументы функции
        repetitions (int): Количество повторений для усреднения

    Returns:
        float: Среднее время выполнения в секундах
    """
    # Используем timeit для более точных измерений
    if repetitions > 1:
        total_time = 0
        for _ in range(repetitions):
            start_time = time.perf_counter()
            func(*args)
            end_time = time.perf_counter()
            total_time += (end_time - start_time)
        return total_time / repetitions
    else:
        start_time = time.perf_counter()
        result = func(*args)
        end_time = time.perf_counter()
        return end_time - start_time, result

def compare_fibonacci_performance(n=35):
    """
    Сравнение производительности наивной и мемоизированной версий.

    Args:
        n (int): Число для вычисления
    """
    global call_count

    print(f"\nСравнение производительности для n={n}")
    print("=" * 60)

    # Сбрасываем счетчики
    call_count = {'naive': 0, 'memo': 0}

    # Мемоизированная версия - однократное выполнение
    time_memo, result_memo = measure_time(fibonacci_memoized, n)
    memo_calls = call_count['memo']

    # Сбрасываем счетчик для наивной версии
    call_count['naive'] = 0

    # Для маленьких n измеряем напрямую, для больших - используем приближение
    if n <= 30:
        time_naive, result_naive = measure_time(fibonacci_naive_counted, n)
        naive_calls = call_count['naive']
    else:
        # Для больших n используем экстраполяцию или ограничиваем измерения
        if n > 35:
            print(f"Предупреждение: Наивное вычисление для n={n} может занять очень много времени")
            # Используем теоретическую оценку
            naive_calls = 2 ** n  # Теоретическое количество вызовов
            time_naive = None
            result_naive = result_memo  # Результаты должны совпадать
        else:
            time_naive, result_naive = measure_time(fibonacci_naive_counted, n)
            naive_calls = call_count['naive']

    print(f"Результат: {result_memo}")
    print(f"Количество вызовов:")
    print(f"  - Наивная версия: {naive_calls:,}")
    print(f"  - Мемоизированная версия: {memo_calls}")
    print(f"  - Экономия вызовов: {naive_calls/memo_calls:.0f}x")

    if time_naive is not None:
        print(f"Время выполнения:")
        print(f"  - Наивная версия: {time_naive:.6f} секунд")
        print(f"  - Мемоизированная версия: {time_memo:.6f} секунд")
        print(f"  - Ускорение: {time_naive/time_memo:.2f}x")
    else:
        print(f"Время выполнения:")
        print(f"  - Наивная версия: слишком долго (оценочно > {2**n / 1000000:.0f} сек)")
        print(f"  - Мемоизированная версия: {time_memo:.6f} секунд")

    # Дополнительная проверка для маленьких n с многократными выполнениями
    if n <= 25:
        print(f"\nТочные измерения (усреднение по 100 выполнениям):")
        time_memo_avg = measure_time(fibonacci_memoized, n, repetitions=100)
        time_naive_avg = measure_time(fibonacci_naive_counted, n, repetitions=100)
        print(f"  - Наивная версия (100 повторов): {time_naive_avg:.6f} сек")
        print(f"  - Мемоизированная версия (100 повторов): {time_memo_avg:.6f} сек")
        print(f"  - Ускорение: {time_naive_avg/time_memo_avg:.2f}x")

def analyze_memoization_benefits():
    """
    Анализ преимуществ мемоизации для разных размеров задач.
    """
    global call_count

    print("\n" + "="*70)
    print("АНАЛИЗ ЭФФЕКТИВНОСТИ МЕМОИЗАЦИИ")
    print("="*70)

    # Тестируем для разных значений n
    test_values = [5, 10, 15, 20, 25, 30, 35]

    for n in test_values:
        call_count = {'naive': 0, 'memo': 0}

        # Вычисляем с мемоизацией
        result_memo = fibonacci_memoized(n)
        memo_calls = call_count['memo']

        # Теоретическое количество вызовов для наивной версии
        call_count['naive'] = 0
        if n <= 25:
            fibonacci_naive_counted(n)
            naive_calls = call_count['naive']
        else:
            # Аппроксимация для больших n
            naive_calls = int(2 ** (n / 2) * 1.5)  # Приблизительная оценка

        print(f"n={n:2d}: Вызовы {naive_calls:>8,} → {memo_calls:>4} "
              f"(сокращение в {naive_calls/memo_calls:6.1f} раз)")

def demo_small_n_measurements():
    """
    Демонстрация для очень маленьких n с точным временем.
    """
    global call_count

    print(f"\n{'='*50}")
    print("ТОЧНЫЕ ИЗМЕРЕНИЯ ДЛЯ МАЛЕНЬКИХ n")
    print(f"{'='*50}")

    for n in [5, 10, 15]:
        call_count = {'naive': 0, 'memo': 0}

        # Измеряем с многократными выполнениями для точности
        time_naive = measure_time(fibonacci_naive_counted, n, repetitions=1000)
        call_count['naive'] = 0  # Сбрасываем для мемоизации
        time_memo = measure_time(fibonacci_memoized, n, repetitions=1000)

        print(f"n={n}: Наивная {time_naive:.6f}с, Мемоизация {time_memo:.6f}с, "
              f"Ускорение {time_naive/time_memo:.1f}x")

if __name__ == "__main__":
    # Анализ эффективности
    analyze_memoization_benefits()

    # Сравнение производительности для конкретных значений
    compare_fibonacci_performance(20)
    compare_fibonacci_performance(25)
    compare_fibonacci_performance(30)
    compare_fibonacci_performance(35)

    # Демонстрация для очень маленьких n с точным временем
    demo_small_n_measurements()