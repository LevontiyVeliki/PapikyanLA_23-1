"""
Реализация приоритетной очереди на основе кучи.
"""

from heap import MinHeap


class PriorityItem:
    """
    Элемент приоритетной очереди с приоритетом и значением.
    """

    def __init__(self, priority, value):
        """
        Инициализация элемента.

        Args:
            priority: Приоритет (меньше значение = выше приоритет)
            value: Значение элемента
        """
        self.priority = priority
        self.value = value

    def __lt__(self, other):
        """Сравнение для min-кучи (меньше приоритет = выше в куче)."""
        return self.priority < other.priority

    def __eq__(self, other):
        """Проверка равенства."""
        return self.priority == other.priority and self.value == other.value

    def __str__(self):
        """Строковое представление."""
        return f"({self.priority}: {self.value})"

    def __repr__(self):
        """Представление для отладки."""
        return f"PriorityItem({self.priority}, {self.value})"


class PriorityQueue:
    """
    Приоритетная очередь на основе min-кучи.
    Элементы с меньшим приоритетом извлекаются первыми.
    """

    def __init__(self):
        """Инициализация пустой приоритетной очереди."""
        self.heap = MinHeap()

    def __len__(self):
        """Количество элементов в очереди."""
        return len(self.heap)

    def __str__(self):
        """Строковое представление очереди."""
        return f"PriorityQueue({[str(item) for item in self.heap.heap]})"

    def enqueue(self, value, priority=0):
        """
        Добавление элемента в очередь с заданным приоритетом.

        Args:
            value: Значение элемента
            priority: Приоритет (меньше значение = выше приоритет)

        Сложность: O(log n)
        """
        item = PriorityItem(priority, value)
        self.heap.insert(item)

    def dequeue(self):
        """
        Извлечение элемента с наивысшим приоритетом (наименьшим значением приоритета).

        Returns:
            Значение элемента или None если очередь пуста

        Сложность: O(log n)
        """
        item = self.heap.extract()
        return item.value if item else None

    def peek(self):
        """
        Просмотр элемента с наивысшим приоритетом без извлечения.

        Returns:
            Значение элемента или None если очередь пуста

        Сложность: O(1)
        """
        item = self.heap.peek()
        return item.value if item else None

    def is_empty(self):
        """Проверка пустоты очереди."""
        return len(self.heap) == 0

    def change_priority(self, value, new_priority):
        """
        Изменение приоритета элемента.
        ВНИМАНИЕ: Эта операция неэффективна для данной реализации (O(n)).
        Для эффективного изменения приоритета нужна более сложная реализация с хеш-таблицей.

        Args:
            value: Значение элемента
            new_priority: Новый приоритет

        Сложность: O(n)
        """
        # Поиск элемента (неэффективно)
        for i, item in enumerate(self.heap.heap):
            if item.value == value:
                old_priority = item.priority
                item.priority = new_priority

                # Если приоритет уменьшился, всплываем
                if new_priority < old_priority:
                    self.heap._sift_up(i)
                # Если приоритет увеличился, погружаем
                elif new_priority > old_priority:
                    self.heap._sift_down(i)
                return True

        return False  # Элемент не найден