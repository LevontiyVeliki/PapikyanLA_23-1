class Node:
    """Узел связного списка"""
    __slots__ = ['data', 'next']  # Оптимизация памяти

    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedList:
    """Односвязный список с указателем на хвост"""
    __slots__ = ['head', 'tail', '_size']

    def __init__(self):
        self.head = None
        self.tail = None
        self._size = 0

    def insert_at_start(self, data):
        """Вставка в начало - O(1)"""
        new_node = Node(data)
        if self.head is None:
            self.head = self.tail = new_node
        else:
            new_node.next = self.head
            self.head = new_node
        self._size += 1

    def insert_at_end(self, data):
        """Вставка в конец - O(1) с использованием tail"""
        new_node = Node(data)
        if self.tail is None:
            self.head = self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node
        self._size += 1

    def delete_from_start(self):
        """Удаление из начала - O(1)"""
        if self.head is None:
            raise IndexError("Удаление из пустого списка")

        data = self.head.data
        self.head = self.head.next
        if self.head is None:
            self.tail = None
        self._size -= 1
        return data

    def traversal(self):
        """Обход списка - O(n)"""
        current = self.head
        while current:
            yield current.data
            current = current.next

    def __len__(self):
        return self._size

    def __str__(self):
        return " -> ".join(str(x) for x in self.traversal()) + " -> None"


# Демонстрация работы
if __name__ == "__main__":
    ll = LinkedList()
    ll.insert_at_start(3)
    ll.insert_at_start(2)
    ll.insert_at_start(1)
    ll.insert_at_end(4)

    print("Список после вставок:", ll)
    print("Удалённый элемент:", ll.delete_from_start())
    print("Список после удаления:", ll)
