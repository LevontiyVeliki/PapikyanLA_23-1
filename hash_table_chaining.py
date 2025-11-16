"""
Реализация хеш-таблицы с методом цепочек для разрешения коллизий
"""

from typing import Any, List, Tuple, Optional
from hash_functions import HASH_FUNCTIONS


class HashEntry:
    """Элемент хеш-таблицы для метода цепочек"""

    def __init__(self, key: str, value: Any):
        self.key = key
        self.value = value
        self.next = None  # Ссылка на следующий элемент в цепочке


class HashTableChaining:
    """
    Хеш-таблица с методом цепочек

    Сложность операций (в среднем случае):
      - Вставка: O(1)
      - Поиск: O(1)
      - Удаление: O(1)

    Сложность операций (в худшем случае):
      - Все операции: O(n) - когда все ключи попадают в одну ячейку

    Память: O(n + m), где n - количество элементов, m - размер таблицы
    """

    def __init__(self, initial_size: int = 16, load_factor_threshold: float = 0.75,
                 hash_function: str = 'djb2'):
        self.size = initial_size
        self.count = 0
        self.load_factor_threshold = load_factor_threshold
        self.hash_func = HASH_FUNCTIONS[hash_function]

        # Инициализация таблицы пустыми цепочками
        self.table: List[Optional[HashEntry]] = [None] * self.size

    def _hash(self, key: str) -> int:
        """Вычисление хеша для ключа"""
        return self.hash_func(key, self.size)

    def _resize(self, new_size: int):
        """Изменение размера таблицы и перехеширование всех элементов"""
        old_table = self.table
        self.size = new_size
        self.table = [None] * self.size
        self.count = 0

        # Перехеширование всех элементов
        for head in old_table:
            current = head
            while current:
                self.insert(current.key, current.value)
                current = current.next

    def _load_factor(self) -> float:
        """Вычисление коэффициента заполнения"""
        return self.count / self.size

    def insert(self, key: str, value: Any) -> None:
        """
        Вставка элемента в хеш-таблицу

        Сложность: O(1) в среднем, O(n) в худшем случае
        """
        # Проверка необходимости resize
        if self._load_factor() > self.load_factor_threshold:
            self._resize(self.size * 2)

        index = self._hash(key)

        # Если ячейка пуста, создаем новую цепочку
        if self.table[index] is None:
            self.table[index] = HashEntry(key, value)
            self.count += 1
            return

        # Поиск ключа в цепочке
        current = self.table[index]
        prev = None

        while current:
            if current.key == key:
                # Ключ существует, обновляем значение
                current.value = value
                return
            prev = current
            current = current.next

        # Ключ не найден, добавляем в конец цепочки
        prev.next = HashEntry(key, value)
        self.count += 1

    def search(self, key: str) -> Optional[Any]:
        """
        Поиск элемента по ключу

        Сложность: O(1) в среднем, O(n) в худшем случае
        """
        index = self._hash(key)
        current = self.table[index]

        while current:
            if current.key == key:
                return current.value
            current = current.next

        return None

    def delete(self, key: str) -> bool:
        """
        Удаление элемента по ключу

        Сложность: O(1) в среднем, O(n) в худшем случае
        """
        index = self._hash(key)
        current = self.table[index]
        prev = None

        while current:
            if current.key == key:
                if prev:
                    prev.next = current.next
                else:
                    self.table[index] = current.next
                self.count -= 1
                return True
            prev = current
            current = current.next

        return False

    def get_stats(self) -> dict:
        """Получение статистики хеш-таблицы"""
        chain_lengths = []
        collisions = 0

        for head in self.table:
            length = 0
            current = head
            while current:
                length += 1
                current = current.next
            if length > 0:
                chain_lengths.append(length)
                if length > 1:
                    collisions += length - 1

        avg_chain_length = sum(chain_lengths) / len(chain_lengths) if chain_lengths else 0
        max_chain_length = max(chain_lengths) if chain_lengths else 0

        return {
            'size': self.size,
            'count': self.count,
            'load_factor': self._load_factor(),
            'collisions': collisions,
            'avg_chain_length': avg_chain_length,
            'max_chain_length': max_chain_length,
            'empty_buckets': sum(1 for head in self.table if head is None)
        }

    def __str__(self):
        """Строковое представление таблицы"""
        result = []
        for i, head in enumerate(self.table):
            if head is not None:
                chain = []
                current = head
                while current:
                    chain.append(f"({current.key}: {current.value})")
                    current = current.next
                result.append(f"[{i}]: {' -> '.join(chain)}")
        return "\n".join(result)


# Демонстрация работы
if __name__ == "__main__":
    print("Демонстрация хеш-таблицы с методом цепочек:")
    print("=" * 50)

    ht = HashTableChaining(initial_size=5, hash_function='polynomial')

    # Вставка элементов
    test_data = [("apple", 1), ("banana", 2), ("orange", 3),
                 ("grape", 4), ("kiwi", 5), ("mango", 6)]

    for key, value in test_data:
        ht.insert(key, value)
        print(f"Вставка: {key} -> {value}")
        print(f"Коэффициент заполнения: {ht._load_factor():.2f}")

    print("\nПоиск элементов:")
    for key in ["apple", "banana", "watermelon"]:
        value = ht.search(key)
        print(f"Поиск {key}: {value}")

    print("\nСтатистика:")
    stats = ht.get_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")

    print("\nСтруктура таблицы:")
    print(ht)