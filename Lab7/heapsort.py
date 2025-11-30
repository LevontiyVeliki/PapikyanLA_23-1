"""
Реализация алгоритма пирамидальной сортировки (Heapsort).
"""

from heap import MinHeap, MaxHeap


def heapsort_using_minheap(array):
    """
    Сортировка массива с использованием min-кучи.

    Args:
        array (list): Массив для сортировки

    Returns:
        list: Отсортированный массив (по возрастанию)

    Сложность: O(n log n)
    """
    heap = MinHeap(array)
    sorted_array = []

    while len(heap) > 0:
        sorted_array.append(heap.extract())

    return sorted_array


def heapsort_using_maxheap(array):
    """
    Сортировка массива с использованием max-кучи.

    Args:
        array (list): Массив для сортировки

    Returns:
        list: Отсортированный массив (по возрастанию)

    Сложность: O(n log n)
    """
    heap = MaxHeap(array)
    sorted_array = [0] * len(array)

    # Извлекаем элементы в обратном порядке для сортировки по возрастанию
    for i in range(len(array) - 1, -1, -1):
        sorted_array[i] = heap.extract()

    return sorted_array


def heapsort_inplace(array):
    """
    In-place версия пирамидальной сортировки без использования дополнительной памяти.
    Преобразует исходный массив в max-кучу и сортирует его.

    Args:
        array (list): Массив для сортировки (изменяется на месте)

    Сложность: O(n log n)
    Память: O(1) - дополнительная память не используется
    """

    def _sift_down(arr, start, end):
        """
        Погружение элемента для in-place сортировки.

        Args:
            arr: Массив
            start: Индекс корня поддерева
            end: Конечный индекс (включительно)
        """
        root = start

        while 2 * root + 1 <= end:
            child = 2 * root + 1  # Левый потомок
            swap = root

            if arr[swap] < arr[child]:
                swap = child

            if child + 1 <= end and arr[swap] < arr[child + 1]:
                swap = child + 1

            if swap == root:
                return
            else:
                arr[root], arr[swap] = arr[swap], arr[root]
                root = swap

    n = len(array)

    if n <= 1:
        return array

    # Построение max-кучи (heapify)
    # Начинаем с последнего нелистового узла
    for i in range(n // 2 - 1, -1, -1):
        _sift_down(array, i, n - 1)

    # Извлечение элементов из кучи
    for i in range(n - 1, 0, -1):
        # Перемещаем текущий корень в конец
        array[0], array[i] = array[i], array[0]
        # Восстанавливаем свойство кучи для уменьшенной кучи
        _sift_down(array, 0, i - 1)

    return array


# Альтернативные названия для удобства
heapsort = heapsort_inplace