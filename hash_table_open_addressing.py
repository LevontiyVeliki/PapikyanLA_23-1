"""
Реализация хеш-таблицы с открытой адресацией
(линейное пробирование и двойное хеширование)
"""

from typing import Any, Optional, Tuple
from hash_functions import HASH_FUNCTIONS


class HashTableOpenAddressing:
    """
    Хеш-таблица с открытой адресацией

    Поддерживает два метода пробирования:
      - Линейное пробирование
      - Двойное хеширование

    Сложность операций (в среднем случае):
      - Вставка: O(1 / (1 - α)) где α - коэффициент заполнения
      - Поиск: O(1 / (1 - α))
      - Удаление: O(1 / (1 - α))

    Память: O(m), где m - размер таблицы
    """

    # Специальные значения для пометки удаленных элементов
    DELETED = object()
    EMPTY = None

    def __init__(self, initial_size: int = 16, load_factor_threshold: float = 0.7,
                 hash_function: str = 'djb2', probing_method: str = 'double_hashing'):
        self.size = initial_size
        self.count = 0
        self.deleted_count = 0
        self.load_factor_threshold = load_factor_threshold
        self.hash_func = HASH_FUNCTIONS[hash_function]
        self.probing_method = probing_method

        # Инициализация таблицы
        self.keys: List[Optional[str]] = [self.EMPTY] * self.size
        self.values: List[Optional[Any]] = [self.EMPTY] * self.size

    def _hash1(self, key: str) -> int:
        """Первая хеш-функция"""
        return self.hash_func(key, self.size)

    def _hash2(self, key: str) -> int:
        """Вторая хеш-функция для двойного хеширования"""
        # Используем другую хеш-функцию для разнообразия
        return djb2_hash(key, self.size - 1) + 1  # Гарантируем, что шаг ≠ 0

    def _probe_sequence(self, key: str, attempt: int) -> int:
        """Генерация последовательности пробирования"""
        if self.probing_method == 'linear':
            # Линейное пробирование: h(k, i) = (h1(k) + i) % m
            return (self._hash1(key) + attempt) % self.size

        elif self.probing_method == 'double_hashing':
            # Двойное хеширование: h(k, i) = (h1(k) + i * h2(k)) % m
            return (self._hash1(key) + attempt * self._hash2(key)) % self.size

        else:
            raise ValueError(f"Неизвестный метод пробирования: {self.probing_method}")

    def _load_factor(self) -> float:
        """Вычисление коэффициента заполнения (учитывая удаленные элементы)"""
        return (self.count + self.deleted_count) / self.size

    def _effective_load_factor(self) -> float:
        """Эффективный коэффициент заполнения (только активные элементы)"""
        return self.count / self.size

    def _resize(self, new_size: int):
        """Изменение размера таблицы и перехеширование"""
        old_keys = self.keys
        old_values = self.values

        self.size = new_size
        self.count = 0
        self.deleted_count = 0
        self.keys = [self.EMPTY] * self.size
        self.values = [self.EMPTY] * self.size

        # Перехеширование активных элементов
        for i in range(len(old_keys)):
            if old_keys[i] not in [self.EMPTY, self.DELETED]:
                self.insert(old_keys[i], old_values[i])

    def _find_slot(self, key: str) -> Tuple[int, bool]:
        """
        Поиск слота для ключа

        Returns:
            (index, found) - индекс и флаг, найден ли ключ
        """
        attempt = 0
        first_deleted = -1

        while attempt < self.size:
            index = self._probe_sequence(key, attempt)

            if self.keys[index] == self.EMPTY:
                # Нашли пустой слот
                return (first_deleted, False) if first_deleted != -1 else (index, False)

            elif self.keys[index] == self.DELETED:
                # Запоминаем первый удаленный слот
                if first_deleted == -1:
                    first_deleted = index

            elif self.keys[index] == key:
                # Ключ найден
                return (index, True)

            attempt += 1

        # Если таблица полна, но есть удаленные элементы, используем первый удаленный
        if first_deleted != -1:
            return (first_deleted, False)

        # Если действительно нет места, делаем экстренный resize
        self._resize(self.size * 2)
        # Рекурсивно пытаемся снова с новой таблицей
        return self._find_slot(key)

    def insert(self, key: str, value: Any) -> None:
        """Вставка элемента в хеш-таблицу"""
        # Проверка необходимости resize
        if self._load_factor() > self.load_factor_threshold:
            self._resize(self.size * 2)

        index, found = self._find_slot(key)

        if found:
            # Обновление существующего ключа
            self.values[index] = value
        else:
            # Вставка нового ключа
            self.keys[index] = key
            self.values[index] = value
            self.count += 1
            if index != -1 and self.keys[index] == self.DELETED:
                self.deleted_count -= 1

    def search(self, key: str) -> Optional[Any]:
        """Поиск элемента по ключу"""
        attempt = 0

        while attempt < self.size:
            index = self._probe_sequence(key, attempt)

            if self.keys[index] == self.EMPTY:
                # Достигли пустого слота - ключ не найден
                return None

            elif self.keys[index] == key:
                # Ключ найден
                return self.values[index]

            attempt += 1

        # Ключ не найден
        return None

    def delete(self, key: str) -> bool:
        """Удаление элемента по ключу"""
        attempt = 0

        while attempt < self.size:
            index = self._probe_sequence(key, attempt)

            if self.keys[index] == self.EMPTY:
                # Ключ не найден
                return False

            elif self.keys[index] == key:
                # Ключ найден, помечаем как удаленный
                self.keys[index] = self.DELETED
                self.values[index] = self.DELETED
                self.count -= 1
                self.deleted_count += 1
                return True

            attempt += 1

        return False

    def get_stats(self) -> dict:
        """Получение статистики хеш-таблицы"""
        probe_lengths = []

        # Измеряем длину пробирования для поиска
        for i in range(self.size):
            if self.keys[i] not in [self.EMPTY, self.DELETED]:
                attempt = 0
                while attempt < self.size:
                    index = self._probe_sequence(self.keys[i], attempt)
                    if index == i:
                        break
                    attempt += 1
                probe_lengths.append(attempt + 1)

        avg_probe_length = sum(probe_lengths) / len(probe_lengths) if probe_lengths else 0
        max_probe_length = max(probe_lengths) if probe_lengths else 0

        return {
            'size': self.size,
            'count': self.count,
            'deleted_count': self.deleted_count,
            'load_factor': self._load_factor(),
            'effective_load_factor': self._effective_load_factor(),
            'avg_probe_length': avg_probe_length,
            'max_probe_length': max_probe_length,
            'empty_slots': sum(1 for key in self.keys if key == self.EMPTY),
            'deleted_slots': self.deleted_count
        }

    def __str__(self):
        """Строковое представление таблицы"""
        result = []
        for i in range(self.size):
            status = "EMPTY"
            if self.keys[i] == self.DELETED:
                status = "DELETED"
            elif self.keys[i] != self.EMPTY:
                status = f"OCCUPIED: {self.keys[i]} -> {self.values[i]}"
            result.append(f"[{i}]: {status}")
        return "\n".join(result)


# Вспомогательная функция для двойного хеширования
def djb2_hash(key: str, table_size: int) -> int:
    """Вспомогательная хеш-функция для двойного хеширования"""
    hash_value = 5381
    for char in key:
        hash_value = ((hash_value << 5) + hash_value) + ord(char)
    return abs(hash_value) % table_size


# Демонстрация работы
if __name__ == "__main__":
    print("Демонстрация хеш-таблицы с открытой адресацией:")
    print("=" * 50)

    # Тестирование разных методов пробирования
    for probing in ['linear', 'double_hashing']:
        print(f"\nМетод пробирования: {probing}")
        ht = HashTableOpenAddressing(initial_size=5, probing_method=probing)

        # Вставка элементов
        test_data = [("apple", 1), ("banana", 2), ("orange", 3),
                     ("grape", 4), ("kiwi", 5)]

        for key, value in test_data:
            ht.insert(key, value)
            print(f"Вставка: {key} -> {value}")

        print("\nСтатистика:")
        stats = ht.get_stats()
        for key, value in stats.items():
            print(f"  {key}: {value}")

        print(f"\nПоиск 'apple': {ht.search('apple')}")
        print(f"Удаление 'banana': {ht.delete('banana')}")
        print(f"Поиск 'banana' после удаления: {ht.search('banana')}")

        print("\nСтруктура таблицы:")
        print(ht)