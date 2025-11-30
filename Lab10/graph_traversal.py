"""
Реализация алгоритмов обхода графов: BFS и DFS.
"""

from typing import List, Dict, Set, Tuple, Optional, Deque
from collections import deque
import graph_representation


class GraphTraversal:
    """
    Класс, содержащий алгоритмы обхода графов.
    """

    @staticmethod
    def bfs(graph: graph_representation.AdjacencyListGraph, start: str) -> Tuple[
        Dict[str, int], Dict[str, Optional[str]]]:
        """
        Поиск в ширину (BFS).

        Сложность: O(V + E)

        Args:
            graph: Граф для обхода
            start: Стартовая вершина

        Returns:
            tuple: (расстояния, родители)
        """
        distances = {start: 0}
        parents = {start: None}
        queue = deque([start])

        while queue:
            current = queue.popleft()
            current_distance = distances[current]

            for neighbor, _ in graph.get_neighbors(current):
                if neighbor not in distances:
                    distances[neighbor] = current_distance + 1
                    parents[neighbor] = current
                    queue.append(neighbor)

        return distances, parents

    @staticmethod
    def bfs_path(graph: graph_representation.AdjacencyListGraph, start: str, end: str) -> Optional[List[str]]:
        """
        Поиск кратчайшего пути с помощью BFS.

        Сложность: O(V + E)

        Args:
            graph: Граф для обхода
            start: Стартовая вершина
            end: Конечная вершина

        Returns:
            Кратчайший путь или None если путь не существует
        """
        _, parents = GraphTraversal.bfs(graph, start)

        if end not in parents:
            return None

        path = []
        current = end

        while current is not None:
            path.append(current)
            current = parents[current]

        return path[::-1]

    @staticmethod
    def dfs_recursive(graph: graph_representation.AdjacencyListGraph, start: str) -> Dict[str, int]:
        """
        Рекурсивный поиск в глубину (DFS).

        Сложность: O(V + E)

        Args:
            graph: Граф для обхода
            start: Стартовая вершина

        Returns:
            Словарь с порядком посещения вершин
        """
        visited = {}
        order = [0]  # Используем список для mutable counter

        def _dfs(current: str):
            visited[current] = order[0]
            order[0] += 1

            for neighbor, _ in graph.get_neighbors(current):
                if neighbor not in visited:
                    _dfs(neighbor)

        _dfs(start)
        return visited

    @staticmethod
    def dfs_iterative(graph: graph_representation.AdjacencyListGraph, start: str) -> Dict[str, int]:
        """
        Итеративный поиск в глубину (DFS).

        Сложность: O(V + E)

        Args:
            graph: Граф для обхода
            start: Стартовая вершина

        Returns:
            Словарь с порядком посещения вершин
        """
        visited = {}
        stack = [start]
        order = 0

        while stack:
            current = stack.pop()

            if current not in visited:
                visited[current] = order
                order += 1

                # Добавляем соседей в обратном порядке для соответствия рекурсивной версии
                neighbors = [n for n, _ in graph.get_neighbors(current)]
                for neighbor in reversed(neighbors):
                    if neighbor not in visited:
                        stack.append(neighbor)

        return visited

    @staticmethod
    def topological_sort(graph: graph_representation.AdjacencyListGraph) -> Optional[List[str]]:
        """
        Топологическая сортировка для ориентированного ациклического графа (DAG).

        Сложность: O(V + E)

        Args:
            graph: Ориентированный граф

        Returns:
            Топологический порядок или None если граф циклический
        """
        if not graph.directed:
            raise ValueError("Топологическая сортировка применима только к ориентированным графам")

        visited = set()
        temp_visited = set()
        result = []

        def visit(vertex: str) -> bool:
            if vertex in temp_visited:
                return False  # Обнаружен цикл
            if vertex in visited:
                return True

            temp_visited.add(vertex)

            for neighbor, _ in graph.get_neighbors(vertex):
                if not visit(neighbor):
                    return False

            temp_visited.remove(vertex)
            visited.add(vertex)
            result.append(vertex)
            return True

        for vertex in graph.get_vertices():
            if vertex not in visited:
                if not visit(vertex):
                    return None  # Граф содержит цикл

        return result[::-1]

    @staticmethod
    def connected_components(graph: graph_representation.AdjacencyListGraph) -> List[List[str]]:
        """
        Поиск компонент связности в неориентированном графе.

        Сложность: O(V + E)

        Args:
            graph: Неориентированный граф

        Returns:
            Список компонент связности
        """
        if graph.directed:
            raise ValueError("Для ориентированных графов используйте strongly_connected_components")

        visited = set()
        components = []

        for vertex in graph.get_vertices():
            if vertex not in visited:
                # Используем BFS для нахождения компоненты
                component = []
                queue = deque([vertex])
                visited.add(vertex)

                while queue:
                    current = queue.popleft()
                    component.append(current)

                    for neighbor, _ in graph.get_neighbors(current):
                        if neighbor not in visited:
                            visited.add(neighbor)
                            queue.append(neighbor)

                components.append(component)

        return components

    @staticmethod
    def is_bipartite(graph: graph_representation.AdjacencyListGraph) -> bool:
        """
        Проверка является ли граф двудольным.

        Сложность: O(V + E)

        Args:
            graph: Граф для проверки

        Returns:
            True если граф двудольный
        """
        if graph.directed:
            # Для ориентированных графов рассматриваем как неориентированный
            pass

        color = {}

        for vertex in graph.get_vertices():
            if vertex not in color:
                queue = deque([vertex])
                color[vertex] = 0

                while queue:
                    current = queue.popleft()
                    current_color = color[current]

                    for neighbor, _ in graph.get_neighbors(current):
                        if neighbor not in color:
                            color[neighbor] = 1 - current_color
                            queue.append(neighbor)
                        elif color[neighbor] == current_color:
                            return False

        return True


class GraphCycleDetection:
    """
    Класс для обнаружения циклов в графах.
    """

    @staticmethod
    def has_cycle_undirected(graph: graph_representation.AdjacencyListGraph) -> bool:
        """
        Проверка наличия циклов в неориентированном графе.

        Сложность: O(V + E)

        Args:
            graph: Неориентированный граф

        Returns:
            True если граф содержит цикл
        """
        if graph.directed:
            raise ValueError("Для ориентированных графов используйте has_cycle_directed")

        visited = set()

        def dfs(current: str, parent: Optional[str]) -> bool:
            visited.add(current)

            for neighbor, _ in graph.get_neighbors(current):
                if neighbor == parent:
                    continue
                if neighbor in visited or dfs(neighbor, current):
                    return True

            return False

        for vertex in graph.get_vertices():
            if vertex not in visited:
                if dfs(vertex, None):
                    return True

        return False

    @staticmethod
    def has_cycle_directed(graph: graph_representation.AdjacencyListGraph) -> bool:
        """
        Проверка наличия циклов в ориентированном графе.

        Сложность: O(V + E)

        Args:
            graph: Ориентированный граф

        Returns:
            True если граф содержит цикл
        """
        if not graph.directed:
            raise ValueError("Для неориентированных графов используйте has_cycle_undirected")

        visited = set()
        recursion_stack = set()

        def dfs(current: str) -> bool:
            visited.add(current)
            recursion_stack.add(current)

            for neighbor, _ in graph.get_neighbors(current):
                if neighbor not in visited:
                    if dfs(neighbor):
                        return True
                elif neighbor in recursion_stack:
                    return True

            recursion_stack.remove(current)
            return False

        for vertex in graph.get_vertices():
            if vertex not in visited:
                if dfs(vertex):
                    return True

        return False