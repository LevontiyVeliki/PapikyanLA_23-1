"""
Генерация тестовых данных различных типов для тестирования сортировок
"""

import random
from typing import List, Dict
import numpy as np


def generate_random_array(size: int, min_val: int = 0, max_val: int = 10000) -> List[int]:
    """Генерация массива случайных чисел"""
    return [random.randint(min_val, max_val) for _ in range(size)]


def generate_sorted_array(size: int) -> List[int]:
    """Генерация отсортированного массива"""
    return list(range(size))


def generate_reversed_array(size: int) -> List[int]:
    """Генерация обратно отсортированного массива"""
    return list(range(size, 0, -1))


def generate_almost_sorted_array(size: int, swap_percentage: float = 0.05) -> List[int]:
    """Генерация почти отсортированного массива"""
    arr = list(range(size))

    # Количество пар для обмена
    num_swaps = int(size * swap_percentage)

    for _ in range(num_swaps):
        i, j = random.sample(range(size), 2)
        arr[i], arr[j] = arr[j], arr[i]

    return arr


def generate_test_datasets(sizes: List[int] = None) -> Dict[str, Dict[int, List[int]]]:
    """
    Генерация полного набора тестовых данных

    Returns:
        Dict с ключами: 'random', 'sorted', 'reversed', 'almost_sorted'
    """
    if sizes is None:
        sizes = [100, 500, 1000, 3000, 5000, 7000, 10000]

    datasets = {
        'random': {},
        'sorted': {},
        'reversed': {},
        'almost_sorted': {}
    }

    for size in sizes:
        datasets['random'][size] = generate_random_array(size)
        datasets['sorted'][size] = generate_sorted_array(size)
        datasets['reversed'][size] = generate_reversed_array(size)
        datasets['almost_sorted'][size] = generate_almost_sorted_array(size)

    return datasets


if __name__ == "__main__":
    # Пример генерации и просмотра данных
    test_data = generate_test_datasets([100, 1000])

    for data_type, sizes_data in test_data.items():
        print(f"\n{data_type}:")
        for size, arr in sizes_data.items():
            print(f"  Size {size}: first 10 elements - {arr[:10]}")