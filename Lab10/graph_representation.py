"""
Реализация различных представлений графов: матрица смежности и список смежности.
"""

from typing import List, Dict, Set, Tuple, Optional, Union
import sys


class AdjacencyMatrixGraph:
    """
    Представление графа в виде матрицы смежности.
    """

    def __init__(self, directed: bool = False, weighted: bool = False):
        """
        Инициализация графа.

        Args:
            directed: Ориентированный ли граф
            weighted: Взвешенный ли граф
        """
        self.directed = directed
        self.weighted = weighted
        self.vertices = []  # Список вершин
        self.vertex_index = {}  # Сопоставление вершины с индексом
        self.matrix = []  # Матрица смежности

    def add_vertex(self, vertex: str) -> None:
        """
        Добавление вершины в граф.

        Сложность: O(V) - при необходимости расширения матрицы

        Args:
            vertex: Имя вершины
        """
        if vertex in self.vertex_index:
            return

        self.vertices.append(vertex)
        self.vertex_index[vertex] = len(self.vertices) - 1

        # Расширяем матрицу
        for row in self.matrix:
            row.append(0 if not self.weighted else float('inf'))

        new_row = [0] * len(self.vertices) if not self.weighted else [float('inf')] * len(self.vertices)
        self.matrix.append(new_row)

        # Диагональ для невзвешенных графов
        if not self.weighted:
            self.matrix[-1][-1] = 0

    def add_edge(self, u: str, v: str, weight: float = 1) -> None:
        """
        Добавление ребра между вершинами.

        Сложность: O(1) - доступ по индексу

        Args:
            u: Начальная вершина
            v: Конечная вершина
            weight: Вес ребра (для взвешенных графов)
        """
        if u not in self.vertex_index or v not in self.vertex_index:
            raise ValueError("Вершины не существуют в графе")

        u_idx = self.vertex_index[u]
        v_idx = self.vertex_index[v]

        if self.weighted:
            self.matrix[u_idx][v_idx] = weight
            if not self.directed:
                self.matrix[v_idx][u_idx] = weight
        else:
            self.matrix[u_idx][v_idx] = 1
            if not self.directed:
                self.matrix[v_idx][u_idx] = 1

    def remove_edge(self, u: str, v: str) -> None:
        """
        Удаление ребра между вершинами.

        Сложность: O(1)

        Args:
            u: Начальная вершина
            v: Конечная вершина
        """
        if u not in self.vertex_index or v not in self.vertex_index:
            return

        u_idx = self.vertex_index[u]
        v_idx = self.vertex_index[v]

        if self.weighted:
            self.matrix[u_idx][v_idx] = float('inf')
            if not self.directed:
                self.matrix[v_idx][u_idx] = float('inf')
        else:
            self.matrix[u_idx][v_idx] = 0
            if not self.directed:
                self.matrix[v_idx][u_idx] = 0

    def get_neighbors(self, vertex: str) -> List[Tuple[str, float]]:
        """
        Получение соседей вершины.

        Сложность: O(V) - нужно проверить всю строку

        Args:
            vertex: Вершина

        Returns:
            Список соседей с весами
        """
        if vertex not in self.vertex_index:
            return []

        idx = self.vertex_index[vertex]
        neighbors = []

        for i, weight in enumerate(self.matrix[idx]):
            if i != idx and ((not self.weighted and weight != 0) or
                             (self.weighted and weight != float('inf'))):
                neighbors.append((self.vertices[i], weight))

        return neighbors

    def has_edge(self, u: str, v: str) -> bool:
        """
        Проверка существования ребра.

        Сложность: O(1)

        Args:
            u: Начальная вершина
            v: Конечная вершина

        Returns:
            True если ребро существует
        """
        if u not in self.vertex_index or v not in self.vertex_index:
            return False

        u_idx = self.vertex_index[u]
        v_idx = self.vertex_index[v]

        if self.weighted:
            return self.matrix[u_idx][v_idx] != float('inf')
        else:
            return self.matrix[u_idx][v_idx] != 0

    def get_vertices(self) -> List[str]:
        """
        Получение списка всех вершин.

        Сложность: O(1)

        Returns:
            Список вершин
        """
        return self.vertices.copy()

    def get_edges(self) -> List[Tuple[str, str, float]]:
        """
        Получение списка всех рёбер.

        Сложность: O(V²)

        Returns:
            Список рёбер в формате (u, v, weight)
        """
        edges = []
        n = len(self.vertices)

        for i in range(n):
            for j in range(n):
                if i != j and ((not self.weighted and self.matrix[i][j] != 0) or
                               (self.weighted and self.matrix[i][j] != float('inf'))):
                    # Для неориентированных графов добавляем каждое ребро только один раз
                    if not self.directed and i > j:
                        continue
                    edges.append((self.vertices[i], self.vertices[j], self.matrix[i][j]))

        return edges

    def __str__(self) -> str:
        """Строковое представление графа."""
        result = "Матрица смежности:\n"
        result += "    " + " ".join(f"{v:>3}" for v in self.vertices) + "\n"

        for i, vertex in enumerate(self.vertices):
            row = [f"{val:>3}" for val in self.matrix[i]]
            result += f"{vertex:>3} " + " ".join(row) + "\n"

        return result

    def memory_usage(self) -> int:
        """
        Оценка использования памяти в байтах.

        Returns:
            Приблизительное использование памяти
        """
        # Память для матрицы + списка вершин + словаря
        matrix_memory = len(self.matrix) * len(self.matrix[0]) * 24 if self.matrix else 0  # float ~24 bytes
        vertices_memory = sum(sys.getsizeof(v) for v in self.vertices)
        index_memory = sum(sys.getsizeof(k) + sys.getsizeof(v) for k, v in self.vertex_index.items())

        return matrix_memory + vertices_memory + index_memory


class AdjacencyListGraph:
    """
    Представление графа в виде списка смежности.
    """

    def __init__(self, directed: bool = False, weighted: bool = False):
        """
        Инициализация графа.

        Args:
            directed: Ориентированный ли граф
            weighted: Взвешенный ли граф
        """
        self.directed = directed
        self.weighted = weighted
        self.adj_list: Dict[str, Dict[str, float]] = {}

    def add_vertex(self, vertex: str) -> None:
        """
        Добавление вершины в граф.

        Сложность: O(1)

        Args:
            vertex: Имя вершины
        """
        if vertex not in self.adj_list:
            self.adj_list[vertex] = {}

    def add_edge(self, u: str, v: str, weight: float = 1) -> None:
        """
        Добавление ребра между вершинами.

        Сложность: O(1)

        Args:
            u: Начальная вершина
            v: Конечная вершина
            weight: Вес ребра (для взвешенных графов)
        """
        if u not in self.adj_list:
            self.add_vertex(u)
        if v not in self.adj_list:
            self.add_vertex(v)

        self.adj_list[u][v] = weight
        if not self.directed:
            self.adj_list[v][u] = weight

    def remove_edge(self, u: str, v: str) -> None:
        """
        Удаление ребра между вершинами.

        Сложность: O(1)

        Args:
            u: Начальная вершина
            v: Конечная вершина
        """
        if u in self.adj_list and v in self.adj_list[u]:
            del self.adj_list[u][v]
            if not self.directed and v in self.adj_list and u in self.adj_list[v]:
                del self.adj_list[v][u]

    def get_neighbors(self, vertex: str) -> List[Tuple[str, float]]:
        """
        Получение соседей вершины.

        Сложность: O(deg(v)) - степень вершины

        Args:
            vertex: Вершина

        Returns:
            Список соседей с весами
        """
        if vertex not in self.adj_list:
            return []

        return list(self.adj_list[vertex].items())

    def has_edge(self, u: str, v: str) -> bool:
        """
        Проверка существования ребра.

        Сложность: O(1) в среднем

        Args:
            u: Начальная вершина
            v: Конечная вершина

        Returns:
            True если ребро существует
        """
        return u in self.adj_list and v in self.adj_list[u]

    def get_vertices(self) -> List[str]:
        """
        Получение списка всех вершин.

        Сложность: O(V)

        Returns:
            Список вершин
        """
        return list(self.adj_list.keys())

    def get_edges(self) -> List[Tuple[str, str, float]]:
        """
        Получение списка всех рёбер.

        Сложность: O(V + E)

        Returns:
            Список рёбер в формате (u, v, weight)
        """
        edges = []

        for u in self.adj_list:
            for v, weight in self.adj_list[u].items():
                # Для неориентированных графов добавляем каждое ребро только один раз
                if not self.directed and u > v:
                    continue
                edges.append((u, v, weight))

        return edges

    def __str__(self) -> str:
        """Строковое представление графа."""
        result = "Список смежности:\n"

        for vertex, neighbors in sorted(self.adj_list.items()):
            neighbor_str = ", ".join(f"{n}({w})" for n, w in neighbors.items())
            result += f"{vertex}: [{neighbor_str}]\n"

        return result

    def memory_usage(self) -> int:
        """
        Оценка использования памяти в байтах.

        Returns:
            Приблизительное использование памяти
        """
        total_memory = 0

        for vertex, neighbors in self.adj_list.items():
            total_memory += sys.getsizeof(vertex)  # Вершина
            total_memory += sys.getsizeof(neighbors)  # Словарь соседей

            for neighbor, weight in neighbors.items():
                total_memory += sys.getsizeof(neighbor)  # Сосед
                total_memory += sys.getsizeof(weight)  # Вес

        return total_memory


class GraphAnalyzer:
    """
    Класс для анализа производительности представлений графов.
    """

    @staticmethod
    def compare_operations(graph_matrix: AdjacencyMatrixGraph,
                           graph_list: AdjacencyListGraph,
                           operations: int = 1000) -> Dict[str, float]:
        """
        Сравнение времени выполнения операций.

        Args:
            graph_matrix: Граф с матрицей смежности
            graph_list: Граф со списком смежности
            operations: Количество операций для теста

        Returns:
            Словарь с временем выполнения операций
        """
        import time
        import random

        vertices = graph_matrix.get_vertices()
        if not vertices:
            return {}

        results = {}

        # Тест добавления рёбер
        start = time.perf_counter()
        for _ in range(operations):
            u, v = random.sample(vertices, 2)
            graph_matrix.add_edge(u, v, 1)
        results['matrix_add_edge'] = time.perf_counter() - start

        start = time.perf_counter()
        for _ in range(operations):
            u, v = random.sample(vertices, 2)
            graph_list.add_edge(u, v, 1)
        results['list_add_edge'] = time.perf_counter() - start

        # Тест проверки рёбер
        start = time.perf_counter()
        for _ in range(operations):
            u, v = random.sample(vertices, 2)
            graph_matrix.has_edge(u, v)
        results['matrix_has_edge'] = time.perf_counter() - start

        start = time.perf_counter()
        for _ in range(operations):
            u, v = random.sample(vertices, 2)
            graph_list.has_edge(u, v)
        results['list_has_edge'] = time.perf_counter() - start

        # Тест получения соседей
        start = time.perf_counter()
        for _ in range(operations):
            v = random.choice(vertices)
            graph_matrix.get_neighbors(v)
        results['matrix_get_neighbors'] = time.perf_counter() - start

        start = time.perf_counter()
        for _ in range(operations):
            v = random.choice(vertices)
            graph_list.get_neighbors(v)
        results['list_get_neighbors'] = time.perf_counter() - start

        return results