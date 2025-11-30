"""
Анализ производительности алгоритмов на строках.
"""

import time
import random
import matplotlib.pyplot as plt
from prefix_function import PrefixFunction, NaiveStringSearch
from z_function import ZFunction
from string_matching import BoyerMoore, RabinKarp
import sys
import string


class StringAlgorithmsAnalysis:
    """
    Класс для анализа производительности алгоритмов на строках.
    """

    @staticmethod
    def analyze_algorithms_performance():
        """
        Анализ производительности различных алгоритмов поиска подстрок.
        """
        print("=== АНАЛИЗ ПРОИЗВОДИТЕЛЬНОСТИ АЛГОРИТМОВ ПОИСКА ПОДСТРОК ===\n")

        # Характеристики тестовой машины
        import platform
        print("Характеристики тестовой машины:")
        print(f"Процессор: {platform.processor()}")
        print(f"Память: {sys.platform == 'win32' and '15 GB' or 'N/A'}")
        print(f"ОС: {platform.system()} {platform.release()}")
        print(f"Python: {sys.version}")
        print()

        # Параметры тестирования
        text_sizes = [1000, 5000, 10000, 50000]
        pattern_sizes = [10, 50, 100]

        algorithms = {
            "Naive": NaiveStringSearch.naive_search,
            "KMP": PrefixFunction.kmp_search,
            "Z-Function": ZFunction.z_search,
            "Boyer-Moore": BoyerMoore.boyer_moore_search,
            "Rabin-Karp": RabinKarp.rabin_karp_search
        }

        results = {algo: [] for algo in algorithms}

        print("ТЕСТИРОВАНИЕ НА СЛУЧАЙНЫХ СТРОКАХ:")
        print("Размер текста | Длина паттерна | " + " | ".join(f"{algo:>12}" for algo in algorithms))
        print("-" * 120)

        for text_size in text_sizes:
            for pattern_size in pattern_sizes:
                if pattern_size >= text_size:
                    continue

                # Генерируем случайные строки
                text = ''.join(random.choices(string.ascii_lowercase, k=text_size))
                pattern = ''.join(random.choices(string.ascii_lowercase, k=pattern_size))

                times_row = [f"{text_size:12} | {pattern_size:14}"]

                for algo_name, algo_func in algorithms.items():
                    try:
                        # Измеряем время выполнения
                        start_time = time.perf_counter()
                        result = algo_func(text, pattern)
                        end_time = time.perf_counter()

                        execution_time = (end_time - start_time) * 1000  # мс
                        results[algo_name].append(execution_time)
                        times_row.append(f"{execution_time:12.3f}")
                    except Exception as e:
                        results[algo_name].append(float('inf'))
                        times_row.append(f"{'ERROR':>12}")

                print(" | ".join(times_row))

        # Построение графиков
        plt.figure(figsize=(15, 10))

        # График 1: Зависимость от размера текста (фиксированный паттерн)
        plt.subplot(2, 2, 1)
        pattern_size_fixed = 50
        text_size_indexes = [i for i, ps in enumerate(pattern_sizes) if ps == pattern_size_fixed]

        for algo_name in algorithms:
            algo_times = [results[algo_name][i] for i in range(len(text_sizes) * len(pattern_sizes))
                          if i % len(pattern_sizes) == text_size_indexes[0] if text_size_indexes]
            if algo_times:
                plt.plot(text_sizes[:len(algo_times)], algo_times, 'o-', label=algo_name, linewidth=2)

        plt.xlabel('Длина текста')
        plt.ylabel('Время (мс)')
        plt.title(f'Зависимость времени от длины текста\n(длина паттерна = {pattern_size_fixed})')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.yscale('log')  # Логарифмическая шкала для наглядности

        # График 2: Зависимость от длины паттерна (фиксированный текст)
        plt.subplot(2, 2, 2)
        text_size_fixed = 5000
        text_size_idx = text_sizes.index(text_size_fixed) if text_size_fixed in text_sizes else 0

        for algo_name in algorithms:
            start_idx = text_size_idx * len(pattern_sizes)
            end_idx = start_idx + len(pattern_sizes)
            algo_times = results[algo_name][start_idx:end_idx]
            if algo_times:
                plt.plot(pattern_sizes, algo_times, 'o-', label=algo_name, linewidth=2)

        plt.xlabel('Длина паттерна')
        plt.ylabel('Время (мс)')
        plt.title(f'Зависимость времени от длины паттерна\n(длина текста = {text_size_fixed})')
        plt.legend()
        plt.grid(True, alpha=0.3)

        # График 3: Сравнение алгоритмов (среднее время)
        plt.subplot(2, 2, 3)
        avg_times = []
        for algo_name in algorithms:
            valid_times = [t for t in results[algo_name] if t != float('inf')]
            avg_times.append(sum(valid_times) / len(valid_times) if valid_times else 0)

        bars = plt.bar(algorithms.keys(), avg_times, color=['red', 'blue', 'green', 'orange', 'purple'])
        plt.xlabel('Алгоритм')
        plt.ylabel('Среднее время (мс)')
        plt.title('Средняя производительность алгоритмов')
        plt.xticks(rotation=45)
        plt.grid(True, alpha=0.3, axis='y')

        # Добавляем значения на столбцы
        for bar, value in zip(bars, avg_times):
            plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.01,
                     f'{value:.2f} мс', ha='center', va='bottom', fontsize=9)

        # График 4: Теоретическая сложность
        plt.subplot(2, 2, 4)
        complexities = {
            'Naive': 'O(n*m)',
            'KMP': 'O(n+m)',
            'Z-Function': 'O(n+m)',
            'Boyer-Moore': 'O(n/m) лучш., O(n*m) худш.',
            'Rabin-Karp': 'O(n+m) средн.'
        }

        # Создаем таблицу
        plt.axis('tight')
        plt.axis('off')
        table_data = [[complexities[algo]] for algo in algorithms]
        table = plt.table(cellText=table_data,
                          rowLabels=list(algorithms.keys()),
                          colLabels=['Сложность'],
                          cellLoc='center',
                          loc='center')
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1, 2)
        plt.title('Теоретическая временная сложность')

        plt.tight_layout()
        plt.savefig('string_algorithms_performance.png', dpi=300, bbox_inches='tight')
        plt.show()

        return results

    @staticmethod
    def analyze_worst_case_performance():
        """
        Анализ производительности в худших случаях.
        """
        print("\n=== АНАЛИЗ ПРОИЗВОДИТЕЛЬНОСТИ В ХУДШИХ СЛУЧАЯХ ===\n")

        # Худший случай для наивного алгоритма
        print("ХУДШИЙ СЛУЧАЙ ДЛЯ НАИВНОГО АЛГОРИТМА:")
        print("Текст: 'a'*1000, Паттерн: 'a'*500 + 'b'")

        text = "a" * 1000
        pattern = "a" * 500 + "b"

        algorithms = {
            "Naive": NaiveStringSearch.naive_search,
            "KMP": PrefixFunction.kmp_search,
            "Z-Function": ZFunction.z_search,
        }

        for algo_name, algo_func in algorithms.items():
            start_time = time.perf_counter()
            result = algo_func(text, pattern)
            end_time = time.perf_counter()
            execution_time = (end_time - start_time) * 1000
            print(f"  {algo_name}: {execution_time:.3f} мс, найдено вхождений: {len(result)}")

        # Худший случай для Бойера-Мура
        print("\nХУДШИЙ СЛУЧАЙ ДЛЯ БОЙЕРА-МУРА:")
        print("Текст: 'aaa...aaa', Паттерн: 'baa...aaa'")

        text = "a" * 1000
        pattern = "b" + "a" * 499

        start_time = time.perf_counter()
        result = BoyerMoore.boyer_moore_search(text, pattern)
        end_time = time.perf_counter()
        execution_time = (end_time - start_time) * 1000
        print(f"  Boyer-Moore: {execution_time:.3f} мс, найдено вхождений: {len(result)}")

        # Лучший случай для Бойера-Мура
        print("\nЛУЧШИЙ СЛУЧАЙ ДЛЯ БОЙЕРА-МУРА:")
        print("Текст: 'x'*1000, Паттерн: 'abcde'")

        text = "x" * 1000
        pattern = "abcde"

        start_time = time.perf_counter()
        result = BoyerMoore.boyer_moore_search(text, pattern)
        end_time = time.perf_counter()
        execution_time = (end_time - start_time) * 1000
        print(f"  Boyer-Moore: {execution_time:.3f} мс, найдено вхождений: {len(result)}")

    @staticmethod
    def analyze_real_world_patterns():
        """
        Анализ производительности на реальных паттернах.
        """
        print("\n=== АНАЛИЗ НА РЕАЛЬНЫХ ПАТТЕРНАХ ===\n")

        # Текст для поиска (отрывок из литературного произведения)
        text = """
        В тот год осенняя погода
        Стояла долго на дворе,
        Зимы ждала, ждала природа.
        Снег выпал только в январе
        На третье в ночь. Проснувшись рано,
        В окно увидела Татьяна
        Поутру побелевший двор,
        Куртины, кровли и забор,
        На стеклах легкие узоры,
        Деревья в зимнем серебре,
        Сорок веселых на дворе
        И мягко устланные горы
        Зимы блистательным ковром.
        Все ярко, все бело кругом.
        """

        # Удаляем переносы строк и лишние пробелы
        text = ' '.join(text.split())

        patterns = [
            "погода",  # Короткое слово
            "Татьяна",  # Имя
            "зим",  # Часть слова (проверка префиксов)
            "все",  # Повторяющееся слово
            "несуществующееслово"  # Отсутствующий паттерн
        ]

        algorithms = {
            "Naive": NaiveStringSearch.naive_search,
            "KMP": PrefixFunction.kmp_search,
            "Z-Function": ZFunction.z_search,
            "Boyer-Moore": BoyerMoore.boyer_moore_search,
            "Rabin-Karp": RabinKarp.rabin_karp_search
        }

        print("РЕЗУЛЬТАТЫ ПОИСКА В ТЕКСТЕ:")
        print("Паттерн | " + " | ".join(f"{algo:>12}" for algo in algorithms))
        print("-" * 90)

        for pattern in patterns:
            results_row = [f"{pattern:16}"]

            for algo_name, algo_func in algorithms.items():
                start_time = time.perf_counter()
                result = algo_func(text, pattern)
                end_time = time.perf_counter()
                execution_time = (end_time - start_time) * 1000000  # микросекунды

                results_row.append(f"{execution_time:12.3f}")

            print(" | ".join(results_row))

    @staticmethod
    def practical_applications_demo():
        """
        Демонстрация практических применений алгоритмов на строках.
        """
        print("\n=== ПРАКТИЧЕСКИЕ ПРИМЕНЕНИЯ ===\n")

        # 1. Поиск периода строки
        print("1. ПОИСК ПЕРИОДА СТРОКИ")
        test_strings = ["abcabcabc", "ababab", "aaaa", "abcde"]

        for s in test_strings:
            period = PrefixFunction.find_period(s)
            if period > 0:
                print(f"  '{s}' - периодическая с периодом {period}")
            else:
                print(f"  '{s}' - непериодическая")

        # 2. Проверка циклического сдвига
        print("\n2. ПРОВЕРКА ЦИКЛИЧЕСКОГО СДВИГА")
        pairs = [("abcde", "cdeab"), ("abcde", "edcba"), ("abc", "bca")]

        for s1, s2 in pairs:
            is_rotation = PrefixFunction.is_rotation(s1, s2)
            print(f"  '{s2}' {'является' if is_rotation else 'не является'} циклическим сдвигом '{s1}'")

        # 3. Подсчет различных подстрок
        print("\n3. ПОДСЧЕТ РАЗЛИЧНЫХ ПОДСТРОК")
        test_strings = ["aaa", "abc", "abab"]

        for s in test_strings:
            count = ZFunction.find_distinct_substrings_count(s)
            print(f"  '{s}' содержит {count} различных подстрок")

        # 4. Поиск палиндромных подстрок
        print("\n4. ПОИСК ПАЛИНДРОМНЫХ ПОДСТРОК")
        test_string = "ababa"
        palindromes = ZFunction.find_palindromic_substrings(test_string)
        print(f"  В '{test_string}' найдены палиндромы: {palindromes}")

        # 5. Поиск нескольких паттернов одновременно
        print("\n5. ПОИСК НЕСКОЛЬКИХ ПАТТЕРНОВ ОДНОВРЕМЕННО")
        text = "быстрый рыжий лис прыгнул через ленивую собаку"
        patterns = ["лис", "собака", "рыжий", "волк"]

        from string_matching import RabinKarp
        results = RabinKarp.rabin_karp_multiple_patterns(text, patterns)

        for pattern, positions in results.items():
            if positions:
                print(f"  '{pattern}' найден в позициях: {positions}")
            else:
                print(f"  '{pattern}' не найден")


def run_comprehensive_analysis():
    """
    Запуск комплексного анализа алгоритмов на строках.
    """
    print("=== КОМПЛЕКСНЫЙ АНАЛИЗ АЛГОРИТМОВ НА СТРОКАХ ===\n")

    # Анализ производительности на случайных строках
    print("1. Анализ производительности на случайных строках...")
    performance_results = StringAlgorithmsAnalysis.analyze_algorithms_performance()

    # Анализ худших случаев
    print("\n2. Анализ производительности в худших случаях...")
    StringAlgorithmsAnalysis.analyze_worst_case_performance()

    # Анализ на реальных паттернах
    print("\n3. Анализ на реальных паттернах...")
    StringAlgorithmsAnalysis.analyze_real_world_patterns()

    # Практические применения
    print("\n4. Демонстрация практических применений...")
    StringAlgorithmsAnalysis.practical_applications_demo()

    print("\n" + "=" * 70)
    print("Анализ завершен успешно! Графики сохранены в файлы PNG.")
    print("=" * 70)

    return performance_results


if __name__ == "__main__":
    run_comprehensive_analysis()