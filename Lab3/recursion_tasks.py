"""
Практические задачи с применением рекурсии
"""
import os

def binary_search_recursive(arr, target, low=0, high=None):
    """
    Рекурсивный бинарный поиск в отсортированном массиве.

    Args:
        arr (list): Отсортированный массив
        target: Искомый элемент
        low (int): Нижняя граница поиска
        high (int): Верхняя граница поиска

    Returns:
        int: Индекс элемента или -1 если не найден
    """
    if high is None:
        high = len(arr) - 1

    # Базовый случай - элемент не найден
    if low > high:
        return -1

    # Находим середину
    mid = (low + high) // 2

    # Базовый случай - элемент найден
    if arr[mid] == target:
        return mid

    # Рекурсивные шаги
    elif arr[mid] > target:
        return binary_search_recursive(arr, target, low, mid - 1)
    else:
        return binary_search_recursive(arr, target, mid + 1, high)


def file_system_walk(start_path, indent=0, max_depth=None, current_depth=0):
    """
    Рекурсивный обход файловой системы.

    Args:
        start_path (str): Начальный путь для обхода
        indent (int): Уровень отступа для визуализации иерархии
        max_depth (int): Максимальная глубина рекурсии
        current_depth (int): Текущая глубина рекурсии
    """
    if max_depth is not None and current_depth > max_depth:
        return

    try:
        # Получаем список элементов в директории
        items = os.listdir(start_path)

        for item in items:
            item_path = os.path.join(start_path, item)

            # Определяем тип элемента
            if os.path.isdir(item_path):
                print("  " * indent + f"📁 {item}/")
                # Рекурсивный обход поддиректории
                file_system_walk(item_path, indent + 1, max_depth, current_depth + 1)
            else:
                print("  " * indent + f"📄 {item}")

    except PermissionError:
        print("  " * indent + "❌ Доступ запрещен")
    except FileNotFoundError:
        print("  " * indent + "❌ Файл не найден")


def hanoi_towers(n, source, target, auxiliary):
    """
    Решение задачи Ханойских башен.

    Args:
        n (int): Количество дисков
        source (str): Исходный стержень
        target (str): Целевой стержень
        auxiliary (str): Вспомогательный стержень
    """
    step_counter = [0]  # Используем список для mutable объекта

    def _hanoi_towers_internal(n, source, target, auxiliary):
        if n == 1:
            # Базовый случай: перемещаем один диск
            step_counter[0] += 1
            print(f"{step_counter[0]}. Переместить диск 1 с {source} на {target}")
            return

        # Рекурсивные шаги:
        # 1. Переместить n-1 дисков на вспомогательный стержень
        _hanoi_towers_internal(n - 1, source, auxiliary, target)

        # 2. Переместить самый большой диск на целевой стержень
        step_counter[0] += 1
        print(f"{step_counter[0]}. Переместить диск {n} с {source} на {target}")

        # 3. Переместить n-1 дисков с вспомогательного на целевой стержень
        _hanoi_towers_internal(n - 1, auxiliary, target, source)

    _hanoi_towers_internal(n, source, target, auxiliary)
    return step_counter[0]


def measure_recursion_depth():
    """
    Измерение максимальной глубины рекурсии при обходе файловой системы.
    """
    max_depth_found = [0]

    def count_depth(path, current_depth):
        max_depth_found[0] = max(max_depth_found[0], current_depth)

        try:
            for item in os.listdir(path):
                item_path = os.path.join(path, item)
                if os.path.isdir(item_path):
                    count_depth(item_path, current_depth + 1)
        except (PermissionError, OSError):
            pass

    # Тестируем на текущей директории
    count_depth(".", 0)
    return max_depth_found[0]


# Демонстрация работы
if __name__ == "__main__":
    print("=== Бинарный поиск ===")
    arr = [1, 3, 5, 7, 9, 11, 13, 15]
    target = 7
    index = binary_search_recursive(arr, target)
    print(f"Массив: {arr}")
    print(f"Элемент {target} найден по индексу: {index}")

    print("\n=== Ханойские башни (3 диска) ===")
    total_steps = hanoi_towers(3, 'A', 'C', 'B')
    print(f"Всего шагов: {total_steps}")

    print("\n=== Обход файловой системы (ограниченная глубина) ===")
    # Обходим текущую директорию с ограничением глубины
    file_system_walk(".", max_depth=2)

    print(f"\n=== Измерение глубины рекурсии ===")
    depth = measure_recursion_depth()
    print(f"Максимальная глубина рекурсии при обходе файловой системы: {depth}")