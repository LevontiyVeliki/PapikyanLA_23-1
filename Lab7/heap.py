"""
Реализация структуры данных "куча" (min-heap и max-heap) на основе массива.
"""


class MinHeap:
    """
    Реализация min-кучи - двоичной кучи, где значение каждого узла меньше или равно значениям его потомков.
    Корень содержит минимальный элемент.
    """

    def __init__(self, array=None):
        """
        Инициализация кучи.

        Args:
            array (list, optional): Массив для построения кучи. Если не указан, создается пустая куча.

        Сложность: O(n) если передан array, O(1) иначе
        """
        self.heap = []
        if array is not None:
            self.build_heap(array)

    def __len__(self):
        """Возвращает количество элементов в куче."""
        return len(self.heap)

    def __str__(self):
        """Строковое представление кучи."""
        return f"MinHeap({self.heap})"

    def _parent_index(self, index):
        """
        Вычисляет индекс родителя для узла с заданным индексом.

        Args:
            index (int): Индекс узла

        Returns:
            int: Индекс родителя или -1 если корень
        """
        if index == 0:
            return -1
        return (index - 1) // 2

    def _left_child_index(self, index):
        """
        Вычисляет индекс левого потомка для узла с заданным индексом.

        Args:
            index (int): Индекс узла

        Returns:
            int: Индекс левого потомка или -1 если потомка нет
        """
        left = 2 * index + 1
        return left if left < len(self.heap) else -1

    def _right_child_index(self, index):
        """
        Вычисляет индекс правого потомка для узла с заданным индексом.

        Args:
            index (int): Индекс узла

        Returns:
            int: Индекс правого потомка или -1 если потомка нет
        """
        right = 2 * index + 2
        return right if right < len(self.heap) else -1

    def _sift_up(self, index):
        """
        Всплытие элемента - перемещение элемента вверх по куче до восстановления свойства кучи.

        Args:
            index (int): Индекс элемента для всплытия

        Сложность: O(log n)
        """
        parent = self._parent_index(index)

        while parent >= 0 and self.heap[parent] > self.heap[index]:
            # Меняем местами с родителем
            self.heap[parent], self.heap[index] = self.heap[index], self.heap[parent]
            index = parent
            parent = self._parent_index(index)

    def _sift_down(self, index):
        """
        Погружение элемента - перемещение элемента вниз по куче до восстановления свойства кучи.

        Args:
            index (int): Индекс элемента для погружения

        Сложность: O(log n)
        """
        size = len(self.heap)

        while True:
            left = self._left_child_index(index)
            right = self._right_child_index(index)
            smallest = index

            # Находим наименьший элемент среди текущего узла и его потомков
            if left != -1 and self.heap[left] < self.heap[smallest]:
                smallest = left
            if right != -1 and self.heap[right] < self.heap[smallest]:
                smallest = right

            # Если текущий узел не наименьший, меняем местами с наименьшим потомком
            if smallest != index:
                self.heap[index], self.heap[smallest] = self.heap[smallest], self.heap[index]
                index = smallest
            else:
                break

    def insert(self, value):
        """
        Вставка нового элемента в кучу.

        Args:
            value: Значение для вставки

        Сложность: O(log n)
        """
        self.heap.append(value)
        self._sift_up(len(self.heap) - 1)

    def extract(self):
        """
        Извлечение минимального элемента (корня) из кучи.

        Returns:
            Минимальный элемент или None если куча пуста

        Сложность: O(log n)
        """
        if not self.heap:
            return None

        if len(self.heap) == 1:
            return self.heap.pop()

        root = self.heap[0]
        # Перемещаем последний элемент в корень и погружаем его
        self.heap[0] = self.heap.pop()
        self._sift_down(0)

        return root

    def peek(self):
        """
        Просмотр минимального элемента без извлечения.

        Returns:
            Минимальный элемент или None если куча пуста

        Сложность: O(1)
        """
        return self.heap[0] if self.heap else None

    def build_heap(self, array):
        """
        Построение кучи из произвольного массива.

        Args:
            array (list): Массив для построения кучи

        Сложность: O(n)
        """
        self.heap = array[:]  # Копируем массив

        # Начинаем с последнего нелистового узла и применяем sift_down
        # Последний нелистовой узел имеет индекс (n//2 - 1)
        for i in range(len(self.heap) // 2 - 1, -1, -1):
            self._sift_down(i)

    def is_valid_heap(self):
        """
        Проверка корректности свойства min-кучи.

        Returns:
            bool: True если куча корректна, False в противном случае

        Сложность: O(n)
        """
        for i in range(len(self.heap)):
            left = self._left_child_index(i)
            right = self._right_child_index(i)

            if left != -1 and self.heap[i] > self.heap[left]:
                return False
            if right != -1 and self.heap[i] > self.heap[right]:
                return False

        return True

    def visualize(self):
        """
        Текстовая визуализация кучи в виде дерева.

        Returns:
            str: Визуализация кучи в виде строки
        """
        if not self.heap:
            return "Empty heap"

        def _visualize_recursive(index, prefix="", is_left=True):
            result = ""

            right = self._right_child_index(index)
            if right != -1:
                result += _visualize_recursive(right, prefix + ("│   " if is_left else "    "), False)

            result += prefix + ("└── " if is_left else "┌── ") + str(self.heap[index]) + "\n"

            left = self._left_child_index(index)
            if left != -1:
                result += _visualize_recursive(left, prefix + ("    " if is_left else "│   "), True)

            return result

        return _visualize_recursive(0)


class MaxHeap:
    """
    Реализация max-кучи - двоичной кучи, где значение каждого узла больше или равно значениям его потомков.
    Корень содержит максимальный элемент.
    """

    def __init__(self, array=None):
        """
        Инициализация max-кучи.

        Args:
            array (list, optional): Массив для построения кучи
        """
        self.heap = []
        if array is not None:
            self.build_heap(array)

    def __len__(self):
        return len(self.heap)

    def __str__(self):
        return f"MaxHeap({self.heap})"

    def _parent_index(self, index):
        if index == 0:
            return -1
        return (index - 1) // 2

    def _left_child_index(self, index):
        left = 2 * index + 1
        return left if left < len(self.heap) else -1

    def _right_child_index(self, index):
        right = 2 * index + 2
        return right if right < len(self.heap) else -1

    def _sift_up(self, index):
        """
        Всплытие элемента для max-кучи.

        Сложность: O(log n)
        """
        parent = self._parent_index(index)

        while parent >= 0 and self.heap[parent] < self.heap[index]:
            self.heap[parent], self.heap[index] = self.heap[index], self.heap[parent]
            index = parent
            parent = self._parent_index(index)

    def _sift_down(self, index):
        """
        Погружение элемента для max-кучи.

        Сложность: O(log n)
        """
        size = len(self.heap)

        while True:
            left = self._left_child_index(index)
            right = self._right_child_index(index)
            largest = index

            if left != -1 and self.heap[left] > self.heap[largest]:
                largest = left
            if right != -1 and self.heap[right] > self.heap[largest]:
                largest = right

            if largest != index:
                self.heap[index], self.heap[largest] = self.heap[largest], self.heap[index]
                index = largest
            else:
                break

    def insert(self, value):
        """
        Вставка элемента в max-кучу.

        Сложность: O(log n)
        """
        self.heap.append(value)
        self._sift_up(len(self.heap) - 1)

    def extract(self):
        """
        Извлечение максимального элемента из кучи.

        Returns:
            Максимальный элемент или None если куча пуста

        Сложность: O(log n)
        """
        if not self.heap:
            return None

        if len(self.heap) == 1:
            return self.heap.pop()

        root = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._sift_down(0)

        return root

    def peek(self):
        """
        Просмотр максимального элемента без извлечения.

        Сложность: O(1)
        """
        return self.heap[0] if self.heap else None

    def build_heap(self, array):
        """
        Построение max-кучи из массива.

        Сложность: O(n)
        """
        self.heap = array[:]

        for i in range(len(self.heap) // 2 - 1, -1, -1):
            self._sift_down(i)

    def is_valid_heap(self):
        """
        Проверка корректности свойства max-кучи.

        Сложность: O(n)
        """
        for i in range(len(self.heap)):
            left = self._left_child_index(i)
            right = self._right_child_index(i)

            if left != -1 and self.heap[i] < self.heap[left]:
                return False
            if right != -1 and self.heap[i] < self.heap[right]:
                return False

        return True

    def visualize(self):
        """
        Текстовая визуализация max-кучи.
        """
        if not self.heap:
            return "Empty heap"

        def _visualize_recursive(index, prefix="", is_left=True):
            result = ""

            right = self._right_child_index(index)
            if right != -1:
                result += _visualize_recursive(right, prefix + ("│   " if is_left else "    "), False)

            result += prefix + ("└── " if is_left else "┌── ") + str(self.heap[index]) + "\n"

            left = self._left_child_index(index)
            if left != -1:
                result += _visualize_recursive(left, prefix + ("    " if is_left else "│   "), True)

            return result

        return _visualize_recursive(0)