"""
Анализ производительности различных представлений графов и алгоритмов.
"""

import time
import random
import matplotlib.pyplot as plt
from graph_representation import *
from graph_traversal import *
from shortest_path import *
import sys
import psutil
import os


class GraphAnalysis:
    """
    Класс для анализа производительности работы с графами.
    """

    @staticmethod
    def analyze_memory_usage():
        """
        Анализ использования памяти различными представлениями графов.
        """
        print("=== АНАЛИЗ ИСПОЛЬЗОВАНИЯ ПАМЯТИ ===\n")

        # Характеристики тестовой машины
        import platform
        print("Характеристики тестовой машины:")
        print(f"Процессор: {platform.processor()}")
        print(f"Память: {psutil.virtual_memory().total // (1024 ** 3)} GB")
        print(f"ОС: {platform.system()} {platform.release()}")
        print(f"Python: {sys.version}")
        print()

        sizes = [10, 50, 100, 200, 500]
        matrix_memory = []
        list_memory = []

        print("Размер | Матрица (КБ) | Список (КБ) | Отношение")
        print("-" * 50)

        for size in sizes:
            # Создаем полный граф для максимального использования памяти
            graph_matrix = AdjacencyMatrixGraph(directed=False, weighted=False)
            graph_list = AdjacencyListGraph(directed=False, weighted=False)

            # Добавляем вершины
            vertices = [f"V{i}" for i in range(size)]
            for v in vertices:
                graph_matrix.add_vertex(v)
                graph_list.add_vertex(v)

            # Добавляем рёбра (полный граф)
            for i in range(size):
                for j in range(i + 1, size):
                    graph_matrix.add_edge(vertices[i], vertices[j])
                    graph_list.add_edge(vertices[i], vertices[j])

            mem_matrix = graph_matrix.memory_usage() / 1024  # КБ
            mem_list = graph_list.memory_usage() / 1024  # КБ

            matrix_memory.append(mem_matrix)
            list_memory.append(mem_list)

            ratio = mem_matrix / mem_list if mem_list > 0 else float('inf')

            print(f"{size:6} | {mem_matrix:11.1f} | {mem_list:10.1f} | {ratio:8.2f}")

        # Построение графиков
        plt.figure(figsize=(12, 5))

        plt.subplot(1, 2, 1)
        plt.plot(sizes, matrix_memory, 'o-', label='Матрица смежности', linewidth=2)
        plt.plot(sizes, list_memory, 's-', label='Список смежности', linewidth=2)
        plt.xlabel('Количество вершин')
        plt.ylabel('Использование памяти (КБ)')
        plt.title('Использование памяти представлениями графов\n(полный граф)')
        plt.legend()
        plt.grid(True, alpha=0.3)

        plt.subplot(1, 2, 2)
        plt.plot(sizes, [m / l for m, l in zip(matrix_memory, list_memory)], 'o-',
                 color='red', linewidth=2)
        plt.xlabel('Количество вершин')
        plt.ylabel('Отношение (матрица/список)')
        plt.title('Отношение использования памяти')
        plt.grid(True, alpha=0.3)

        plt.tight_layout()
        plt.savefig('memory_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()

        return sizes, matrix_memory, list_memory

    @staticmethod
    def analyze_operations_performance():
        """
        Анализ производительности операций для разных представлений.
        """
        print("\n=== АНАЛИЗ ПРОИЗВОДИТЕЛЬНОСТИ ОПЕРАЦИЙ ===\n")

        sizes = [100, 200, 500, 1000]
        operations = 1000

        results = {
            'add_edge_matrix': [],
            'add_edge_list': [],
            'has_edge_matrix': [],
            'has_edge_list': [],
            'get_neighbors_matrix': [],
            'get_neighbors_list': []
        }

        print("Размер | Добавление (мс) | Проверка (мс) | Соседи (мс)")
        print("       | Матрица | Список | Матрица | Список | Матрица | Список")
        print("-" * 70)

        for size in sizes:
            # Создаем графы с заданным количеством вершин
            graph_matrix = AdjacencyMatrixGraph(directed=False, weighted=False)
            graph_list = AdjacencyListGraph(directed=False, weighted=False)

            vertices = [f"V{i}" for i in range(size)]
            for v in vertices:
                graph_matrix.add_vertex(v)
                graph_list.add_vertex(v)

            # Добавляем некоторые рёбра для реалистичности
            for i in range(size * 2):
                u, v = random.sample(vertices, 2)
                graph_matrix.add_edge(u, v)
                graph_list.add_edge(u, v)

            # Тестируем операции
            perf_results = GraphAnalyzer.compare_operations(graph_matrix, graph_list, operations)

            results['add_edge_matrix'].append(perf_results['matrix_add_edge'] * 1000)
            results['add_edge_list'].append(perf_results['list_add_edge'] * 1000)
            results['has_edge_matrix'].append(perf_results['matrix_has_edge'] * 1000)
            results['has_edge_list'].append(perf_results['list_has_edge'] * 1000)
            results['get_neighbors_matrix'].append(perf_results['matrix_get_neighbors'] * 1000)
            results['get_neighbors_list'].append(perf_results['list_get_neighbors'] * 1000)

            print(f"{size:6} | {results['add_edge_matrix'][-1]:7.2f} | {results['add_edge_list'][-1]:6.2f} | "
                  f"{results['has_edge_matrix'][-1]:7.2f} | {results['has_edge_list'][-1]:6.2f} | "
                  f"{results['get_neighbors_matrix'][-1]:7.2f} | {results['get_neighbors_list'][-1]:6.2f}")

        # Построение графиков
        plt.figure(figsize=(15, 10))

        # График добавления рёбер
        plt.subplot(2, 2, 1)
        plt.plot(sizes, results['add_edge_matrix'], 'o-', label='Матрица', linewidth=2)
        plt.plot(sizes, results['add_edge_list'], 's-', label='Список', linewidth=2)
        plt.xlabel('Количество вершин')
        plt.ylabel('Время (мс)')
        plt.title('Добавление рёбер (1000 операций)')
        plt.legend()
        plt.grid(True, alpha=0.3)

        # График проверки рёбер
        plt.subplot(2, 2, 2)
        plt.plot(sizes, results['has_edge_matrix'], 'o-', label='Матрица', linewidth=2)
        plt.plot(sizes, results['has_edge_list'], 's-', label='Список', linewidth=2)
        plt.xlabel('Количество вершин')
        plt.ylabel('Время (мс)')
        plt.title('Проверка рёбер (1000 операций)')
        plt.legend()
        plt.grid(True, alpha=0.3)

        # График получения соседей
        plt.subplot(2, 2, 3)
        plt.plot(sizes, results['get_neighbors_matrix'], 'o-', label='Матрица', linewidth=2)
        plt.plot(sizes, results['get_neighbors_list'], 's-', label='Список', linewidth=2)
        plt.xlabel('Количество вершин')
        plt.ylabel('Время (мс)')
        plt.title('Получение соседей (1000 операций)')
        plt.legend()
        plt.grid(True, alpha=0.3)

        # Сводный график
        plt.subplot(2, 2, 4)
        x_pos = range(len(sizes))
        width = 0.35

        # Усреднённое время для матрицы и списка
        avg_matrix = [(a + h + g) / 3 for a, h, g in zip(results['add_edge_matrix'],
                                                         results['has_edge_matrix'],
                                                         results['get_neighbors_matrix'])]
        avg_list = [(a + h + g) / 3 for a, h, g in zip(results['add_edge_list'],
                                                       results['has_edge_list'],
                                                       results['get_neighbors_list'])]

        plt.bar([x - width / 2 for x in x_pos], avg_matrix, width, label='Матрица', alpha=0.8)
        plt.bar([x + width / 2 for x in x_pos], avg_list, width, label='Список', alpha=0.8)
        plt.xlabel('Размер графа')
        plt.ylabel('Среднее время (мс)')
        plt.title('Средняя производительность операций')
        plt.xticks(x_pos, sizes)
        plt.legend()
        plt.grid(True, alpha=0.3, axis='y')

        plt.tight_layout()
        plt.savefig('operations_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()

        return sizes, results

    @staticmethod
    def analyze_algorithms_scalability():
        """
        Анализ масштабируемости алгоритмов на графах.
        """
        print("\n=== АНАЛИЗ МАСШТАБИРУЕМОСТИ АЛГОРИТМОВ ===\n")

        sizes = [100, 200, 500, 1000, 2000]
        bfs_times = []
        dfs_times = []
        dijkstra_times = []
        connected_components_times = []

        print("Размер | BFS (мс) | DFS (мс) | Дейкстра (мс) | Компоненты (мс)")
        print("-" * 65)

        for size in sizes:
            # Создаем разреженный граф для реалистичности
            graph = AdjacencyListGraph(directed=False, weighted=True)

            vertices = [f"V{i}" for i in range(size)]
            for v in vertices:
                graph.add_vertex(v)

            # Добавляем рёбра (каждая вершина соединяется с 3-5 случайными)
            for i in range(size):
                num_edges = random.randint(3, 5)
                neighbors = random.sample(vertices, min(num_edges, size))
                for neighbor in neighbors:
                    if neighbor != vertices[i]:
                        weight = random.randint(1, 10)
                        graph.add_edge(vertices[i], neighbor, weight)

            # Тестируем BFS
            start = time.perf_counter()
            GraphTraversal.bfs(graph, vertices[0])
            bfs_time = (time.perf_counter() - start) * 1000
            bfs_times.append(bfs_time)

            # Тестируем DFS
            start = time.perf_counter()
            GraphTraversal.dfs_iterative(graph, vertices[0])
            dfs_time = (time.perf_counter() - start) * 1000
            dfs_times.append(dfs_time)

            # Тестируем Дейкстру
            start = time.perf_counter()
            ShortestPath.dijkstra(graph, vertices[0])
            dijkstra_time = (time.perf_counter() - start) * 1000
            dijkstra_times.append(dijkstra_time)

            # Тестируем поиск компонент связности
            start = time.perf_counter()
            GraphTraversal.connected_components(graph)
            components_time = (time.perf_counter() - start) * 1000
            connected_components_times.append(components_time)

            print(f"{size:6} | {bfs_time:8.2f} | {dfs_time:7.2f} | {dijkstra_time:12.2f} | {components_time:14.2f}")

        # Построение графиков
        plt.figure(figsize=(12, 8))

        plt.subplot(2, 2, 1)
        plt.plot(sizes, bfs_times, 'o-', label='BFS', linewidth=2)
        plt.plot(sizes, dfs_times, 's-', label='DFS', linewidth=2)
        plt.xlabel('Количество вершин')
        plt.ylabel('Время (мс)')
        plt.title('Масштабируемость BFS и DFS')
        plt.legend()
        plt.grid(True, alpha=0.3)

        plt.subplot(2, 2, 2)
        plt.plot(sizes, dijkstra_times, 'o-', label='Дейкстра', linewidth=2, color='red')
        plt.xlabel('Количество вершин')
        plt.ylabel('Время (мс)')
        plt.title('Масштабируемость алгоритма Дейкстры')
        plt.legend()
        plt.grid(True, alpha=0.3)

        plt.subplot(2, 2, 3)
        plt.plot(sizes, connected_components_times, 'o-', label='Компоненты связности',
                 linewidth=2, color='green')
        plt.xlabel('Количество вершин')
        plt.ylabel('Время (мс)')
        plt.title('Масштабируемость поиска компонент связности')
        plt.legend()
        plt.grid(True, alpha=0.3)

        plt.subplot(2, 2, 4)
        # Нормализованные времена для сравнения
        max_time = max(max(bfs_times), max(dfs_times), max(dijkstra_times), max(connected_components_times))
        norm_bfs = [t / max_time for t in bfs_times]
        norm_dfs = [t / max_time for t in dfs_times]
        norm_dijkstra = [t / max_time for t in dijkstra_times]
        norm_components = [t / max_time for t in connected_components_times]

        plt.plot(sizes, norm_bfs, 'o-', label='BFS O(V+E)', linewidth=2)
        plt.plot(sizes, norm_dfs, 's-', label='DFS O(V+E)', linewidth=2)
        plt.plot(sizes, norm_dijkstra, '^-', label='Дейкстра O((V+E)logV)', linewidth=2)
        plt.plot(sizes, norm_components, 'd-', label='Компоненты O(V+E)', linewidth=2)
        plt.xlabel('Количество вершин')
        plt.ylabel('Нормализованное время')
        plt.title('Сравнительная масштабируемость алгоритмов')
        plt.legend()
        plt.grid(True, alpha=0.3)

        plt.tight_layout()
        plt.savefig('algorithms_scalability.png', dpi=300, bbox_inches='tight')
        plt.show()

        return sizes, bfs_times, dfs_times, dijkstra_times, connected_components_times

    @staticmethod
    def practical_applications():
        """
        Демонстрация практического применения алгоритмов на графах.
        """
        print("\n=== ПРАКТИЧЕСКИЕ ПРИМЕНЕНИЯ ===\n")

        # 1. Социальная сеть - поиск друзей
        print("1. СОЦИАЛЬНАЯ СЕТЬ - ПОИСК ДРУЗЕЙ")
        social_network = AdjacencyListGraph(directed=False, weighted=False)

        users = ['Алиса', 'Боб', 'Чарли', 'Дина', 'Ева', 'Франк']
        friendships = [
            ('Алиса', 'Боб'), ('Алиса', 'Чарли'), ('Боб', 'Дина'),
            ('Чарли', 'Дина'), ('Дина', 'Ева'), ('Ева', 'Франк')
        ]

        for u, v in friendships:
            social_network.add_edge(u, v)

        # Поиск общих друзей
        print("Граф социальной сети:")
        print(social_network)

        # Поиск пути между пользователями
        path = GraphTraversal.bfs_path(social_network, 'Алиса', 'Франк')
        print(f"Путь от Алисы к Франку: {' -> '.join(path)}")

        # Компоненты связности (группы друзей)
        components = GraphTraversal.connected_components(social_network)
        print(f"Группы друзей: {components}")

        # 2. Дорожная сеть - поиск кратчайшего пути
        print("\n2. ДОРОЖНАЯ СЕТЬ - КРАТЧАЙШИЙ ПУТЬ")
        road_network = AdjacencyListGraph(directed=False, weighted=True)

        cities = ['Москва', 'Санкт-Петербург', 'Казань', 'Нижний Новгород', 'Екатеринбург']
        roads = [
            ('Москва', 'Санкт-Петербург', 700),
            ('Москва', 'Казань', 800),
            ('Москва', 'Нижний Новгород', 400),
            ('Санкт-Петербург', 'Казань', 1200),
            ('Казань', 'Екатеринбург', 900),
            ('Нижний Новгород', 'Екатеринбург', 1200)
        ]

        for u, v, w in roads:
            road_network.add_edge(u, v, w)

        # Поиск кратчайшего пути
        path, distance = ShortestPath.dijkstra_path(road_network, 'Москва', 'Екатеринбург')
        print(f"Кратчайший путь из Москвы в Екатеринбург: {' -> '.join(path)}")
        print(f"Расстояние: {distance} км")

        # 3. Зависимости задач - топологическая сортировка
        print("\n3. ЗАВИСИМОСТИ ЗАДАЧ - ТОПОЛОГИЧЕСКАЯ СОРТИРОВКА")
        task_dependencies = AdjacencyListGraph(directed=True, weighted=False)

        tasks = {
            'A': 'Анализ требований',
            'B': 'Проектирование архитектуры',
            'C': 'Разработка backend',
            'D': 'Разработка frontend',
            'E': 'Интеграция',
            'F': 'Тестирование',
            'G': 'Деплой'
        }

        dependencies = [
            ('A', 'B'), ('A', 'C'), ('B', 'D'), ('C', 'E'),
            ('D', 'E'), ('E', 'F'), ('F', 'G')
        ]

        for u, v in dependencies:
            task_dependencies.add_edge(u, v)

        order = GraphTraversal.topological_sort(task_dependencies)
        print("Порядок выполнения задач:")
        for i, task in enumerate(order, 1):
            print(f"  {i}. {tasks[task]} ({task})")

        return social_network, road_network, task_dependencies


def run_comprehensive_analysis():
    """
    Запуск комплексного анализа графов.
    """
    print("=== КОМПЛЕКСНЫЙ АНАЛИЗ ГРАФОВ ===\n")

    # Анализ использования памяти
    print("1. Анализ использования памяти...")
    memory_results = GraphAnalysis.analyze_memory_usage()

    # Анализ производительности операций
    print("\n2. Анализ производительности операций...")
    operations_results = GraphAnalysis.analyze_operations_performance()

    # Анализ масштабируемости алгоритмов
    print("\n3. Анализ масштабируемости алгоритмов...")
    scalability_results = GraphAnalysis.analyze_algorithms_scalability()

    # Практические применения
    print("\n4. Практические применения...")
    practical_results = GraphAnalysis.practical_applications()

    print("\n" + "=" * 60)
    print("Анализ завершен успешно! Все графики сохранены в файлы PNG.")
    print("=" * 60)

    return memory_results, operations_results, scalability_results, practical_results


if __name__ == "__main__":
    run_comprehensive_analysis()