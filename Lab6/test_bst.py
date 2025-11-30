"""
Unit-тесты для проверки корректности реализации BST.
"""

import unittest
from binary_search_tree import BinarySearchTree, TreeNode
from tree_traversal import *


class TestBinarySearchTree(unittest.TestCase):
    """Тесты для бинарного дерева поиска."""

    def setUp(self):
        """Настройка тестового окружения."""
        self.bst = BinarySearchTree()

    def test_insert_and_search(self):
        """Тест вставки и поиска."""
        values = [50, 30, 70, 20, 40, 60, 80]

        for value in values:
            self.bst.insert(value)

        # Проверка поиска существующих значений
        for value in values:
            node = self.bst.search(value)
            self.assertIsNotNone(node)
            self.assertEqual(node.value, value)

        # Проверка поиска несуществующих значений
        self.assertIsNone(self.bst.search(100))
        self.assertIsNone(self.bst.search(10))

    def test_delete(self):
        """Тест удаления элементов."""
        values = [50, 30, 70, 20, 40, 60, 80]

        for value in values:
            self.bst.insert(value)

        # Удаление листа
        success = self.bst.delete(20)
        self.assertTrue(success)
        self.assertIsNone(self.bst.search(20))
        self.assertTrue(self.bst.is_valid_bst())

        # Удаление узла с одним потомком
        success = self.bst.delete(30)
        self.assertTrue(success)
        self.assertIsNone(self.bst.search(30))
        self.assertTrue(self.bst.is_valid_bst())

        # Удаление узла с двумя потомками
        success = self.bst.delete(50)
        self.assertTrue(success)
        self.assertIsNone(self.bst.search(50))
        self.assertTrue(self.bst.is_valid_bst())

        # Удаление несуществующего элемента
        success = self.bst.delete(100)
        self.assertFalse(success)

    def test_find_min_max(self):
        """Тест поиска минимального и максимального значений."""
        values = [50, 30, 70, 20, 40, 60, 80]

        for value in values:
            self.bst.insert(value)

        self.assertEqual(self.bst.find_min().value, 20)
        self.assertEqual(self.bst.find_max().value, 80)

        # Поиск в поддереве
        node_30 = self.bst.search(30)
        self.assertEqual(self.bst.find_min(node_30).value, 20)
        self.assertEqual(self.bst.find_max(node_30).value, 40)

    def test_height(self):
        """Тест вычисления высоты."""
        # Пустое дерево
        self.assertEqual(self.bst.height(), -1)

        # Дерево с одним элементом
        self.bst.insert(50)
        self.assertEqual(self.bst.height(), 0)

        # Сбалансированное дерево
        self.bst.insert(30)
        self.bst.insert(70)
        self.assertEqual(self.bst.height(), 1)

        # Добавляем еще уровней
        self.bst.insert(20)
        self.bst.insert(40)
        self.assertEqual(self.bst.height(), 2)

    def test_is_valid_bst(self):
        """Тест проверки корректности BST."""
        # Корректное BST
        values = [50, 30, 70, 20, 40, 60, 80]
        for value in values:
            self.bst.insert(value)
        self.assertTrue(self.bst.is_valid_bst())

        # Создаем некорректное BST вручную
        self.bst.root = TreeNode(50)
        self.bst.root.left = TreeNode(60)  # Нарушение свойства BST
        self.bst.root.right = TreeNode(70)
        self.assertFalse(self.bst.is_valid_bst())

    def test_traversals(self):
        """Тест различных методов обхода."""
        values = [50, 30, 70, 20, 40, 60, 80]
        sorted_values = sorted(values)

        for value in values:
            self.bst.insert(value)

        # In-order обход должен возвращать отсортированные значения
        self.assertEqual(inorder_recursive(self.bst.root), sorted_values)
        self.assertEqual(inorder_iterative(self.bst.root), sorted_values)

        # Pre-order обход
        preorder_result = preorder_recursive(self.bst.root)
        self.assertEqual(preorder_result[0], 50)  # Корень первый

        # Post-order обход
        postorder_result = postorder_recursive(self.bst.root)
        self.assertEqual(postorder_result[-1], 50)  # Корень последний

        # Level-order обход
        level_order = level_order_traversal(self.bst.root)
        self.assertEqual(len(level_order), len(values))

    def test_size(self):
        """Тест подсчета размера дерева."""
        # Пустое дерево
        self.assertEqual(self.bst.get_size(), 0)

        # Дерево с элементами
        values = [50, 30, 70, 20, 40]
        for value in values:
            self.bst.insert(value)

        self.assertEqual(self.bst.get_size(), len(values))

        # После удаления
        self.bst.delete(30)
        self.assertEqual(self.bst.get_size(), len(values) - 1)


if __name__ == "__main__":
    unittest.main()