"""
Реализация основных алгоритмов сортировки с анализом сложности
"""

import time
from typing import List, Callable
import random


def bubble_sort(arr: List[int]) -> List[int]:
    """
    Сортировка пузырьком
    Сложность:
      - Лучший случай: O(n) - уже отсортированный массив
      - Средний случай: O(n²)
      - Худший случай: O(n²) - обратно отсортированный массив
      - Пространственная: O(1) - сортировка на месте
    """
    n = len(arr)
    arr = arr.copy()

    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break
    return arr


def selection_sort(arr: List[int]) -> List[int]:
    """
    Сортировка выбором
    Сложность:
      - Лучший случай: O(n²)
      - Средний случай: O(n²)
      - Худший случай: O(n²)
      - Пространственная: O(1) - сортировка на месте
      - Неустойчивая сортировка
    """
    n = len(arr)
    arr = arr.copy()

    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr


def insertion_sort(arr: List[int]) -> List[int]:
    """
    Сортировка вставками
    Сложность:
      - Лучший случай: O(n) - уже отсортированный массив
      - Средний случай: O(n²)
      - Худший случай: O(n²) - обратно отсортированный массив
      - Пространственная: O(1) - сортировка на месте
      - Устойчивая сортировка
      - Адаптивная - эффективна на почти отсортированных данных
    """
    arr = arr.copy()

    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr


def merge_sort(arr: List[int]) -> List[int]:
    """
    Сортировка слиянием
    Сложность:
      - Лучший случай: O(n log n)
      - Средний случай: O(n log n)
      - Худший случай: O(n log n)
      - Пространственная: O(n) - требуется дополнительная память
      - Устойчивая сортировка
    """
    if len(arr) <= 1:
        return arr.copy()

    def merge(left: List[int], right: List[int]) -> List[int]:
        result = []
        i = j = 0

        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1

        result.extend(left[i:])
        result.extend(right[j:])
        return result

    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])

    return merge(left, right)


def quick_sort(arr: List[int]) -> List[int]:
    """
    Быстрая сортировка (Хоара)
    Сложность:
      - Лучший случай: O(n log n) - сбалансированное разбиение
      - Средний случай: O(n log n)
      - Худший случай: O(n²) - неудачный выбор опорного элемента
      - Пространственная: O(log n) - стек вызовов
      - Неустойчивая сортировка
    """
    arr = arr.copy()

    def _quick_sort(sub_arr: List[int]) -> List[int]:
        if len(sub_arr) <= 1:
            return sub_arr

        # Выбор опорного элемента (медиана трех)
        first, middle, last = sub_arr[0], sub_arr[len(sub_arr) // 2], sub_arr[-1]
        pivot = sorted([first, middle, last])[1]

        left = [x for x in sub_arr if x < pivot]
        middle = [x for x in sub_arr if x == pivot]
        right = [x for x in sub_arr if x > pivot]

        return _quick_sort(left) + middle + _quick_sort(right)

    return _quick_sort(arr)


# Словарь всех алгоритмов для удобного тестирования
SORTING_ALGORITHMS = {
    'bubble_sort': bubble_sort,
    'selection_sort': selection_sort,
    'insertion_sort': insertion_sort,
    'merge_sort': merge_sort,
    'quick_sort': quick_sort
}