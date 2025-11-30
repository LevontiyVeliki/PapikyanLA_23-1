"""
Реализация классических жадных алгоритмов.
"""

import heapq
from collections import Counter, namedtuple
import math

# Структуры данных для задач
Interval = namedtuple('Interval', ['start', 'end', 'name'])
Item = namedtuple('Item', ['value', 'weight', 'name'])
HuffmanNode = namedtuple('HuffmanNode', ['char', 'freq', 'left', 'right'])
Edge = namedtuple('Edge', ['u', 'v', 'weight'])


class GreedyAlgorithms:
    """
    Класс, содержащий реализации различных жадных алгоритмов.
    """

    @staticmethod
    def interval_scheduling(intervals):
        """
        Задача о выборе заявок (Interval Scheduling).
        Выбор максимального количества непересекающихся интервалов.

        Жадная стратегия: сортировка по времени окончания и выбор следующего
        рано заканчивающегося непересекающегося интервала.

        Args:
            intervals: Список интервалов в формате (start, end) или (start, end, name)

        Returns:
            list: Выбранные интервалы

        Сложность: O(n log n) - сортировка + линейный проход
        """
        if not intervals:
            return []

        # Преобразуем в именованные кортежи если нужно
        if len(intervals[0]) == 2:
            intervals = [Interval(start, end, f"Task_{i}")
                         for i, (start, end) in enumerate(intervals)]

        # Сортируем по времени окончания
        intervals_sorted = sorted(intervals, key=lambda x: x.end)

        selected = []
        last_end = -float('inf')

        for interval in intervals_sorted:
            if interval.start >= last_end:
                selected.append(interval)
                last_end = interval.end

        return selected

    @staticmethod
    def fractional_knapsack(capacity, items):
        """
        Непрерывный рюкзак (Fractional Knapsack).
        Максимизация стоимости с возможностью брать дробные части предметов.

        Жадная стратегия: сортировка по удельной стоимости (value/weight)
        и взятие большего количества лучших предметов.

        Args:
            capacity: Вместимость рюкзака
            items: Список предметов в формате (value, weight) или (value, weight, name)

        Returns:
            tuple: (максимальная стоимость, список выбранных предметов с долями)

        Сложность: O(n log n) - сортировка по удельной стоимости
        """
        if not items or capacity <= 0:
            return 0, []

        # Преобразуем в именованные кортежи если нужно
        if len(items[0]) == 2:
            items = [Item(value, weight, f"Item_{i}")
                     for i, (value, weight) in enumerate(items)]

        # Сортируем по убыванию удельной стоимости
        items_sorted = sorted(items, key=lambda x: x.value / x.weight, reverse=True)

        total_value = 0
        remaining_capacity = capacity
        selected_items = []

        for item in items_sorted:
            if remaining_capacity >= item.weight:
                # Берем весь предмет
                total_value += item.value
                remaining_capacity -= item.weight
                selected_items.append((item, 1.0))  # 1.0 означает весь предмет
            else:
                # Берем дробную часть
                fraction = remaining_capacity / item.weight
                total_value += item.value * fraction
                selected_items.append((item, fraction))
                break  # Рюкзак заполнен

        return total_value, selected_items

    @staticmethod
    def huffman_coding(text):
        """
        Алгоритм Хаффмана для оптимального префиксного кодирования.

        Жадная стратегия: на каждом шаге объединяем два символа с наименьшей частотой.

        Args:
            text: Входной текст для кодирования

        Returns:
            tuple: (кодировка, закодированный текст, дерево Хаффмана)

        Сложность: O(n log n) - построение кучи и n операций извлечения/добавления
        """
        if not text:
            return {}, "", None

        # Подсчет частот
        freq = Counter(text)

        if len(freq) == 1:
            # Особый случай: только один символ
            char = next(iter(freq))
            return {char: '0'}, '0' * len(text), HuffmanNode(char, freq[char], None, None)

        # Создаем кучу из узлов
        heap = []
        for char, count in freq.items():
            heapq.heappush(heap, (count, id(char), HuffmanNode(char, count, None, None)))

        # Построение дерева Хаффмана
        while len(heap) > 1:
            # Извлекаем два узла с наименьшей частотой
            freq1, id1, node1 = heapq.heappop(heap)
            freq2, id2, node2 = heapq.heappop(heap)

            # Создаем новый узел
            merged_freq = freq1 + freq2
            merged_node = HuffmanNode(None, merged_freq, node1, node2)
            heapq.heappush(heap, (merged_freq, id(merged_node), merged_node))

        # Корень дерева
        _, _, root = heap[0]

        # Построение кодировки
        codes = {}

        def build_codes(node, code):
            if node is None:
                return

            if node.char is not None:
                codes[node.char] = code
                return

            build_codes(node.left, code + '0')
            build_codes(node.right, code + '1')

        build_codes(root, "")

        # Кодирование текста
        encoded_text = ''.join(codes[char] for char in text)

        return codes, encoded_text, root

    @staticmethod
    def coin_change(amount, coins):
        """
        Задача о выдаче сдачи минимальным количеством монет.
        Жадный алгоритм работает только для канонических систем монет.

        Args:
            amount: Сумма для выдачи
            coins: Доступные номиналы монет (должны быть отсортированы по убыванию)

        Returns:
            dict: Номинал -> количество монет

        Сложность: O(n) где n - количество различных номиналов
        """
        coins_sorted = sorted(coins, reverse=True)
        result = {}
        remaining = amount

        for coin in coins_sorted:
            if remaining == 0:
                break

            count = remaining // coin
            if count > 0:
                result[coin] = count
                remaining -= coin * count

        if remaining > 0:
            raise ValueError(f"Невозможно выдать сумму {amount} данными монетами")

        return result

    @staticmethod
    def prim_algorithm(vertices, edges):
        """
        Алгоритм Прима для построения минимального остовного дерева.

        Жадная стратегия: на каждом шаге добавляем ребро минимального веса,
        соединяющее дерево с новой вершиной.

        Args:
            vertices: Список вершин
            edges: Список ребер в формате (u, v, weight)

        Returns:
            list: Ребра минимального остовного дерева

        Сложность: O(E log V) с использованием кучи
        """
        if not vertices:
            return []

        # Создаем словарь смежности
        graph = {v: [] for v in vertices}
        for u, v, weight in edges:
            graph[u].append((v, weight))
            graph[v].append((u, weight))

        # Инициализация
        visited = set()
        mst_edges = []
        start_vertex = vertices[0]

        # Куча для хранения ребер (вес, u, v)
        heap = []
        visited.add(start_vertex)

        # Добавляем все ребра из стартовой вершины
        for neighbor, weight in graph[start_vertex]:
            heapq.heappush(heap, (weight, start_vertex, neighbor))

        while heap and len(visited) < len(vertices):
            # Извлекаем ребро с минимальным весом
            weight, u, v = heapq.heappop(heap)

            if v in visited:
                continue

            # Добавляем ребро в MST
            visited.add(v)
            mst_edges.append(Edge(u, v, weight))

            # Добавляем все ребра из новой вершины
            for neighbor, new_weight in graph[v]:
                if neighbor not in visited:
                    heapq.heappush(heap, (new_weight, v, neighbor))

        return mst_edges


class KnapsackSolver:
    """
    Класс для решения различных версий задачи о рюкзаке.
    """

    @staticmethod
    def brute_force_01_knapsack(capacity, items):
        """
        Точное решение задачи о рюкзаке 0-1 методом полного перебора.

        Args:
            capacity: Вместимость рюкзака
            items: Список предметов (value, weight)

        Returns:
            tuple: (максимальная стоимость, выбранные предметы)

        Сложность: O(2^n) - экспоненциальная
        """
        n = len(items)
        max_value = 0
        best_selection = []

        # Перебираем все возможные комбинации
        for i in range(1 << n):
            current_weight = 0
            current_value = 0
            selection = []

            for j in range(n):
                if i & (1 << j):
                    current_weight += items[j].weight
                    current_value += items[j].value
                    selection.append(items[j])

            if current_weight <= capacity and current_value > max_value:
                max_value = current_value
                best_selection = selection

        return max_value, best_selection

    @staticmethod
    def compare_knapsack_methods(capacity, items):
        """
        Сравнение жадного подхода для непрерывного рюкзака
        с точным решением для дискретного рюкзака.
        """
        print("Сравнение методов решения задачи о рюкзаке:")
        print(f"Вместимость рюкзака: {capacity}")
        print("Предметы:")
        for item in items:
            print(f"  {item.name}: стоимость={item.value}, вес={item.weight}, "
                  f"удельная стоимость={item.value / item.weight:.2f}")

        # Жадный алгоритм для непрерывного рюкзака
        greedy_value, greedy_selection = GreedyAlgorithms.fractional_knapsack(capacity, items)
        print(f"\nЖадный алгоритм (непрерывный):")
        print(f"  Максимальная стоимость: {greedy_value:.2f}")
        print("  Выбранные предметы:")
        for item, fraction in greedy_selection:
            print(f"    {item.name}: {fraction * 100:.1f}%")

        # Точное решение для дискретного рюкзака 0-1
        if len(items) <= 20:  # Ограничиваем размер для полного перебора
            exact_value, exact_selection = KnapsackSolver.brute_force_01_knapsack(capacity, items)
            print(f"\nТочное решение (0-1 рюкзак):")
            print(f"  Максимальная стоимость: {exact_value}")
            print("  Выбранные предметы:")
            for item in exact_selection:
                print(f"    {item.name}")

            print(f"\nРазница: {greedy_value - exact_value:.2f}")
        else:
            print("\nТочное решение: слишком много предметов для полного перебора")

        return greedy_value, exact_value if len(items) <= 20 else None