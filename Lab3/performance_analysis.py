import timeit
import matplotlib.pyplot as plt
from collections import deque
from linked_list import LinkedList
import platform

def measure_insert_start_list(n):
    """Измерение вставки в начало списка - O(n)"""
    setup = "lst = list(range(1000))"
    stmt = f"""
for i in range({n}):
    lst.insert(0, i)
    """
    return timeit.timeit(stmt, setup, number=1)


def measure_insert_start_linked_list(n):
    """Измерение вставки в начало связного списка - O(1)"""
    setup = """
from linked_list import LinkedList
ll = LinkedList()
"""
    stmt = f"""
for i in range({n}):
    ll.insert_at_start(i)
    """
    return timeit.timeit(stmt, setup, number=1)


def measure_dequeue_list(n):
    """Измерение удаления из начала списка - O(n)"""
    setup = f"lst = list(range({n}))"
    stmt = """
while lst:
    lst.pop(0)
"""
    return timeit.timeit(stmt, setup, number=1)


def measure_dequeue_deque(n):
    """Измерение удаления из начала дека - O(1)"""
    setup = f"from collections import deque; dq = deque(range({n}))"
    stmt = """
while dq:
    dq.popleft()
"""
    return timeit.timeit(stmt, setup, number=1)


def run_performance_tests():
    print("=== ИНФОРМАЦИЯ О СИСТЕМЕ ===")
    pc_info = """
    Характеристики ПК для тестирования:
    - Процессор: Intel Core i5-11400H @ 2.70GHz
    - Оперативная память: 16 GB DDR4
    - ОС: Windows 10
    - Python: 3.9.7
    """
    print(pc_info)

    print("\n=== ТЕСТИРОВАНИЕ ПРОИЗВОДИТЕЛЬНОСТИ ===")

    # Тестирование вставки в начало
    sizes = [100, 500, 1000, 2000, 5000]
    list_times = []
    linked_list_times = []

    print("Тест вставки в начало:")
    for size in sizes:
        time_list = measure_insert_start_list(size)
        time_ll = measure_insert_start_linked_list(size)
        list_times.append(time_list)
        linked_list_times.append(time_ll)
        print(f"n={size}: list={time_list:.4f}s, LinkedList={time_ll:.4f}s")

    # Тестирование операций очереди
    print("\nТест операций очереди:")
    deq_list_times = []
    deq_deque_times = []

    for size in sizes:
        time_list = measure_dequeue_list(size)
        time_deque = measure_dequeue_deque(size)
        deq_list_times.append(time_list)
        deq_deque_times.append(time_deque)
        print(f"n={size}: list.pop(0)={time_list:.4f}s, deque.popleft()={time_deque:.4f}s")

    # Построение графиков
    plt.figure(figsize=(12, 5))

    # График 1: Вставка в начало
    plt.subplot(1, 2, 1)
    plt.plot(sizes, list_times, 'r-', label='list.insert(0, item) - O(n)')
    plt.plot(sizes, linked_list_times, 'g-', label='LinkedList.insert_at_start - O(1)')
    plt.xlabel('Количество элементов')
    plt.ylabel('Время (секунды)')
    plt.title('Вставка в начало')
    plt.legend()
    plt.grid(True)

    # График 2: Удаление из начала
    plt.subplot(1, 2, 2)
    plt.plot(sizes, deq_list_times, 'r-', label='list.pop(0) - O(n)')
    plt.plot(sizes, deq_deque_times, 'b-', label='deque.popleft() - O(1)')
    plt.xlabel('Количество элементов')
    plt.ylabel('Время (секунды)')
    plt.title('Удаление из начала')
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.savefig('performance_comparison.png', dpi=300)
    plt.show()


if __name__ == "__main__":
    run_performance_tests()