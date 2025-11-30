"""
Unit-тесты для проверки корректности работы с графами.
"""

import unittest
from graph_representation import AdjacencyMatrixGraph, AdjacencyListGraph, GraphAnalyzer
from graph_traversal import GraphTraversal, GraphCycleDetection
from shortest_path import ShortestPath, MazeSolver


class TestGraphRepresentation(unittest.TestCase):
    """Тесты представлений графов."""

    def setUp(self):
        """Настройка тестовых графов."""
        # Простой неориентированный невзвешенный граф
        self.simple_graph_edges = [('A', 'B'), ('A', 'C'), ('B', 'C'), ('C', 'D')]

        # Ориентированный взвешенный граф
        self.directed_weighted_edges = [('A', 'B', 3), ('A', 'C', 1), ('B', 'D', 2), ('C', 'D', 4)]

    def test_adjacency_matrix_undirected(self):
        """Тест матрицы смежности для неориентированного графа."""
        graph = AdjacencyMatrixGraph(directed=False, weighted=False)

        for u, v in self.simple_graph_edges:
            graph.add_vertex(u)
            graph.add_vertex(v)
            graph.add_edge(u, v)

        # Проверка симметричности
        self.assertTrue(graph.has_edge('A', 'B'))
        self.assertTrue(graph.has_edge('B', 'A'))
        self.assertTrue(graph.has_edge('A', 'C'))
        self.assertTrue(graph.has_edge('C', 'A'))

        # Проверка отсутствия лишних рёбер
        self.assertFalse(graph.has_edge('A', 'D'))
        self.assertFalse(graph.has_edge('B', 'D'))  # Хотя C-D существует

        # Проверка соседей
        neighbors_a = set(n for n, w in graph.get_neighbors('A'))
        self.assertEqual(neighbors_a, {'B', 'C'})

    def test_adjacency_list_directed_weighted(self):
        """Тест списка смежности для ориентированного взвешенного графа."""
        graph = AdjacencyListGraph(directed=True, weighted=True)

        for u, v, w in self.directed_weighted_edges:
            graph.add_edge(u, v, w)

        # Проверка направленности
        self.assertTrue(graph.has_edge('A', 'B'))
        self.assertFalse(graph.has_edge('B', 'A'))  # Обратное ребро не должно существовать

        # Проверка весов
        neighbors_a = dict(graph.get_neighbors('A'))
        self.assertEqual(neighbors_a['B'], 3)
        self.assertEqual(neighbors_a['C'], 1)

        # Проверка вершин
        vertices = set(graph.get_vertices())
        self.assertEqual(vertices, {'A', 'B', 'C', 'D'})

    def test_remove_edge(self):
        """Тест удаления рёбер."""
        graph = AdjacencyListGraph(directed=False, weighted=False)
        graph.add_edge('A', 'B')
        graph.add_edge('A', 'C')

        self.assertTrue(graph.has_edge('A', 'B'))
        self.assertTrue(graph.has_edge('B', 'A'))

        graph.remove_edge('A', 'B')

        self.assertFalse(graph.has_edge('A', 'B'))
        self.assertFalse(graph.has_edge('B', 'A'))
        self.assertTrue(graph.has_edge('A', 'C'))  # Другое ребро должно остаться


class TestGraphTraversal(unittest.TestCase):
    """Тесты алгоритмов обхода графов."""

    def setUp(self):
        """Настройка тестового графа."""
        self.graph = AdjacencyListGraph(directed=False, weighted=False)
        edges = [('A', 'B'), ('A', 'C'), ('B', 'D'), ('C', 'E'), ('D', 'E'), ('E', 'F')]

        for u, v in edges:
            graph.add_edge(u, v)

    def test_bfs(self):
        """Тест поиска в ширину."""
        distances, parents = GraphTraversal.bfs(self.graph, 'A')

        # Проверка расстояний
        self.assertEqual(distances['A'], 0)
        self.assertEqual(distances['B'], 1)
        self.assertEqual(distances['C'], 1)
        self.assertEqual(distances['D'], 2)
        self.assertEqual(distances['E'], 2)
        self.assertEqual(distances['F'], 3)

        # Проверка родителей
        self.assertIsNone(parents['A'])
        self.assertEqual(parents['B'], 'A')
        self.assertEqual(parents['C'], 'A')
        self.assertEqual(parents['D'], 'B')

    def test_bfs_path(self):
        """Тест поиска пути BFS."""
        path = GraphTraversal.bfs_path(self.graph, 'A', 'F')
        expected_paths = [
            ['A', 'C', 'E', 'F'],
            ['A', 'B', 'D', 'E', 'F']
        ]

        self.assertIn(path, expected_paths)

        # Несуществующий путь
        graph_disconnected = AdjacencyListGraph(directed=False, weighted=False)
        graph_disconnected.add_edge('X', 'Y')
        graph_disconnected.add_vertex('Z')

        path = GraphTraversal.bfs_path(graph_disconnected, 'X', 'Z')
        self.assertIsNone(path)

    def test_dfs(self):
        """Тест поиска в глубину."""
        visited_recursive = GraphTraversal.dfs_recursive(self.graph, 'A')
        visited_iterative = GraphTraversal.dfs_iterative(self.graph, 'A')

        # Обе версии должны посетить все вершины
        self.assertEqual(set(visited_recursive.keys()), set(self.graph.get_vertices()))
        self.assertEqual(set(visited_iterative.keys()), set(self.graph.get_vertices()))

    def test_connected_components(self):
        """Тест поиска компонент связности."""
        graph = AdjacencyListGraph(directed=False, weighted=False)

        # Первая компонента
        graph.add_edge('A', 'B')
        graph.add_edge('B', 'C')

        # Вторая компонента
        graph.add_edge('D', 'E')

        # Изолированная вершина
        graph.add_vertex('F')

        components = GraphTraversal.connected_components(graph)

        # Должно быть 3 компоненты
        self.assertEqual(len(components), 3)

        # Проверка содержимого компонент
        component_sets = [set(comp) for comp in components]
        self.assertIn({'A', 'B', 'C'}, component_sets)
        self.assertIn({'D', 'E'}, component_sets)
        self.assertIn({'F'}, component_sets)

    def test_topological_sort(self):
        """Тест топологической сортировки."""
        graph = AdjacencyListGraph(directed=True, weighted=False)

        # DAG: A -> B -> C, A -> C
        graph.add_edge('A', 'B')
        graph.add_edge('B', 'C')
        graph.add_edge('A', 'C')
        graph.add_edge('C', 'D')

        order = GraphTraversal.topological_sort(graph)

        # Проверка допустимого топологического порядка
        self.assertIsNotNone(order)
        self.assertEqual(set(order), {'A', 'B', 'C', 'D'})

        # A должен быть перед B и C, B перед C, C перед D
        self.assertLess(order.index('A'), order.index('B'))
        self.assertLess(order.index('A'), order.index('C'))
        self.assertLess(order.index('B'), order.index('C'))
        self.assertLess(order.index('C'), order.index('D'))

        # Граф с циклом
        graph_cyclic = AdjacencyListGraph(directed=True, weighted=False)
        graph_cyclic.add_edge('A', 'B')
        graph_cyclic.add_edge('B', 'C')
        graph_cyclic.add_edge('C', 'A')  # Цикл

        order = GraphTraversal.topological_sort(graph_cyclic)
        self.assertIsNone(order)


class TestShortestPath(unittest.TestCase):
    """Тесты алгоритмов поиска кратчайших путей."""

    def test_dijkstra(self):
        """Тест алгоритма Дейкстры."""
        graph = AdjacencyListGraph(directed=True, weighted=True)

        edges = [
            ('A', 'B', 4),
            ('A', 'C', 2),
            ('B', 'C', 1),
            ('B', 'D', 5),
            ('C', 'D', 8),
            ('C', 'E', 10),
            ('D', 'E', 2)
        ]

        for u, v, w in edges:
            graph.add_edge(u, v, w)

        distances, parents = ShortestPath.dijkstra(graph, 'A')

        # Проверка расстояний
        self.assertEqual(distances['A'], 0)
        self.assertEqual(distances['B'], 4)
        self.assertEqual(distances['C'], 2)
        self.assertEqual(distances['D'], 9)  # A->B->C->D = 4+1+? нет, A->C->? Лучше A->B->D = 4+5=9
        self.assertEqual(distances['E'], 11)  # A->B->D->E = 4+5+2=11

        # Проверка пути
        path, length = ShortestPath.dijkstra_path(graph, 'A', 'E')
        self.assertEqual(path, ['A', 'B', 'D', 'E'])
        self.assertEqual(length, 11)

    def test_bellman_ford(self):
        """Тест алгоритма Беллмана-Форда."""
        graph = AdjacencyListGraph(directed=True, weighted=True)

        edges = [
            ('A', 'B', 4),
            ('A', 'C', 2),
            ('B', 'C', -1),  # Отрицательный вес
            ('B', 'D', 5),
            ('C', 'D', 8),
            ('C', 'E', 10),
            ('D', 'E', 2)
        ]

        for u, v, w in edges:
            graph.add_edge(u, v, w)

        result = ShortestPath.bellman_ford(graph, 'A')
        self.assertIsNotNone(result)  # Не должно быть отрицательных циклов

        distances, parents = result

        # Проверка расстояний
        self.assertEqual(distances['A'], 0)
        self.assertEqual(distances['B'], 4)
        self.assertEqual(distances['C'], 3)  # A->B->C = 4 + (-1) = 3
        self.assertEqual(distances['D'], 9)  # A->B->D = 4+5=9
        self.assertEqual(distances['E'], 11)  # A->B->D->E = 4+5+2=11


class TestMazeSolver(unittest.TestCase):
    """Тесты решения лабиринтов."""

    def test_maze_solver(self):
        """Тест решения лабиринта."""
        maze = [
            [1, 1, 1, 0, 1],
            [1, 0, 1, 1, 1],
            [1, 0, 0, 1, 0],
            [1, 1, 1, 1, 1],
            [0, 0, 1, 0, 1]
        ]

        start = (0, 0)
        end = (4, 4)

        path = MazeSolver.solve_maze(maze, start, end)

        self.assertIsNotNone(path)
        self.assertEqual(path[0], start)
        self.assertEqual(path[-1], end)

        # Проверка что путь состоит только из проходимых клеток
        for i, j in path:
            self.assertEqual(maze[i][j], 1)

        # Проверка что путь непрерывен
        for i in range(len(path) - 1):
            current = path[i]
            next_cell = path[i + 1]
            distance = abs(current[0] - next_cell[0]) + abs(current[1] - next_cell[1])
            self.assertEqual(distance, 1)  # Соседние клетки


if __name__ == '__main__':
    unittest.main()