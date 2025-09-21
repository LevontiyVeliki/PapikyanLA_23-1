import timeit
import random

def linear_search(arr, target):
    """Линейный поиск в массиве"""
    for i in range(0, len(arr)): # 0(N) - перебор массива данных
        if(arr[i] == target): # 0(1) - проверка на необходимый элемент в массиве
            return i # 0(1) - Возврат индекса найденного элемента
    return -1 # 0(1) - Если индекс не найден - вовращаем -1
    # Общая сложность алгоритма O(N) + O(1) + 0(1) = 0(N)

sizes = [1000, 5000, 10000, 50000, 100000, 500000] # Размеры массивов

for size in sizes:
    # Генерация случайного массива заданного размера
    data = [random.randint(1, 1000) for _ in range(size)]
    print("{:>10} - index: {}".format(size, linear_search(data, 5)))