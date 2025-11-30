"""
Демонстрация работы кучи, пирамидальной сортировки и приоритетной очереди.
"""

from heap import MinHeap, MaxHeap
from heapsort import heapsort_inplace
from priority_queue import PriorityQueue
import random


def demonstrate_heap_operations():
    """Демонстрация основных операций с кучей."""
    print("=== ДЕМОНСТРАЦИЯ ОСНОВНЫХ ОПЕРАЦИЙ С MIN-КУЧЕЙ ===\n")

    # Создание кучи
    heap = MinHeap()
    values = [9, 5, 2, 7, 1, 8, 3, 6, 4]

    print(f"Исходный массив: {values}")

    # Последовательная вставка
    print("\nПоследовательная вставка элементов:")
    for value in values:
        heap.insert(value)
        print(f"После вставки {value}: {heap}")

    print(f"\nВизуализация кучи:")
    print(heap.visualize())

    print(f"Корень кучи (минимальный элемент): {heap.peek()}")
    print(f"Корректность кучи: {heap.is_valid_heap()}")

    # Извлечение элементов
    print("\nИзвлечение элементов в порядке возрастания:")
    extracted = []
    while len(heap) > 0:
        value = heap.extract()
        extracted.append(value)
        print(f"Извлечен {value}, оставшаяся куча: {heap}")

    print(f"Извлеченные элементы: {extracted}")
    print(f"Отсортированный массив: {sorted(values)}")


def demonstrate_heap_construction():
    """Демонстрация различных методов построения кучи."""
    print("\n\n=== ДЕМОНСТРАЦИЯ ПОСТРОЕНИЯ КУЧИ ИЗ МАССИВА ===\n")

    array = [9, 5, 2, 7, 1, 8, 3, 6, 4]
    print(f"Исходный массив: {array}")

    # Построение кучи из массива
    heap = MinHeap(array)
    print(f"Куча после build_heap: {heap}")
    print(f"Корректность кучи: {heap.is_valid_heap()}")

    # Визуализация
    print("\nВизуализация построенной кучи:")
    print(heap.visualize())


def demonstrate_max_heap():
    """Демонстрация работы max-кучи."""
    print("\n\n=== ДЕМОНСТРАЦИЯ MAX-КУЧИ ===\n")

    array = [9, 5, 2, 7, 1, 8, 3, 6, 4]
    heap = MaxHeap(array)

    print(f"Исходный массив: {array}")
    print(f"Max-куча: {heap}")
    print(f"Корень (максимальный элемент): {heap.peek()}")
    print(f"Корректность max-кучи: {heap.is_valid_heap()}")

    print("\nВизуализация max-кучи:")
    print(heap.visualize())

    print("\nИзвлечение элементов в порядке убывания:")
    extracted = []
    while len(heap) > 0:
        extracted.append(heap.extract())

    print(f"Извлеченные элементы: {extracted}")


def demonstrate_heapsort():
    """Демонстрация пирамидальной сортировки."""
    print("\n\n=== ДЕМОНСТРАЦИЯ ПИРАМИДАЛЬНОЙ СОРТИРОВКИ ===\n")

    array = [9, 5, 2, 7, 1, 8, 3, 6, 4]
    print(f"Исходный массив: {array}")

    # In-place сортировка
    sorted_array = heapsort_inplace(array[:])  # Используем копию
    print(f"Отсортированный массив (in-place): {sorted_array}")

    # Проверка
    print(f"Правильно отсортирован: {sorted_array == sorted(array)}")


def demonstrate_priority_queue():
    """Демонстрация приоритетной очереди."""
    print("\n\n=== ДЕМОНСТРАЦИЯ ПРИОРИТЕТНОЙ ОЧЕРЕДИ ===\n")

    pq = PriorityQueue()

    # Добавление задач с разными приоритетами
    tasks = [
        ("Обычная задача", 2),
        ("Срочная задача", 1),
        ("Очень срочная задача", 0),
        ("Не очень срочная задача", 3),
    ]

    print("Добавление задач в приоритетную очередь:")
    for value, priority in tasks:
        pq.enqueue(value, priority)
        print(f"Добавлена: {value} с приоритетом {priority}")

    print(f"\nСостояние очереди: {pq}")
    print(f"Следующая задача для выполнения: {pq.peek()}")

    print("\nВыполнение задач в порядке приоритета:")
    while not pq.is_empty():
        task = pq.dequeue()
        print(f"Выполняется: {task}")


def demonstrate_large_example():
    """Демонстрация работы с большим набором данных."""
    print("\n\n=== ДЕМОНСТРАЦИЯ С БОЛЬШИМ НАБОРОМ ДАННЫХ ===\n")

    # Генерация большого массива
    size = 20
    large_array = random.sample(range(100), size)

    print(f"Большой массив ({size} элементов): {large_array[:10]}...")  # Показываем первые 10

    # Сортировка с помощью кучи
    heap = MinHeap(large_array)
    sorted_elements = []

    for i in range(min(5, size)):  # Извлекаем первые 5 для демонстрации
        sorted_elements.append(heap.extract())

    print(f"Первые 5 отсортированных элементов: {sorted_elements}")
    print(f"Размер оставшейся кучи: {len(heap)}")


if __name__ == "__main__":
    # Установим seed для воспроизводимости
    random.seed(42)

    demonstrate_heap_operations()
    demonstrate_heap_construction()
    demonstrate_max_heap()
    demonstrate_heapsort()
    demonstrate_priority_queue()
    demonstrate_large_example()