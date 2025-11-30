"""
Реализация алгоритмов поиска кратчайших путей в графах.
"""

from typing import List, Dict, Set, Tuple, Optional
import heapq
import graph_representation


class ShortestPath:
    """
    Класс, содержащий алгоритмы поиска кратчайших путей.
    """

    @staticmethod
    def dijkstra(graph: graph_representation.AdjacencyListGraph, start: str) -> Tuple[
        Dict[str, float], Dict[str, Optional[str]]]:
        """
        Алгоритм Дейкстры для поиска кратчайших путей во взвешенном графе с неотрицательными весами.

        Сложность: O((V + E) log V) с использованием кучи

        Args:
            graph: Взвешенный граф с неотрицательными весами
            start: Стартовая вершина

        Returns:
            tuple: (расстояния, родители)
        """
        if not graph.weighted:
            raise ValueError("Алгоритм Дейкстры требует взвешенный граф")

        distances = {vertex: float('inf') for vertex in graph.get_vertices()}
        parents = {vertex: None for vertex in graph.get_vertices()}
        distances[start] = 0

        # Приоритетная очередь (расстояние, вершина)
        priority_queue = [(0, start)]

        while priority_queue:
            current_distance, current_vertex = heapq.heappop(priority_queue)

            # Пропускаем устаревшие записи
            if current_distance > distances[current_vertex]:
                continue

            for neighbor, weight in graph.get_neighbors(current_vertex):
                distance = current_distance + weight

                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    parents[neighbor] = current_vertex
                    heapq.heappush(priority_queue, (distance, neighbor))

        return distances, parents

    @staticmethod
    def dijkstra_path(graph: graph_representation.AdjacencyListGraph, start: str, end: str) -> Optional[
        Tuple[List[str], float]]:
        """
        Поиск кратчайшего пути с помощью алгоритма Дейкстры.

        Сложность: O((V + E) log V)

        Args:
            graph: Взвешенный граф с неотрицательными весами
            start: Стартовая вершина
            end: Конечная вершина

        Returns:
            tuple: (путь, длина) или None если путь не существует
        """
        distances, parents = ShortestPath.dijkstra(graph, start)

        if distances[end] == float('inf'):
            return None

        path = []
        current = end

        while current is not None:
            path.append(current)
            current = parents[current]

        return path[::-1], distances[end]

    @staticmethod
    def bellman_ford(graph: graph_representation.AdjacencyListGraph, start: str) -> Optional[
        Tuple[Dict[str, float], Dict[str, Optional[str]]]]:
        """
        Алгоритм Беллмана-Форда для графов с отрицательными весами (но без отрицательных циклов).

        Сложность: O(V * E)

        Args:
            graph: Взвешенный граф (может содержать отрицательные веса)
            start: Стартовая вершина

        Returns:
            tuple: (расстояния, родители) или None если обнаружен отрицательный цикл
        """
        if not graph.weighted:
            raise ValueError("Алгоритм Беллмана-Форда требует взвешенный граф")

        distances = {vertex: float('inf') for vertex in graph.get_vertices()}
        parents = {vertex: None for vertex in graph.get_vertices()}
        distances[start] = 0

        edges = graph.get_edges()

        # Релаксация рёбер V-1 раз
        for _ in range(len(graph.get_vertices()) - 1):
            updated = False

            for u, v, weight in edges:
                if distances[u] != float('inf') and distances[u] + weight < distances[v]:
                    distances[v] = distances[u] + weight
                    parents[v] = u
                    updated = True

            if not updated:
                break

        # Проверка на отрицательные циклы
        for u, v, weight in edges:
            if distances[u] != float('inf') and distances[u] + weight < distances[v]:
                return None  # Обнаружен отрицательный цикл

        return distances, parents

    @staticmethod
    def floyd_warshall(graph: graph_representation.AdjacencyMatrixGraph) -> Tuple[
        List[List[float]], List[List[Optional[int]]]]:
        """
        Алгоритм Флойда-Уоршелла для поиска кратчайших путей между всеми парами вершин.

        Сложность: O(V³)

        Args:
            graph: Граф в виде матрицы смежности

        Returns:
            tuple: (матрица расстояний, матрица следующих вершин)
        """
        if not graph.weighted:
            raise ValueError("Алгоритм Флойда-Уоршелла требует взвешенный граф")

        n = len(graph.vertices)
        dist = [[float('inf')] * n for _ in range(n)]
        next_vertex = [[None] * n for _ in range(n)]

        # Инициализация
        for i in range(n):
            dist[i][i] = 0
            for j in range(n):
                if graph.matrix[i][j] != float('inf'):
                    dist[i][j] = graph.matrix[i][j]
                    next_vertex[i][j] = j

        # Основной алгоритм
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    if dist[i][k] != float('inf') and dist[k][j] != float('inf'):
                        if dist[i][j] > dist[i][k] + dist[k][j]:
                            dist[i][j] = dist[i][k] + dist[k][j]
                            next_vertex[i][j] = next_vertex[i][k]

        return dist, next_vertex

    @staticmethod
    def reconstruct_path_floyd(next_vertex: List[List[Optional[int]]],
                               vertices: List[str],
                               start: str,
                               end: str) -> Optional[List[str]]:
        """
        Восстановление пути из матрицы следующей вершины алгоритма Флойда-Уоршелла.

        Args:
            next_vertex: Матрица следующих вершин
            vertices: Список вершин
            start: Начальная вершина
            end: Конечная вершина

        Returns:
            Кратчайший путь или None если путь не существует
        """
        if start not in vertices or end not in vertices:
            return None

        i = vertices.index(start)
        j = vertices.index(end)

        if next_vertex[i][j] is None:
            return None

        path = [start]

        while i != j:
            i = next_vertex[i][j]
            path.append(vertices[i])

        return path


class MazeSolver:
    """
    Класс для решения задач на графах, связанных с лабиринтами.
    """

    @staticmethod
    def maze_to_graph(maze: List[List[int]]) -> graph_representation.AdjacencyListGraph:
        """
        Преобразование лабиринта в граф.

        Args:
            maze: Двумерный список, где 0 - стена, 1 - проход

        Returns:
            Граф представляющий лабиринт
        """
        graph = graph_representation.AdjacencyListGraph(directed=False, weighted=False)
        rows = len(maze)
        cols = len(maze[0]) if rows > 0 else 0

        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # вправо, вниз, влево, вверх

        for i in range(rows):
            for j in range(cols):
                if maze[i][j] == 1:  # Проход
                    vertex = f"{i},{j}"
                    graph.add_vertex(vertex)

                    for dx, dy in directions:
                        ni, nj = i + dx, j + dy
                        if 0 <= ni < rows and 0 <= nj < cols and maze[ni][nj] == 1:
                            neighbor = f"{ni},{nj}"
                            graph.add_edge(vertex, neighbor)

        return graph

    @staticmethod
    def solve_maze(maze: List[List[int]], start: Tuple[int, int], end: Tuple[int, int]) -> Optional[
        List[Tuple[int, int]]]:
        """
        Поиск пути в лабиринте от start до end.

        Args:
            maze: Двумерный список лабиринта
            start: Координаты начала (row, col)
            end: Координаты конца (row, col)

        Returns:
            Список координат пути или None если путь не существует
        """
        graph = MazeSolver.maze_to_graph(maze)
        start_vertex = f"{start[0]},{start[1]}"
        end_vertex = f"{end[0]},{end[1]}"

        path = GraphTraversal.bfs_path(graph, start_vertex, end_vertex)

        if path is None:
            return None

        return [(int(coord.split(',')[0]), int(coord.split(',')[1])) for coord in path]