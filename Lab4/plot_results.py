"""
Визуализация результатов тестирования производительности
"""

import matplotlib.pyplot as plt
import numpy as np
from performance_test import main as run_performance_tests


class ResultsVisualizer:
    """Класс для визуализации результатов тестирования"""

    def __init__(self, results):
        self.results = results
        self.colors = {
            'bubble_sort': 'red',
            'selection_sort': 'blue',
            'insertion_sort': 'green',
            'merge_sort': 'orange',
            'quick_sort': 'purple'
        }

        plt.style.use('seaborn-v0_8')

    def plot_time_vs_size(self, data_type: str = 'random'):
        """График времени выполнения от размера массива"""
        plt.figure(figsize=(12, 8))

        if data_type not in self.results:
            print(f"Тип данных '{data_type}' не найден в результатах")
            return

        for algo_name, times in self.results[data_type].items():
            sizes = [size for size, _ in times]
            time_vals = [time_val for _, time_val in times]

            plt.plot(sizes, time_vals,
                    label=algo_name,
                    color=self.colors.get(algo_name, 'black'),
                    marker='o',
                    linewidth=2,
                    markersize=6)

        plt.xlabel('Размер массива')
        plt.ylabel('Время выполнения (секунды)')
        plt.title(f'Зависимость времени сортировки от размера массива\n(Тип данных: {data_type})')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.yscale('log')  # Логарифмическая шкала для лучшего отображения
        plt.xscale('log')
        plt.tight_layout()
        plt.savefig(f'time_vs_size_{data_type}.png', dpi=300, bbox_inches='tight')
        plt.show()

    def plot_comparison_by_data_type(self, size: int = 5000):
        """Сравнение алгоритмов по типам данных для фиксированного размера"""
        plt.figure(figsize=(14, 8))

        # Собираем данные для выбранного размера
        comparison_data = {}

        for data_type, algorithms in self.results.items():
            comparison_data[data_type] = {}
            for algo_name, times in algorithms.items():
                # Ищем время для нужного размера
                for arr_size, time_val in times:
                    if arr_size == size:
                        comparison_data[data_type][algo_name] = time_val
                        break

        # Подготовка данных для группированного bar chart
        algorithms = list(SORTING_ALGORITHMS.keys())
        data_types = list(comparison_data.keys())

        x = np.arange(len(data_types))
        width = 0.15

        fig, ax = plt.subplots(figsize=(14, 8))

        for i, algo_name in enumerate(algorithms):
            times = [comparison_data[dt].get(algo_name, 0) for dt in data_types]
            ax.bar(x + i * width - width * 2, times, width,
                   label=algo_name,
                   color=self.colors.get(algo_name, 'gray'))

        ax.set_xlabel('Тип данных')
        ax.set_ylabel('Время выполнения (секунды)')
        ax.set_title(f'Сравнение алгоритмов сортировки по типам данных\n(Размер массива: {size})')
        ax.set_xticks(x)
        ax.set_xticklabels([dt.upper() for dt in data_types])
        ax.legend()
        ax.grid(True, alpha=0.3, axis='y')

        plt.tight_layout()
        plt.savefig(f'comparison_data_types_size_{size}.png', dpi=300, bbox_inches='tight')
        plt.show()

    def create_performance_table(self):
        """Создание сводной таблицы производительности"""
        print("\n" + "="*100)
        print("СВОДНАЯ ТАБЛИЦА ПРОИЗВОДИТЕЛЬНОСТИ")
        print("="*100)

        # Для размера 5000 собираем все данные
        target_size = 5000
        table_data = []

        headers = ["Algorithm"] + list(self.results.keys())
        table_data.append(headers)

        for algo_name in SORTING_ALGORITHMS.keys():
            row = [algo_name]
            for data_type in self.results.keys():
                time_val = None
                for size, t in self.results[data_type][algo_name]:
                    if size == target_size:
                        time_val = t
                        break
                row.append(f"{time_val:.4f}s" if time_val is not None else "N/A")
            table_data.append(row)

        # Вывод таблицы
        col_widths = [max(len(str(item)) for item in col) for col in zip(*table_data)]

        for row in table_data:
            print("| " + " | ".join(f"{item:<{col_widths[i]}}" for i, item in enumerate(row)) + " |")

        return table_data


def main():
    """Основная функция визуализации"""
    # Запускаем тесты если результаты не переданы
    print("Запуск тестов производительности...")
    results = run_performance_tests()

    # Визуализация
    visualizer = ResultsVisualizer(results)

    # Графики для разных типов данных
    for data_type in ['random', 'sorted', 'reversed', 'almost_sorted']:
        visualizer.plot_time_vs_size(data_type)

    # Сравнение по типам данных
    visualizer.plot_comparison_by_data_type(5000)

    # Сводная таблица
    visualizer.create_performance_table()


if __name__ == "__main__":
    main()