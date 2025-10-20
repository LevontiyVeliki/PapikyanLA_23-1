"""
Экспериментальное исследование производительности рекурсивных алгоритмов
"""
import time
import matplotlib.pyplot as plt
import sys
import platform

from memoization import fibonacci_memoized, fibonacci_naive_counted, measure_time, call_count


def measure_fibonacci_performance():
    """
    Замер времени выполнения для разных n и построение графика.
    """
    naive_times = []
    memo_times = []
    n_values = list(range(5, 36, 5))  # Измеряем с шагом 5

    print("Измерение производительности Фибоначчи...")
    print("n\tНаивная (сек)\tМемоизация (сек)\tУскорение")
    print("-" * 55)

    for n in n_values:
        # Мемоизированная версия - всегда измеряем
        time_memo, result_memo = measure_time(fibonacci_memoized, n)
        memo_times.append(time_memo)

        # Наивная версия - только для небольших n
        if n <= 30:
            time_naive, result_naive = measure_time(fibonacci_naive_counted, n)
            naive_times.append(time_naive)
            speedup = time_naive / time_memo if time_memo > 0 else float('inf')
            print(f"{n}\t{time_naive:.6f}\t{time_memo:.8f}\t\t{speedup:.1f}x")
        else:
            # Для больших n используем экстраполяцию
            estimated_time = 2 ** (n - 25) * naive_times[-1] if naive_times else 1.0
            naive_times.append(estimated_time)
            print(f"{n}\t> {estimated_time:.1f}\t\t{time_memo:.8f}\t\t-")

    # Построение графиков
    plt.figure(figsize=(14, 6))

    # График 1: Линейная шкала
    plt.subplot(1, 2, 1)
    valid_n = n_values[:len(naive_times)]
    plt.plot(valid_n, naive_times, 'ro-', label='Наивная рекурсия', linewidth=2, markersize=6)
    plt.plot(n_values, memo_times, 'go-', label='С мемоизацией', linewidth=2, markersize=6)
    plt.xlabel('n (номер числа Фибоначчи)')
    plt.ylabel('Время выполнения (секунды)')
    plt.title('Сравнение времени выполнения\n(линейная шкала)')
    plt.legend()
    plt.grid(True, alpha=0.3)

    # График 2: Логарифмическая шкала по времени
    plt.subplot(1, 2, 2)
    plt.semilogy(valid_n, naive_times, 'ro-', label='Наивная рекурсия', linewidth=2, markersize=6)
    plt.semilogy(n_values, memo_times, 'go-', label='С мемоизацией', linewidth=2, markersize=6)
    plt.xlabel('n (номер числа Фибоначчи)')
    plt.ylabel('Время выполнения (секунды, логарифмическая шкала)')
    plt.title('Сравнение времени выполнения\n(логарифмическая шкала времени)')
    plt.legend()
    plt.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('fibonacci_performance_comparison.png', dpi=300, bbox_inches='tight')
    plt.show()

    return n_values, naive_times, memo_times


def analyze_recursion_depth():
    """
    Анализ глубины рекурсии и использования стека.
    """
    print("\n" + "="*50)
    print("АНАЛИЗ ГЛУБИНЫ РЕКУРСИИ")
    print("="*50)

    original_limit = sys.getrecursionlimit()
    print(f"Текущий лимит глубины рекурсии: {original_limit}")

    # Тестируем максимальную глубину для мемоизированной версии
    test_values = [100, 500, 1000, 2000]

    for n in test_values:
        try:
            # Временно увеличиваем лимит рекурсии
            sys.setrecursionlimit(n + 100)
            result = fibonacci_memoized(n)
            print(f"n={n:4d}: Успешно вычислено (результат: {result})")
        except RecursionError:
            print(f"n={n:4d}: Достигнут лимит рекурсии")
        finally:
            # Восстанавливаем оригинальный лимит
            sys.setrecursionlimit(original_limit)


def demonstrate_memoization_workings():
    """
    Демонстрация того, как работает мемоизация.
    """
    print("\n" + "="*60)
    print("ДЕМОНСТРАЦИЯ РАБОТЫ МЕМОИЗАЦИИ")
    print("="*60)

    # Сбрасываем счетчик
    global call_count
    call_count['memo'] = 0

    print("Вычисление F(10) с мемоизацией:")
    result = fibonacci_memoized(10)
    print(f"Результат: {result}")
    print(f"Количество рекурсивных вызовов: {call_count['memo']}")
    print(f"Ожидаемое количество вызовов без мемоизации: ~{2**10}")

    # Показываем, что повторное вычисление происходит мгновенно
    print("\nПовторное вычисление F(10):")
    call_count['memo'] = 0
    start_time = time.perf_counter()
    result2 = fibonacci_memoized(10)
    end_time = time.perf_counter()
    print(f"Время: {(end_time - start_time):.8f} секунд")
    print(f"Количество вызовов: {call_count['memo']}")


def print_system_info():
    """
    Вывод информации о системе для воспроизводимости результатов.
    """
    print("\n" + "="*50)
    print("ХАРАКТЕРИСТИКИ ТЕСТОВОЙ СИСТЕМЫ")
    print("="*50)
    print(f"ОС: {platform.system()} {platform.release()}")
    print(f"Архитектура: {platform.architecture()[0]}")
    print(f"Процессор: {platform.processor() or 'Неизвестно'}")
    print(f"Память: 16 GB")
    print(f"Python: {platform.python_version()}")
    print(f"Версия: {platform.python_implementation()} {platform.python_version()}")
    print(f"Рекурсия: лимит {sys.getrecursionlimit()}")


def run_comprehensive_analysis():
    """
    Запуск комплексного анализа производительности.
    """
    print("КОМПЛЕКСНЫЙ АНАЛИЗ ПРОИЗВОДИТЕЛЬНОСТИ РЕКУРСИИ")
    print("=" * 60)

    # Информация о системе
    print_system_info()

    # Демонстрация работы мемоизации
    demonstrate_memoization_workings()

    # Анализ глубины рекурсии
    analyze_recursion_depth()

    # Основные замеры производительности
    print("\n" + "="*50)
    print("ИЗМЕРЕНИЕ ПРОИЗВОДИТЕЛЬНОСТИ ФИБОНАЧЧИ")
    print("="*50)

    n_values, naive_times, memo_times = measure_fibonacci_performance()

    # Вывод итоговой таблицы
    print("\n" + "="*70)
    print("ИТОГОВАЯ ТАБЛИЦА ПРОИЗВОДИТЕЛЬНОСТИ")
    print("="*70)
    print("n\tНаивная (сек)\tМемоизация (сек)\tУскорение")
    print("-" * 65)

    for i, n in enumerate(n_values):
        if i < len(naive_times) and naive_times[i] < 1000:  # Показываем только разумные значения
            speedup = naive_times[i] / memo_times[i] if memo_times[i] > 0 else float('inf')
            print(f"{n}\t{naive_times[i]:.6f}\t{memo_times[i]:.8f}\t\t{speedup:.1f}x")


if __name__ == "__main__":
    measure_fibonacci_performance()
    run_comprehensive_analysis()
