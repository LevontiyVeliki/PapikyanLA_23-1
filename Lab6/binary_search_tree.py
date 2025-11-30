"""
Реализация бинарного дерева поиска (BST) на основе узлов.
"""

class TreeNode:
    """Класс узла бинарного дерева поиска."""

    def __init__(self, value):
        """
        Инициализация узла.

        Args:
            value: Значение узла
        """
        self.value = value
        self.left = None
        self.right = None

    def __str__(self):
        """Строковое представление узла."""
        return f"TreeNode({self.value})"


class BinarySearchTree:
    """Класс бинарного дерева поиска."""

    def __init__(self):
        """Инициализация пустого дерева."""
        self.root = None

    def insert(self, value):
        """
        Вставка нового значения в дерево.

        Сложность:
            Средний случай: O(log n)
            Худший случай: O(n) - вырожденное дерево

        Args:
            value: Значение для вставки
        """
        if self.root is None:
            self.root = TreeNode(value)
        else:
            self._insert_recursive(self.root, value)

    def _insert_recursive(self, node, value):
        """
        Рекурсивная вспомогательная функция для вставки.

        Args:
            node: Текущий узел
            value: Значение для вставки
        """
        if value < node.value:
            if node.left is None:
                node.left = TreeNode(value)
            else:
                self._insert_recursive(node.left, value)
        elif value > node.value:
            if node.right is None:
                node.right = TreeNode(value)
            else:
                self._insert_recursive(node.right, value)
        # Если значение уже существует, ничего не делаем

    def search(self, value):
        """
        Поиск значения в дереве.

        Сложность:
            Средний случай: O(log n)
            Худший случай: O(n) - вырожденное дерево

        Args:
            value: Значение для поиска

        Returns:
            TreeNode: Найденный узел или None
        """
        return self._search_recursive(self.root, value)

    def _search_recursive(self, node, value):
        """
        Рекурсивная вспомогательная функция для поиска.

        Args:
            node: Текущий узел
            value: Значение для поиска

        Returns:
            TreeNode: Найденный узел или None
        """
        if node is None or node.value == value:
            return node

        if value < node.value:
            return self._search_recursive(node.left, value)
        else:
            return self._search_recursive(node.right, value)

    def delete(self, value):
        """
        Удаление значения из дерева.

        Сложность:
            Средний случай: O(log n)
            Худший случай: O(n) - вырожденное дерево

        Args:
            value: Значение для удаления

        Returns:
            bool: True если удаление успешно, False если значение не найдено
        """
        if self.root is None:
            return False

        # Проверяем, существует ли значение перед удалением
        if self.search(value) is None:
            return False

        self.root = self._delete_recursive(self.root, value)
        return True

    def _delete_recursive(self, node, value):
        """
        Рекурсивная вспомогательная функция для удаления.

        Args:
            node: Текущий узел
            value: Значение для удаления

        Returns:
            TreeNode: Новый корень поддерева
        """
        if node is None:
            return node

        # Поиск узла для удаления
        if value < node.value:
            node.left = self._delete_recursive(node.left, value)
        elif value > node.value:
            node.right = self._delete_recursive(node.right, value)
        else:
            # Узел найден - обработка трех случаев

            # Случай 1: Узел без потомков или с одним потомком
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left

            # Случай 2: Узел с двумя потомками
            # Находим минимальный узел в правом поддереве
            min_node = self._find_min_node(node.right)
            node.value = min_node.value
            node.right = self._delete_recursive(node.right, min_node.value)

        return node

    def _find_min_node(self, node):
        """
        Поиск узла с минимальным значением в поддереве.

        Args:
            node: Корень поддерева

        Returns:
            TreeNode: Узел с минимальным значением
        """
        current = node
        while current.left is not None:
            current = current.left
        return current

    def find_min(self, node=None):
        """
        Поиск минимального значения в поддереве.

        Сложность: O(h), где h - высота поддерева

        Args:
            node: Корень поддерева (по умолчанию - корень всего дерева)

        Returns:
            TreeNode: Узел с минимальным значением
        """
        if node is None:
            node = self.root

        if node is None:
            return None

        return self._find_min_node(node)

    def find_max(self, node=None):
        """
        Поиск максимального значения в поддереве.

        Сложность: O(h), где h - высота поддерева

        Args:
            node: Корень поддерева (по умолчанию - корень всего дерева)

        Returns:
            TreeNode: Узел с максимальным значением
        """
        if node is None:
            node = self.root

        if node is None:
            return None

        current = node
        while current.right is not None:
            current = current.right

        return current

    def height(self, node=None):
        """
        Вычисление высоты дерева/поддерева.

        Сложность: O(n) - необходимо посетить все узлы

        Args:
            node: Корень поддерева (по умолчанию - корень всего дерева)

        Returns:
            int: Высота дерева
        """
        if node is None:
            node = self.root

        if node is None:
            return -1  # Высота пустого дерева

        left_height = self.height(node.left) if node.left else -1
        right_height = self.height(node.right) if node.right else -1

        return max(left_height, right_height) + 1

    def is_valid_bst(self):
        """
        Проверка, является ли дерево корректным BST.

        Сложность: O(n) - необходимо проверить все узлы

        Returns:
            bool: True если дерево корректно, False в противном случае
        """
        return self._is_valid_recursive(self.root, float('-inf'), float('inf'))

    def _is_valid_recursive(self, node, min_val, max_val):
        """
        Рекурсивная проверка корректности BST.

        Args:
            node: Текущий узел
            min_val: Минимально допустимое значение
            max_val: Максимально допустимое значение

        Returns:
            bool: True если поддерево корректно
        """
        if node is None:
            return True

        if not (min_val < node.value < max_val):
            return False

        return (self._is_valid_recursive(node.left, min_val, node.value) and
                self._is_valid_recursive(node.right, node.value, max_val))

    def __contains__(self, value):
        """Проверка наличия значения в дереве."""
        return self.search(value) is not None

    def __str__(self):
        """Строковое представление дерева."""
        return self._visualize()

    def _visualize(self, node=None, prefix="", is_left=True):
        """
        Текстовая визуализация дерева.

        Args:
            node: Текущий узел
            prefix: Префикс для отступов
            is_left: Является ли узел левым потомком

        Returns:
            str: Визуализация дерева в виде строки
        """
        if node is None:
            node = self.root

        if node is None:
            return "Empty tree"

        result = ""

        if node.right:
            result += self._visualize(node.right, prefix + ("│   " if is_left else "    "), False)

        result += prefix + ("└── " if is_left else "┌── ") + str(node.value) + "\n"

        if node.left:
            result += self._visualize(node.left, prefix + ("    " if is_left else "│   "), True)

        return result

    def get_size(self):
        """
        Получение количества элементов в дереве.

        Returns:
            int: Количество элементов
        """
        return self._get_size_recursive(self.root)

    def _get_size_recursive(self, node):
        """
        Рекурсивный подсчет количества элементов.

        Args:
            node: Текущий узел

        Returns:
            int: Количество элементов в поддереве
        """
        if node is None:
            return 0
        return 1 + self._get_size_recursive(node.left) + self._get_size_recursive(node.right)