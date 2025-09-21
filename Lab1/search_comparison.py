import timeit
import random

def linear_search(arr, target):
    """Линейный поиск в массиве"""
    for i in range(0, len(arr)):  # 0(N) - перебор массива данных
        if (arr[i] == target):  # 0(1) - проверка на необходимый элемент
            return i  # 0(1) - Возврат индекса найденного элемента
    return -1  # 0(1) - Если индекс не найден - вовращаем -1
    # Общая сложность алгоритма O(N) + O(1) + 0(1) = 0(N)


def binary_search(arr, target):
    """Бинарный поиск в отсортированном массиве"""
    left = 0  # 0(1) - положение крайнего левого элемента
    right = len(arr) - 1  # 0(1) - положение крайнего правого элемента

    while left <= right:  # 0(log(n)) - алгоритм бинарного поиска
        mid = (left + right) // 2  # 0(1) высчитываем средний индекс
        if arr[mid] == target:  # 0(1) проверяем на совпадения
            return mid  # 0(1) возвращаем индекс
        elif arr[mid] < target:  # 0(1) если искомое больше среднего
            left = mid + 1  # 0(1) смещаем левую границу
        else:
            right = mid - 1  # 0(1) смещаем правую границу

    return -1  # Если элемент не был найден в массиве
    # 0(log(n)) - средняя скорость алгоритма с отсортированным массивом
    # 0(n log(n)) - средняя скорость алгоритма с сортировкой массива


sizes = [1000, 5000, 10000, 50000, 100000, 500000]  # Размеры массивов, подобранные для тестов

for size in sizes:
    # Генерация случайного массива заданного размера
    data = [random.randint(1, 1000) for _ in range(size)]
    print("Linear: {:>10} - index: {}".format(size, linear_search(data, 5)))
    data.sort()
    print("Binary: {:>10} - index: {}".format(size, binary_search(data, 5)))