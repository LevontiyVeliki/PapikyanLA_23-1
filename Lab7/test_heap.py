"""
Unit-тесты для проверки корректности реализации кучи, heapsort и приоритетной очереди.
"""

import unittest
import random
from heap import MinHeap, MaxHeap
from heapsort import heapsort_using_minheap, heapsort_using_maxheap, heapsort_inplace
from priority_queue import PriorityQueue


class TestMinHeap(unittest.TestCase):
    """Тесты для min-кучи."""

    def setUp(self):
        self.heap = MinHeap()

    def test_empty_heap(self):
        """Тест пустой кучи."""
        self.assertEqual(len(self.heap), 0)
        self.assertIsNone(self.heap.peek())
        self.assertIsNone(self.heap.extract())
        self.assertTrue(self.heap.is_valid_heap())

    def test_insert_and_peek(self):
        """Тест вставки и просмотра."""
        self.heap.insert(5)
        self.assertEqual(self.heap.peek(), 5)
        self.assertEqual(len(self.heap), 1)

        self.heap.insert(3)
        self.assertEqual(self.heap.peek(), 3)

        self.heap.insert(7)
        self.assertEqual(self.heap.peek(), 3)

        self.assertTrue(self.heap.is_valid_heap())

    def test_extract(self):
        """Тест извлечения."""
        values = [5, 3, 8, 1, 9, 2]
        for val in values:
            self.heap.insert(val)

        self.assertTrue(self.heap.is_valid_heap())

        extracted = []
        while len(self.heap) > 0:
            extracted.append(self.heap.extract())
            self.assertTrue(self.heap.is_valid_heap() if len(self.heap) > 0 else True)

        self.assertEqual(extracted, sorted(values))

    def test_build_heap(self):
        """Тест построения кучи из массива."""
        array = [9, 5, 2, 7, 1, 8, 3]
        heap = MinHeap(array)

        self.assertTrue(heap.is_valid_heap())
        self.assertEqual(len(heap), len(array))

        # Проверяем, что извлекаются элементы в правильном порядке
        prev = heap.extract()
        while len(heap) > 0:
            current = heap.extract()
            self.assertLessEqual(prev, current)
            prev = current

    def test_large_heap(self):
        """Тест с большим количеством элементов."""
        size = 1000
        values = random.sample(range(10000), size)

        heap = MinHeap(values)
        self.assertTrue(heap.is_valid_heap())

        extracted = []
        for _ in range(size):
            extracted.append(heap.extract())

        self.assertEqual(extracted, sorted(values))


class TestMaxHeap(unittest.TestCase):
    """Тесты для max-кучи."""

    def test_basic_operations(self):
        """Базовые тесты для max-кучи."""
        heap = MaxHeap()

        values = [5, 3, 8, 1, 9, 2]
        for val in values:
            heap.insert(val)

        self.assertTrue(heap.is_valid_heap())

        extracted = []
        while len(heap) > 0:
            extracted.append(heap.extract())

        self.assertEqual(extracted, sorted(values, reverse=True))

    def test_build_max_heap(self):
        """Тест построения max-кучи из массива."""
        array = [9, 5, 2, 7, 1, 8, 3]
        heap = MaxHeap(array)

        self.assertTrue(heap.is_valid_heap())

        prev = heap.extract()
        while len(heap) > 0:
            current = heap.extract()
            self.assertGreaterEqual(prev, current)
            prev = current


class TestHeapsort(unittest.TestCase):
    """Тесты пирамидальной сортировки."""

    def test_heapsort_minheap(self):
        """Тест сортировки с использованием min-кучи."""
        array = [9, 5, 2, 7, 1, 8, 3, 6, 4]
        sorted_array = heapsort_using_minheap(array)
        self.assertEqual(sorted_array, sorted(array))

    def test_heapsort_maxheap(self):
        """Тест сортировки с использованием max-кучи."""
        array = [9, 5, 2, 7, 1, 8, 3, 6, 4]
        sorted_array = heapsort_using_maxheap(array)
        self.assertEqual(sorted_array, sorted(array))

    def test_heapsort_inplace(self):
        """Тест in-place сортировки."""
        array = [9, 5, 2, 7, 1, 8, 3, 6, 4]
        original = array[:]
        sorted_array = heapsort_inplace(array)

        self.assertEqual(sorted_array, sorted(original))
        self.assertEqual(array, sorted(original))  # Проверяем, что исходный массив изменен

    def test_empty_array(self):
        """Тест сортировки пустого массива."""
        self.assertEqual(heapsort_inplace([]), [])

    def test_single_element(self):
        """Тест сортировки массива с одним элементом."""
        self.assertEqual(heapsort_inplace([5]), [5])

    def test_large_array(self):
        """Тест сортировки большого массива."""
        size = 1000
        array = random.sample(range(10000), size)
        sorted_array = heapsort_inplace(array[:])

        self.assertEqual(sorted_array, sorted(array))


class TestPriorityQueue(unittest.TestCase):
    """Тесты приоритетной очереди."""

    def setUp(self):
        self.pq = PriorityQueue()

    def test_enqueue_dequeue(self):
        """Тест добавления и извлечения."""
        self.pq.enqueue("task1", 3)
        self.pq.enqueue("task2", 1)  # Высший приоритет
        self.pq.enqueue("task3", 2)

        self.assertEqual(self.pq.dequeue(), "task2")  # Наивысший приоритет
        self.assertEqual(self.pq.dequeue(), "task3")
        self.assertEqual(self.pq.dequeue(), "task1")
        self.assertIsNone(self.pq.dequeue())

    def test_peek(self):
        """Тест просмотра без извлечения."""
        self.pq.enqueue("task1", 2)
        self.pq.enqueue("task2", 1)

        self.assertEqual(self.pq.peek(), "task2")
        self.assertEqual(self.pq.peek(), "task2")  # Должен остаться тот же элемент
        self.assertEqual(self.pq.dequeue(), "task2")  # Теперь извлекаем

    def test_empty_queue(self):
        """Тест пустой очереди."""
        self.assertTrue(self.pq.is_empty())
        self.assertIsNone(self.pq.dequeue())
        self.assertIsNone(self.pq.peek())

    def test_priority_order(self):
        """Тест порядка приоритетов."""
        tasks = [
            ("low", 3),
            ("high", 1),
            ("medium", 2),
            ("urgent", 0),
        ]

        for value, priority in tasks:
            self.pq.enqueue(value, priority)

        expected_order = ["urgent", "high", "medium", "low"]
        for expected in expected_order:
            self.assertEqual(self.pq.dequeue(), expected)


if __name__ == "__main__":
    unittest.main()