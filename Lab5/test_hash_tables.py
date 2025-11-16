"""
Unit-тесты для проверки корректности работы хеш-таблиц
"""

import unittest
from hash_table_chaining import HashTableChaining
from hash_table_open_addressing import HashTableOpenAddressing
from hash_functions import HASH_FUNCTIONS


class TestHashFunctions(unittest.TestCase):
    """Тестирование хеш-функций"""

    def test_hash_functions_consistency(self):
        """Тест на детерминированность хеш-функций"""
        test_key = "test_key"
        table_size = 100

        for func_name, hash_func in HASH_FUNCTIONS.items():
            with self.subTest(function=func_name):
                hash1 = hash_func(test_key, table_size)
                hash2 = hash_func(test_key, table_size)
                self.assertEqual(hash1, hash2,
                                 f"Хеш-функция {func_name} не детерминирована")

    def test_hash_functions_range(self):
        """Тест на корректный диапазон хеш-значений"""
        test_key = "test_key"
        table_size = 50

        for func_name, hash_func in HASH_FUNCTIONS.items():
            with self.subTest(function=func_name):
                hash_value = hash_func(test_key, table_size)
                self.assertTrue(0 <= hash_value < table_size,
                                f"Хеш-функция {func_name} вышла за диапазон")


class TestHashTableChaining(unittest.TestCase):
    """Тестирование хеш-таблицы с методом цепочек"""

    def setUp(self):
        self.ht = HashTableChaining(initial_size=10)

    def test_insert_and_search(self):
        """Тест базовых операций вставки и поиска"""
        # Вставка элементов
        self.ht.insert("key1", "value1")
        self.ht.insert("key2", "value2")

        # Проверка поиска
        self.assertEqual(self.ht.search("key1"), "value1")
        self.assertEqual(self.ht.search("key2"), "value2")
        self.assertIsNone(self.ht.search("key3"))

    def test_update_existing_key(self):
        """Тест обновления существующего ключа"""
        self.ht.insert("key1", "value1")
        self.ht.insert("key1", "new_value")

        self.assertEqual(self.ht.search("key1"), "new_value")

    def test_delete(self):
        """Тест удаления элементов"""
        self.ht.insert("key1", "value1")
        self.ht.insert("key2", "value2")

        # Удаление существующего ключа
        self.assertTrue(self.ht.delete("key1"))
        self.assertIsNone(self.ht.search("key1"))
        self.assertEqual(self.ht.search("key2"), "value2")

        # Удаление несуществующего ключа
        self.assertFalse(self.ht.delete("key3"))

    def test_collision_handling(self):
        """Тест обработки коллизий"""
        # Создаем маленькую таблицу для гарантированных коллизий
        small_ht = HashTableChaining(initial_size=2)

        # Вставляем несколько ключей
        small_ht.insert("a", 1)  # хеш 0
        small_ht.insert("b", 2)  # хеш 1
        small_ht.insert("c", 3)  # хеш 0 - коллизия с "a"

        # Проверяем, что все ключи доступны
        self.assertEqual(small_ht.search("a"), 1)
        self.assertEqual(small_ht.search("b"), 2)
        self.assertEqual(small_ht.search("c"), 3)

    def test_resize(self):
        """Тест динамического изменения размера"""
        # Начальный размер
        initial_size = self.ht.size

        # Вставляем много элементов для trigger resize
        for i in range(20):
            self.ht.insert(f"key{i}", f"value{i}")

        # Проверяем, что размер увеличился
        self.assertGreater(self.ht.size, initial_size)

        # Проверяем, что все элементы доступны после resize
        for i in range(20):
            self.assertEqual(self.ht.search(f"key{i}"), f"value{i}")


class TestHashTableOpenAddressing(unittest.TestCase):
    """Тестирование хеш-таблицы с открытой адресацией"""

    def test_linear_probing(self):
        """Тест линейного пробирования"""
        ht = HashTableOpenAddressing(initial_size=5, probing_method='linear')

        # Вставка элементов
        ht.insert("a", 1)
        ht.insert("b", 2)
        ht.insert("c", 3)  # Возможна коллизия

        # Проверка поиска
        self.assertEqual(ht.search("a"), 1)
        self.assertEqual(ht.search("b"), 2)
        self.assertEqual(ht.search("c"), 3)

    def test_double_hashing(self):
        """Тест двойного хеширования"""
        ht = HashTableOpenAddressing(initial_size=5, probing_method='double_hashing')

        # Вставка элементов
        ht.insert("x", 10)
        ht.insert("y", 20)
        ht.insert("z", 30)

        # Проверка поиска
        self.assertEqual(ht.search("x"), 10)
        self.assertEqual(ht.search("y"), 20)
        self.assertEqual(ht.search("z"), 30)

    def test_deletion_and_reinsertion(self):
        """Тест удаления и повторной вставки"""
        ht = HashTableOpenAddressing(initial_size=5)

        ht.insert("key1", "value1")
        ht.insert("key2", "value2")

        # Удаление
        self.assertTrue(ht.delete("key1"))
        self.assertIsNone(ht.search("key1"))

        # Повторная вставка в тот же слот
        ht.insert("key1", "new_value")
        self.assertEqual(ht.search("key1"), "new_value")
        self.assertEqual(ht.search("key2"), "value2")

    def test_load_factor_calculation(self):
        """Тест вычисления коэффициента заполнения"""
        ht = HashTableOpenAddressing(initial_size=10)

        # Начальный коэффициент заполнения
        self.assertEqual(ht._effective_load_factor(), 0.0)

        # После вставки
        ht.insert("key1", "value1")
        self.assertAlmostEqual(ht._effective_load_factor(), 0.1)

        # После удаления
        ht.delete("key1")
        self.assertEqual(ht._effective_load_factor(), 0.0)


class TestCrossImplementation(unittest.TestCase):
    """Сравнительное тестирование обеих реализаций"""

    def test_consistency_between_implementations(self):
        """Тест на согласованность между реализациями"""
        test_data = [
            ("apple", 1), ("banana", 2), ("orange", 3),
            ("grape", 4), ("kiwi", 5), ("mango", 6)
        ]

        # Тестируем обе реализации
        implementations = [
            HashTableChaining(initial_size=10),
            HashTableOpenAddressing(initial_size=10)
        ]

        for ht in implementations:
            with self.subTest(implementation=type(ht).__name__):
                # Вставка
                for key, value in test_data:
                    ht.insert(key, value)

                # Проверка поиска
                for key, expected_value in test_data:
                    self.assertEqual(ht.search(key), expected_value)

                # Проверка удаления
                self.assertTrue(ht.delete("apple"))
                self.assertIsNone(ht.search("apple"))


if __name__ == "__main__":
    # Запуск всех тестов
    unittest.main(verbosity=2)