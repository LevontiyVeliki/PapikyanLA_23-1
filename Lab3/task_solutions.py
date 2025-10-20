from collections import deque
from linked_list import LinkedList


def check_brackets_balance(expression):
    """
    Проверка сбалансированности скобок с использованием стека
    Сложность: O(n)
    """
    stack = []
    brackets = {')': '(', ']': '[', '}': '{'}

    for char in expression:
        if char in '([{':
            stack.append(char)  # O(1)
        elif char in ')]}':
            if not stack or stack[-1] != brackets[char]:
                return False
            stack.pop()  # O(1)

    return len(stack) == 0


def simulate_print_queue(tasks, time_slice=1):
    """
    Симуляция обработки задач в очереди печати
    Сложность: O(n) где n - количество задач
    """
    queue = deque(tasks)
    time_elapsed = 0
    processing_order = []

    while queue:  # O(n) операций
        current_task = queue.popleft()  # O(1)
        processing_order.append(current_task)
        time_elapsed += time_slice

        # Имитация обработки задачи
        print(f"Время {time_elapsed}: обработана задача '{current_task}'")

    return processing_order, time_elapsed


def is_palindrome_deque(sequence):
    """
    Проверка палиндрома с использованием дека
    Сложность: O(n)
    """
    dq = deque(sequence)

    while len(dq) > 1:  # O(n/2) = O(n)
        if dq.popleft() != dq.pop():  # O(1) + O(1)
            return False
    return True


def is_palindrome_linked_list(sequence):
    """
    Проверка палиндрома с использованием связного списка
    Сложность: O(n)
    """
    ll = LinkedList()

    # Заполняем список
    for char in sequence:
        ll.insert_at_end(char)

    # Для проверки палиндрома в односвязном списке потребуется O(n²)
    # Поэтому используем дополнительную структуру
    stack = []
    current = ll.head

    # Заполняем стек
    while current:
        stack.append(current.data)
        current = current.next

    # Проверяем
    current = ll.head
    while current and stack:
        if current.data != stack.pop():
            return False
        current = current.next

    return True


# Демонстрация работы
if __name__ == "__main__":
    print("=== ПРОВЕРКА СБАЛАНСИРОВАННОСТИ СКОБОК ===")
    test_cases = ["()[]{}", "([{}])", "([)]", "((()))", "()[]"]
    for test in test_cases:
        result = check_brackets_balance(test)
    print(f"'{test}': {'Сбалансированы' if result else 'Не сбалансированы'}")

    print("\n=== СИМУЛЯЦИЯ ОЧЕРЕДИ ПЕЧАТИ ===")
    tasks = ["doc1.pdf", "doc2.docx", "image.png", "report.pdf"]
    order, total_time = simulate_print_queue(tasks)
    print(f"Всего задач: {len(tasks)}, Общее время: {total_time}")

    print("\n=== ПРОВЕРКА ПАЛИНДРОМОВ ===")
    test_sequences = ["радар", "level", "hello", "а роза упала на лапу азора"]
    for seq in test_sequences:
    # Убираем пробелы для проверки
        clean_seq = seq.replace(" ", "")
    result_deque = is_palindrome_deque(clean_seq)
    result_ll = is_palindrome_linked_list(clean_seq)
    print(f"'{seq}': deque={result_deque}, LinkedList={result_ll}")