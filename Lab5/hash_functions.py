"""
Реализация различных хеш-функций для строковых ключей
"""


def simple_hash(key: str, table_size: int) -> int:
    """
    Простая хеш-функция - сумма кодов символов

    Особенности:
      - Быстрая, но плохое распределение
      - Чувствительна к анаграммам
      - Неравномерное распределение для похожих строк

    Качество: Низкое
    """
    hash_value = 0
    for char in key:
        hash_value += ord(char)
    return hash_value % table_size


def polynomial_hash(key: str, table_size: int, base: int = 31) -> int:
    """
    Полиномиальная хеш-функция (хорошее качество распределения)

    Формула: h(s) = (s[0] * p^(n-1) + s[1] * p^(n-2) + ... + s[n-1]) % M

    Особенности:
      - Хорошее распределение для похожих строк
      - Меньше коллизий для строк с общими префиксами/суффиксами
      - Используется во многих реальных приложениях

    Качество: Высокое
    """
    hash_value = 0
    for char in key:
        hash_value = (hash_value * base + ord(char)) % table_size
    return hash_value


def djb2_hash(key: str, table_size: int) -> int:
    """
    Хеш-функция DJB2 (очень хорошее качество распределения)

    Алгоритм Дэна Бернстайна, популярен в реальных приложениях

    Особенности:
      - Отличное распределение
      - Быстрая вычисляется
      - Минимальные коллизии
      - Используется во многих языках программирования

    Качество: Очень высокое
    """
    hash_value = 5381
    for char in key:
        hash_value = ((hash_value << 5) + hash_value) + ord(char)  # hash * 33 + c
    return abs(hash_value) % table_size


def fnv_hash(key: str, table_size: int) -> int:
    """
    Хеш-функция FNV-1a (Fowler-Noll-Vo)

    Особенности:
      - Быстрая и эффективная
      - Хорошее распределение
      - Используется в многих системах

    Качество: Высокое
    """
    FNV_OFFSET_BASIS = 2166136261
    FNV_PRIME = 16777619

    hash_value = FNV_OFFSET_BASIS
    for char in key:
        hash_value ^= ord(char)
        hash_value = (hash_value * FNV_PRIME) % (2 ** 32)

    return hash_value % table_size


# Словарь всех хеш-функций для удобного тестирования
HASH_FUNCTIONS = {
    'simple': simple_hash,
    'polynomial': polynomial_hash,
    'djb2': djb2_hash,
    'fnv': fnv_hash
}


def test_hash_functions():
    """Тестирование распределения хеш-функций"""
    test_keys = ["hello", "world", "test", "key", "value", "hash", "table",
                 "hello1", "world1", "test1", "collision", "bucket", "probe"]

    table_size = 100

    print("Тестирование распределения хеш-функций:")
    print("=" * 50)

    for func_name, hash_func in HASH_FUNCTIONS.items():
        hashes = []
        for key in test_keys:
            hashes.append(hash_func(key, table_size))

        unique_hashes = len(set(hashes))
        collision_rate = (len(test_keys) - unique_hashes) / len(test_keys)

        print(f"{func_name:>12}: {unique_hashes:2} уникальных хешей из {len(test_keys)} "
              f"(коллизии: {collision_rate:.1%})")
        print(f"              Хеши: {sorted(hashes)}")


if __name__ == "__main__":
    test_hash_functions()