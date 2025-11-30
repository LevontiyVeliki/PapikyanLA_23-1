"""
Реализация различных методов обхода бинарного дерева.
"""

def inorder_recursive(node, result=None):
    """
    Рекурсивный in-order обход (левый-корень-правый).

    Сложность: O(n) - посещаются все узлы

    Args:
        node: Корень дерева/поддерева
        result: Список для сохранения результатов

    Returns:
        list: Узлы в порядке in-order
    """
    if result is None:
        result = []

    if node:
        inorder_recursive(node.left, result)
        result.append(node.value)
        inorder_recursive(node.right, result)

    return result


def preorder_recursive(node, result=None):
    """
    Рекурсивный pre-order обход (корень-левый-правый).

    Сложность: O(n) - посещаются все узлы

    Args:
        node: Корень дерева/поддерева
        result: Список для сохранения результатов

    Returns:
        list: Узлы в порядке pre-order
    """
    if result is None:
        result = []

    if node:
        result.append(node.value)
        preorder_recursive(node.left, result)
        preorder_recursive(node.right, result)

    return result


def postorder_recursive(node, result=None):
    """
    Рекурсивный post-order обход (левый-правый-корень).

    Сложность: O(n) - посещаются все узлы

    Args:
        node: Корень дерева/поддерева
        result: Список для сохранения результатов

    Returns:
        list: Узлы в порядке post-order
    """
    if result is None:
        result = []

    if node:
        postorder_recursive(node.left, result)
        postorder_recursive(node.right, result)
        result.append(node.value)

    return result


def inorder_iterative(root):
    """
    Итеративный in-order обход с использованием стека.

    Сложность: O(n) - посещаются все узлы

    Args:
        root: Корень дерева

    Returns:
        list: Узлы в порядке in-order
    """
    result = []
    stack = []
    current = root

    while current or stack:
        # Достигаем самого левого узла
        while current:
            stack.append(current)
            current = current.left

        # Извлекаем узел из стека
        current = stack.pop()
        result.append(current.value)

        # Переходим к правому поддереву
        current = current.right

    return result


def level_order_traversal(root):
    """
    Обход в ширину (BFS) по уровням.

    Сложность: O(n) - посещаются все узлы

    Args:
        root: Корень дерева

    Returns:
        list: Узлы в порядке уровней
    """
    if not root:
        return []

    result = []
    queue = [root]

    while queue:
        current = queue.pop(0)
        result.append(current.value)

        if current.left:
            queue.append(current.left)
        if current.right:
            queue.append(current.right)

    return result