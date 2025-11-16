"""
Визуализация результатов тестирования хеш-таблиц
"""

import matplotlib.pyplot as plt
import numpy as np
from performance_analysis import main as run_performance_tests


class ResultsVisualizer:
    """Класс для визуализации результатов тестирования"""

    def __init__(self, results):
        self.results = results
        self.colors = {
            'Chaining': 'blue',
            'OpenAddr-Linear': 'green',
            'OpenAddr-Double': 'red'
        }

        plt.style.use('seaborn-v0_8')

    def plot_operation_times(self, operation: str):
        """График времени операций от коэффициента заполнения"""
        plt.figure(figsize=(12, 8))

        for impl_name, lf_data in self.results.items():
            load_factors = []
            times = []

            for lf, data in lf_data.items():
                if operation in data:
                    load_factors.append(lf)
                    times.append(data[operation])

            plt.plot(load_factors, times,
                     label=impl_name,
                     color=self.colors.get(impl_name, 'black'),
                     marker='o',
                     linewidth=2,
                     markersize=8)

        plt.xlabel('Коэффициент заполнения')
        plt.ylabel('Время выполнения (секунды)')
        plt.title(f'Зависимость времени операции {operation} от коэффициента заполнения')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(f'{operation}_performance.png', dpi=300, bbox_inches='tight')
        plt.show()

    def plot_collision_analysis(self):
        """График анализа коллизий для разных методов"""
        # Собираем данные о коллизиях
        collision_data = {}

        for impl_name, lf_data in self.results.items():
            collision_data[impl_name] = {}

            for lf, data in lf_data.items():
                if 'collisions' in data:
                    collision_data[impl_name][lf] = data['collisions']
                elif 'avg_probe_length' in data:
                    # Для открытой адресации используем среднюю длину пробирования как индикатор коллизий
                    collision_data[impl_name][lf] = data['avg_probe_length'] * 10  # Масштабируем для наглядности

        # Создаем группированный bar chart
        fig, ax = plt.subplots(figsize=(14, 8))

        load_factors = list(list(self.results.values())[0].keys())
        x = np.arange(len(load_factors))
        width = 0.25

        for i, (impl_name, lf_data) in enumerate(collision_data.items()):
            values = [lf_data[lf] for lf in load_factors]
            ax.bar(x + i * width - width, values, width,
                   label=impl_name,
                   color=self.colors.get(impl_name, 'gray'))

        ax.set_xlabel('Коэффициент заполнения')
        ax.set_ylabel('Коллизии (метрика)')
        ax.set_title('Сравнение количества коллизий для разных методов')
        ax.set_xticks(x)
        ax.set_xticklabels([f'{lf}' for lf in load_factors])
        ax.legend()
        ax.grid(True, alpha=0.3, axis='y')

        plt.tight_layout()
        plt.savefig('collision_comparison.png', dpi=300, bbox_inches='tight')
        plt.show()

    def plot_memory_usage(self):
        """График использования памяти"""
        plt.figure(figsize=(12, 8))

        for impl_name, lf_data in self.results.items():
            load_factors = []
            memory_usage = []

            for lf, data in lf_data.items():
                load_factors.append(lf)
                # Оцениваем использование памяти через размер таблицы
                if 'size' in data:
                    memory_usage.append(data['size'])

            plt.plot(load_factors, memory_usage,
                     label=impl_name,
                     color=self.colors.get(impl_name, 'black'),
                     marker='s',
                     linewidth=2,
                     markersize=8)

        plt.xlabel('Коэффициент заполнения')
        plt.ylabel('Размер таблицы')
        plt.title('Использование памяти разными реализациями')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig('memory_usage.png', dpi=300, bbox_inches='tight')
        plt.show()

    def create_comprehensive_report(self):
        """Создание комплексного отчета"""
        print("\n" + "=" * 100)
        print("КОМПЛЕКСНЫЙ ОТЧЕТ ПО ПРОИЗВОДИТЕЛЬНОСТИ ХЕШ-ТАБЛИЦ")
        print("=" * 100)

        # Сводная таблица для коэффициента заполнения 0.75
        target_lf = 0.75

        headers = ["Implementation", "Insert Time", "Search Success", "Search Fail", "Delete Time",
                   "Collisions", "Memory Size"]
        table_data = [headers]

        for impl_name, lf_data in self.results.items():
            if target_lf in lf_data:
                data = lf_data[target_lf]
                row = [
                    impl_name,
                    f"{data.get('insert', 0):.4f}s",
                    f"{data.get('search_success', 0):.4f}s",
                    f"{data.get('search_fail', 0):.4f}s",
                    f"{data.get('delete', 0):.4f}s",
                    f"{data.get('collisions', data.get('avg_probe_length', 0)):.1f}",
                    f"{data.get('size', 0)}"
                ]
                table_data.append(row)

        # Вывод таблицы
        col_widths = [max(len(str(item)) for item in col) for col in zip(*table_data)]

        print(f"\nСравнение при коэффициенте заполнения {target_lf}:")
        print("-" * (sum(col_widths) + 3 * len(col_widths) + 1))

        for row in table_data:
            print("| " + " | ".join(f"{item:<{col_widths[i]}}" for i, item in enumerate(row)) + " |")

        print("-" * (sum(col_widths) + 3 * len(col_widths) + 1))

        # Ключевые выводы
        print("\nКЛЮЧЕВЫЕ ВЫВОДЫ:")
        print("1. Метод цепочек стабилен при высоких коэффициентах заполнения")
        print("2. Открытая адресация быстрее при низких коэффициентах заполнения")
        print("3. Двойное хеширование эффективнее линейного пробирования")
        print("4. Оптимальный коэффициент заполнения: 0.5-0.75")
        print("5. Выбор реализации зависит от ожидаемого коэффициента заполнения и требований к памяти")


def main():
    """Основная функция визуализации"""
    print("Запуск тестов производительности для визуализации...")
    results = run_performance_tests()

    # Визуализация
    visualizer = ResultsVisualizer(results)

    # Графики для разных операций
    for operation in ['insert', 'search_success', 'search_fail', 'delete']:
        visualizer.plot_operation_times(operation)

    # Дополнительные графики
    visualizer.plot_collision_analysis()
    visualizer.plot_memory_usage()

    # Комплексный отчет
    visualizer.create_comprehensive_report()


if __name__ == "__main__":
    main()