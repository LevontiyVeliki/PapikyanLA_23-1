"""
Анализ производительности операций BST для разных конфигураций деревьев.
"""

import time
import random
import matplotlib.pyplot as plt
from binary_search_tree import BinarySearchTree
import sys


def generate_balanced_tree(size):
    """
    Генерация сбалансированного дерева (случайные значения).

    Args:
        size: Количество элементов

    Returns:
        BinarySearchTree: Сбалансированное дерево
    """
    bst = BinarySearchTree()
    # Увеличиваем диапазон для уменьшения вероятности дубликатов
    values = random.sample(range(size * 3), size)

    for value in values:
        bst.insert(value)

    return bst, values


def generate_degenerate_tree(size):
    """
    Генерация вырожденного дерева (отсортированные значения).
    Используем итеративный подход для избежания рекурсии.

    Args:
        size: Количество элементов

    Returns:
        BinarySearchTree: Вырожденное дерево
    """
    bst = BinarySearchTree()
    values = list(range(size))

    # Увеличиваем лимит рекурсии для больших деревьев
    if size > 990:
        old_limit = sys.getrecursionlimit()
        sys.setrecursionlimit(size + 100)

    try:
        for value in values:
            bst.insert(value)
    finally:
        # Восстанавливаем оригинальный лимит
        if size > 990:
            sys.setrecursionlimit(old_limit)

    return bst, values


def generate_degenerate_tree_iterative(size):
    """
    Альтернативная реализация: генерация вырожденного дерева через прямое построение.
    Это полностью избегает рекурсии при вставке.

    Args:
        size: Количество элементов

    Returns:
        BinarySearchTree: Вырожденное дерево
    """
    bst = BinarySearchTree()

    if size == 0:
        return bst, []

    values = list(range(size))

    # Создаем вырожденное дерево через прямое построение связей
    # Это эффективнее, чем последовательная вставка
    bst.root = BinarySearchTree.TreeNode(values[0])
    current = bst.root

    for i in range(1, size):
        current.right = BinarySearchTree.TreeNode(values[i])
        current = current.right

    return bst, values


def measure_search_performance(bst, search_values, num_searches=1000):
    """
    Измерение времени выполнения операций поиска.

    Args:
        bst: Дерево для тестирования
        search_values: Значения для поиска
        num_searches: Количество операций поиска

    Returns:
        float: Среднее время одной операции поиска в секундах
    """
    start_time = time.perf_counter()

    for _ in range(num_searches):
        value = random.choice(search_values)
        bst.search(value)

    end_time = time.perf_counter()

    return (end_time - start_time) / num_searches


def run_performance_analysis():
    """Запуск полного анализа производительности."""
    print("=== АНАЛИЗ ПРОИЗВОДИТЕЛЬНОСТИ BST ===\n")

    # Характеристики тестовой машины
    import platform
    import psutil

    print("Характеристики тестовой машины:")
    print(f"Процессор: {platform.processor()}")
    print(f"Память: {psutil.virtual_memory().total // (1024**3)} GB")
    print(f"ОС: {platform.system()} {platform.release()}")
    print(f"Текущий лимит рекурсии: {sys.getrecursionlimit()}")
    print()

    # Уменьшим размеры для избежания рекурсии, но сохраним анализ
    sizes = [100, 500, 800, 1000, 1500, 2000]
    balanced_times = []
    degenerate_times = []
    balanced_heights = []
    degenerate_heights = []

    print("Размер | Баланс. время (мкс) | Вырожд. время (мкс) | Баланс. высота | Вырожд. высота")
    print("-" * 85)

    for size in sizes:
        try:
            print(f"Обрабатываем размер: {size}...")

            # Генерация деревьев с обработкой рекурсии
            balanced_bst, balanced_values = generate_balanced_tree(size)

            # Для больших размеров используем итеративный метод
            if size > 800:
                degenerate_bst, degenerate_values = generate_degenerate_tree_iterative(size)
            else:
                degenerate_bst, degenerate_values = generate_degenerate_tree(size)

            # Измерение времени поиска
            balanced_time = measure_search_performance(balanced_bst, balanced_values) * 1e6  # мкс
            degenerate_time = measure_search_performance(degenerate_bst, degenerate_values) * 1e6  # мкс

            # Измерение высоты
            balanced_height = balanced_bst.height()
            degenerate_height = degenerate_bst.height()

            balanced_times.append(balanced_time)
            degenerate_times.append(degenerate_time)
            balanced_heights.append(balanced_height)
            degenerate_heights.append(degenerate_height)

            print(f"{size:6} | {balanced_time:18.2f} | {degenerate_time:19.2f} | {balanced_height:13} | {degenerate_height:14}")

        except RecursionError as e:
            print(f"Пропуск размера {size} из-за ошибки рекурсии: {e}")
            continue
        except Exception as e:
            print(f"Ошибка при размере {size}: {e}")
            continue

    # Построение графиков только если есть данные
    if balanced_times and degenerate_times:
        plt.figure(figsize=(12, 5))

        # График времени выполнения
        plt.subplot(1, 2, 1)
        plt.plot(sizes[:len(balanced_times)], balanced_times, 'o-', label='Сбалансированное дерево', linewidth=2)
        plt.plot(sizes[:len(degenerate_times)], degenerate_times, 's-', label='Вырожденное дерево', linewidth=2)
        plt.xlabel('Количество элементов')
        plt.ylabel('Время поиска (микросекунды)')
        plt.title('Зависимость времени поиска от размера дерева')
        plt.legend()
        plt.grid(True, alpha=0.3)

        # График высоты деревьев
        plt.subplot(1, 2, 2)
        plt.plot(sizes[:len(balanced_heights)], balanced_heights, 'o-', label='Сбалансированное дерево', linewidth=2)
        plt.plot(sizes[:len(degenerate_heights)], degenerate_heights, 's-', label='Вырожденное дерево', linewidth=2)
        plt.plot(sizes, [size - 1 for size in sizes], '--', label='Идеальная высота (n-1)', alpha=0.7)
        plt.plot(sizes, [1.44 * (size + 1).bit_length() for size in sizes], '--',
                 label='Теоретическая высота (~1.44log₂n)', alpha=0.7)
        plt.xlabel('Количество элементов')
        plt.ylabel('Высота дерева')
        plt.title('Зависимость высоты дерева от количества элементов')
        plt.legend()
        plt.grid(True, alpha=0.3)

        plt.tight_layout()
        plt.savefig('bst_performance_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()

        print("\nАнализ завершен успешно! Графики сохранены в 'bst_performance_analysis.png'")
    else:
        print("Не удалось получить данные для построения графиков.")

    return sizes, balanced_times, degenerate_times, balanced_heights, degenerate_heights


if __name__ == "__main__":
    run_performance_analysis()