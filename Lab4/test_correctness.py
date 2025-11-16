"""
Тестирование корректности реализации алгоритмов сортировки
"""

import random
from sorts import SORTING_ALGORITHMS


def test_sorting_correctness():
    """Тестирование корректности всех алгоритмов сортировки"""

    # Тестовые случаи
    test_cases = [
        [],  # пустой массив
        [1],  # один элемент
        [1, 2, 3, 4, 5],  # уже отсортированный
        [5, 4, 3, 2, 1],  # обратно отсортированный
        [3, 1, 4, 1, 5, 9, 2, 6],  # случайный с повторениями
        [5, 5, 5, 5, 5],  # все элементы одинаковые
        [random.randint(0, 100) for _ in range(100)]  # большой случайный
    ]

    print("Тестирование корректности сортировок...")

    for algo_name, algo_func in SORTING_ALGORITHMS.items():
        print(f"\nТестирование {algo_name}:")
        all_passed = True

        for i, test_arr in enumerate(test_cases):
            try:
                sorted_arr = algo_func(test_arr)
                expected = sorted(test_arr)

                if sorted_arr == expected:
                    print(f"  Тест {i + 1}: ✓ PASSED")
                else:
                    print(f"  Тест {i + 1}: ✗ FAILED")
                    print(f"    Ожидалось: {expected}")
                    print(f"    Получено:  {sorted_arr}")
                    all_passed = False

            except Exception as e:
                print(f"  Тест {i + 1}: ✗ ERROR - {e}")
                all_passed = False

        if all_passed:
            print(f"  ✅ {algo_name} - ВСЕ ТЕСТЫ ПРОЙДЕНЫ")
        else:
            print(f"  ❌ {algo_name} - ЕСТЬ ОШИБКИ")

    print("\n" + "=" * 50)
    print("ТЕСТИРОВАНИЕ ЗАВЕРШЕНО")


if __name__ == "__main__":
    test_sorting_correctness()