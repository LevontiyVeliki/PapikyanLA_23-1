"""
Анализ производительности операций с кучей и сравнение алгоритмов сортировки.
"""

import time
import random
import matplotlib.pyplot as plt
from heap import MinHeap
from heapsort import heapsort_inplace, heapsort_using_minheap
import sys


def measure_heap_operations():
    """
    Измерение времени основных операций с кучей.
    """
    print("=== АНАЛИЗ ПРОИЗВОДИТЕЛЬНОСТИ ОПЕРАЦИЙ С КУЧЕЙ ===\n")

    # Характеристики тестовой машины
    import platform
    import psutil

    print("Характеристики тестовой машины:")
    print(f"Процессор: {platform.processor()}")
    print(f"Память: {psutil.virtual_memory().total // (1024 ** 3)} GB")
    print(f"ОС: {platform.system()} {platform.release()}")
    print(f"Python: {sys.version}")
    print()

    sizes = [100, 500, 1000, 5000, 10000]
    build_heap_times = []
    sequential_insert_times = []
    extract_all_times = []

    print("Размер | Построение (мс) | Послед. вставка (мс) | Извлечение всех (мс)")
    print("-" * 75)

    for size in sizes:
        array = random.sample(range(size * 10), size)

        # Измерение времени построения кучи из массива
        start_time = time.perf_counter()
        heap1 = MinHeap(array)
        build_time = (time.perf_counter() - start_time) * 1000  # мс

        # Измерение времени последовательной вставки
        heap2 = MinHeap()
        start_time = time.perf_counter()
        for value in array:
            heap2.insert(value)
        insert_time = (time.perf_counter() - start_time) * 1000  # мс

        # Измерение времени извлечения всех элементов
        start_time = time.perf_counter()
        while len(heap1) > 0:
            heap1.extract()
        extract_time = (time.perf_counter() - start_time) * 1000  # мс

        build_heap_times.append(build_time)
        sequential_insert_times.append(insert_time)
        extract_all_times.append(extract_time)

        print(f"{size:6} | {build_time:15.2f} | {insert_time:19.2f} | {extract_time:20.2f}")

    # Построение графиков
    plt.figure(figsize=(12, 5))

    plt.subplot(1, 2, 1)
    plt.plot(sizes, build_heap_times, 'o-', label='Build Heap (O(n))', linewidth=2)
    plt.plot(sizes, sequential_insert_times, 's-', label='Sequential Insert (O(n log n))', linewidth=2)
    plt.xlabel('Количество элементов')
    plt.ylabel('Время (миллисекунды)')
    plt.title('Сравнение методов построения кучи')
    plt.legend()
    plt.grid(True, alpha=0.3)

    plt.subplot(1, 2, 2)
    plt.plot(sizes, extract_all_times, 'o-', label='Extract All Elements', linewidth=2, color='red')
    plt.xlabel('Количество элементов')
    plt.ylabel('Время (миллисекунды)')
    plt.title('Время извлечения всех элементов из кучи')
    plt.legend()
    plt.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('heap_performance.png', dpi=300, bbox_inches='tight')
    plt.show()

    return sizes, build_heap_times, sequential_insert_times, extract_all_times


def compare_sorting_algorithms():
    """
    Сравнение производительности различных алгоритмов сортировки.
    """
    print("\n=== СРАВНЕНИЕ АЛГОРИТМОВ СОРТИРОВКИ ===\n")

    sizes = [100, 500, 1000, 5000, 10000]
    heapsort_times = []
    quicksort_times = []
    mergesort_times = []
    builtin_sort_times = []

    print("Размер | Heapsort (мс) | Quicksort (мс) | Mergesort (мс) | Built-in (мс)")
    print("-" * 85)

    for size in sizes:
        array = random.sample(range(size * 10), size)

        # Heapsort
        arr1 = array[:]
        start_time = time.perf_counter()
        heapsort_inplace(arr1)
        heapsort_time = (time.perf_counter() - start_time) * 1000

        # Quicksort
        def quicksort(arr):
            if len(arr) <= 1:
                return arr
            pivot = arr[len(arr) // 2]
            left = [x for x in arr if x < pivot]
            middle = [x for x in arr if x == pivot]
            right = [x for x in arr if x > pivot]
            return quicksort(left) + middle + quicksort(right)

        arr2 = array[:]
        start_time = time.perf_counter()
        quicksort(arr2)
        quicksort_time = (time.perf_counter() - start_time) * 1000

        # Mergesort
        def mergesort(arr):
            if len(arr) <= 1:
                return arr

            mid = len(arr) // 2
            left = mergesort(arr[:mid])
            right = mergesort(arr[mid:])

            result = []
            i = j = 0
            while i < len(left) and j < len(right):
                if left[i] < right[j]:
                    result.append(left[i])
                    i += 1
                else:
                    result.append(right[j])
                    j += 1

            result.extend(left[i:])
            result.extend(right[j:])
            return result

        arr3 = array[:]
        start_time = time.perf_counter()
        mergesort(arr3)
        mergesort_time = (time.perf_counter() - start_time) * 1000

        # Built-in sort (Timsort)
        arr4 = array[:]
        start_time = time.perf_counter()
        sorted(arr4)
        builtin_time = (time.perf_counter() - start_time) * 1000

        heapsort_times.append(heapsort_time)
        quicksort_times.append(quicksort_time)
        mergesort_times.append(mergesort_time)
        builtin_sort_times.append(builtin_time)

        print(
            f"{size:6} | {heapsort_time:13.2f} | {quicksort_time:14.2f} | {mergesort_time:13.2f} | {builtin_time:12.2f}")

    # Построение графиков
    plt.figure(figsize=(10, 6))

    plt.plot(sizes, heapsort_times, 'o-', label='Heapsort', linewidth=2)
    plt.plot(sizes, quicksort_times, 's-', label='Quicksort', linewidth=2)
    plt.plot(sizes, mergesort_times, '^-', label='Mergesort', linewidth=2)
    plt.plot(sizes, builtin_sort_times, 'd-', label='Built-in (Timsort)', linewidth=2)

    plt.xlabel('Количество элементов')
    plt.ylabel('Время (миллисекунды)')
    plt.title('Сравнение алгоритмов сортировки')
    plt.legend()
    plt.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('sorting_comparison.png', dpi=300, bbox_inches='tight')
    plt.show()

    return sizes, heapsort_times, quicksort_times, mergesort_times, builtin_sort_times


if __name__ == "__main__":
    # Установим seed для воспроизводимости результатов
    random.seed(42)

    measure_heap_operations()
    compare_sorting_algorithms()