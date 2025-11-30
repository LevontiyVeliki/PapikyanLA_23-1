"""
Демонстрация работы бинарного дерева поиска.
"""

from binary_search_tree import BinarySearchTree
from tree_traversal import *
from analysis import generate_balanced_tree, generate_degenerate_tree


def demonstrate_bst_operations():
    """Демонстрация основных операций с BST."""
    print("=== ДЕМОНСТРАЦИЯ ОСНОВНЫХ ОПЕРАЦИЙ BST ===\n")

    bst = BinarySearchTree()

    # Вставка элементов
    values = [50, 30, 70, 20, 40, 60, 80, 10, 25, 35, 45]
    print(f"Вставляем значения: {values}")

    for value in values:
        bst.insert(value)

    print("\nСтруктура дерева:")
    print(bst._visualize())

    # Проверка свойств
    print(f"Размер дерева: {bst.get_size()}")
    print(f"Высота дерева: {bst.height()}")
    print(f"Минимальное значение: {bst.find_min().value}")
    print(f"Максимальное значение: {bst.find_max().value}")
    print(f"Является корректным BST: {bst.is_valid_bst()}")

    # Обходы
    print(f"\nIn-order обход (рекурсивный): {inorder_recursive(bst.root)}")
    print(f"In-order обход (итеративный): {inorder_iterative(bst.root)}")
    print(f"Pre-order обход: {preorder_recursive(bst.root)}")
    print(f"Post-order обход: {postorder_recursive(bst.root)}")
    print(f"Level-order обход: {level_order_traversal(bst.root)}")

    # Поиск
    search_values = [40, 55, 20]
    for value in search_values:
        result = bst.search(value)
        if result:
            print(f"Значение {value} найдено в дереве")
        else:
            print(f"Значение {value} не найдено в дереве")

    # Удаление
    delete_values = [20, 30, 50]
    for value in delete_values:
        print(f"\nУдаляем значение {value}")
        success = bst.delete(value)
        if success:
            print(f"Удаление успешно")
            print(f"In-order после удаления: {inorder_recursive(bst.root)}")
            print(f"Является корректным BST: {bst.is_valid_bst()}")
            print(f"Размер дерева после удаления: {bst.get_size()}")
        else:
            print(f"Значение {value} не найдено для удаления")


def demonstrate_tree_comparison():
    """Демонстрация сравнения сбалансированного и вырожденного деревьев."""
    print("\n\n=== СРАВНЕНИЕ СБАЛАНСИРОВАННОГО И ВЫРОЖДЕННОГО ДЕРЕВЬЕВ ===\n")

    size = 15

    # Сбалансированное дерево
    balanced_bst, _ = generate_balanced_tree(size)
    print("Сбалансированное дерево (случайные значения):")
    print(balanced_bst._visualize())
    print(f"Высота: {balanced_bst.height()}")
    print(f"Размер: {balanced_bst.get_size()}")

    # Вырожденное дерево
    degenerate_bst, _ = generate_degenerate_tree(size)
    print("\nВырожденное дерево (отсортированные значения):")
    print(degenerate_bst._visualize())
    print(f"Высота: {degenerate_bst.height()}")
    print(f"Размер: {degenerate_bst.get_size()}")


if __name__ == "__main__":
    demonstrate_bst_operations()
    demonstrate_tree_comparison()