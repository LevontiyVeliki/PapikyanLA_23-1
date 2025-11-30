"""
Демонстрация работы жадных алгоритмов на практических примерах.
"""

from greedy_algorithms import GreedyAlgorithms, KnapsackSolver, Interval, Item
import random


def demonstrate_interval_scheduling():
    """Демонстрация задачи о выборе заявок."""
    print("=== ДЕМОНСТРАЦИЯ: ВЫБОР ЗАЯВОК ===\n")

    # Пример с лекциями
    lectures = [
        Interval(9, 10, "Математика"),
        Interval(9, 11, "Физика"),
        Interval(10, 12, "Химия"),
        Interval(11, 13, "Биология"),
        Interval(12, 14, "Информатика"),
        Interval(13, 15, "История"),
    ]

    print("Расписание лекций:")
    for lecture in lectures:
        print(f"  {lecture.name}: {lecture.start}:00-{lecture.end}:00")

    selected = GreedyAlgorithms.interval_scheduling(lectures)

    print("\nМаксимальное количество непересекающихся лекций:")
    for lecture in selected:
        print(f"  {lecture.name}: {lecture.start}:00-{lecture.end}:00")

    print(f"\nИтого: можно посетить {len(selected)} лекций из {len(lectures)}")


def demonstrate_fractional_knapsack():
    """Демонстрация непрерывного рюкзака."""
    print("\n=== ДЕМОНСТРАЦИЯ: НЕПРЕРЫВНЫЙ РЮКЗАК ===\n")

    # Пример с продуктами
    products = [
        Item(300, 3, "Мясо"),  # удельная: 100
        Item(200, 2, "Сыр"),  # удельная: 100
        Item(150, 1, "Хлеб"),  # удельная: 150
        Item(400, 5, "Рыба"),  # удельная: 80
    ]
    backpack_capacity = 6

    print("Продукты для похода:")
    for product in products:
        unit_value = product.value / product.weight
        print(f"  {product.name}: стоимость={product.value}, вес={product.weight}, "
              f"удельная стоимость={unit_value:.1f}")

    value, selection = GreedyAlgorithms.fractional_knapsack(backpack_capacity, products)

    print(f"\nВместимость рюкзака: {backpack_capacity} кг")
    print(f"Максимальная стоимость: {value:.2f}")
    print("Выбранные продукты:")
    for product, fraction in selection:
        amount = product.weight * fraction
        cost = product.value * fraction
        print(f"  {product.name}: {amount:.1f} кг за {cost:.1f} руб (доля: {fraction:.1%})")


def demonstrate_huffman_coding():
    """Демонстрация кодирования Хаффмана."""
    print("\n=== ДЕМОНСТРАЦИЯ: КОДИРОВАНИЕ ХАФФМАНА ===\n")

    # Пример с частым текстом
    text = "aaaaaaaaaabbbbbccccccdddddeeeeeffff"

    print(f"Исходный текст: '{text}'")
    print(f"Частоты символов:")
    from collections import Counter
    freq = Counter(text)
    for char, count in sorted(freq.items()):
        print(f"  '{char}': {count} раз")

    codes, encoded, tree = GreedyAlgorithms.huffman_coding(text)

    print(f"\nКоды Хаффмана:")
    for char, code in sorted(codes.items()):
        print(f"  '{char}': {code}")

    print(f"\nЗакодированный текст: {encoded}")
    print(f"Длина исходного текста в битах (ASCII): {len(text) * 8}")
    print(f"Длина закодированного текста: {len(encoded)}")
    print(f"Экономия: {len(text) * 8 - len(encoded)} бит "
          f"({(1 - len(encoded) / (len(text) * 8)):.1%})")


def demonstrate_coin_change():
    """Демонстрация задачи о сдаче."""
    print("\n=== ДЕМОНСТРАЦИЯ: ВЫДАЧА СДАЧИ ===\n")

    # Различные системы монет
    systems = {
        "Американская": [25, 10, 5, 1],
        "Европейская": [50, 20, 10, 5, 2, 1],
        "Неканоническая": [25, 10, 1]  # Пропущена 5-центовая монета
    }

    amounts = [67, 99, 42]

    for system_name, coins in systems.items():
        print(f"\n{system_name} система: {coins}")

        for amount in amounts:
            try:
                result = GreedyAlgorithms.coin_change(amount, coins)
                total_coins = sum(result.values())
                print(f"  {amount} центов: {result} (всего {total_coins} монет)")
            except ValueError as e:
                print(f"  {amount} центов: {e}")


def demonstrate_prim_algorithm():
    """Демонстрация алгоритма Прима."""
    print("\n=== ДЕМОНСТРАЦИЯ: АЛГОРИТМ ПРИМА ===\n")

    # Пример с городами и дорогами
    cities = ['Москва', 'Санкт-Петербург', 'Казань', 'Нижний Новгород', 'Екатеринбург']
    roads = [
        ('Москва', 'Санкт-Петербург', 700),
        ('Москва', 'Казань', 800),
        ('Москва', 'Нижний Новгород', 400),
        ('Санкт-Петербург', 'Казань', 1200),
        ('Санкт-Петербург', 'Екатеринбург', 2000),
        ('Казань', 'Нижний Новгород', 400),
        ('Казань', 'Екатеринбург', 900),
        ('Нижний Новгород', 'Екатеринбург', 1200),
    ]

    print("Города и расстояния между ними:")
    for u, v, weight in roads:
        print(f"  {u} -- {v}: {weight} км")

    mst_edges = GreedyAlgorithms.prim_algorithm(cities, roads)

    print("\nМинимальная сеть дорог (алгоритм Прима):")
    total_length = 0
    for u, v, weight in mst_edges:
        print(f"  {u} -- {v}: {weight} км")
        total_length += weight

    print(f"Общая длина сети: {total_length} км")


def demonstrate_knapsack_comparison():
    """Демонстрация сравнения методов решения рюкзака."""
    print("\n=== ДЕМОНСТРАЦИЯ: СРАВНЕНИЕ РЮКЗАКОВ ===\n")

    # Пример, где жадный алгоритм не оптимален для 0-1 рюкзака
    items = [
        Item(30, 10, "Золото"),  # удельная: 3.0
        Item(20, 10, "Серебро"),  # удельная: 2.0
        Item(20, 10, "Бронза"),  # удельная: 2.0
    ]
    capacity = 20

    print("Ситуация, когда жадный алгоритм не оптимален для 0-1 рюкзака:")
    print("Предметы:")
    for item in items:
        unit_value = item.value / item.weight
        print(f"  {item.name}: стоимость={item.value}, вес={item.weight}, "
              f"удельная стоимость={unit_value:.1f}")

    KnapsackSolver.compare_knapsack_methods(capacity, items)


if __name__ == "__main__":
    random.seed(42)  # Для воспроизводимости

    demonstrate_interval_scheduling()
    demonstrate_fractional_knapsack()
    demonstrate_huffman_coding()
    demonstrate_coin_change()
    demonstrate_prim_algorithm()
    demonstrate_knapsack_comparison()