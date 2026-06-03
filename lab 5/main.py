"""
Сравнение рекурсивного и итеративного факториала с мемоизацией и без неё.

Функции:
- fact_recursive: рекурсивный факториал
- fact_recursive_memo: рекурсивный факториал с мемоизацией (lru_cache)
- fact_iterative: итеративный факториал
- fact_iterative_memo: итеративный факториал с мемоизацией (lru_cache)

Сравнение выполняется по двум направлениям:
1. Рекурсивный vs итеративный (оба с мемоизацией и оба без)
2. С мемоизацией vs без мемоизации (для каждого типа отдельно)

Визуализация: matplotlib
Бенчмарк: timeit
"""

import timeit
import matplotlib.pyplot as plt
from functools import lru_cache


# Реализация функций 

def fact_recursive(n: int) -> int:
    """
    Рекурсивный факториал без мемоизации.

    Сложность: O(n) по времени и O(n) по памяти (стек вызовов).
    """
    if n == 0:
        return 1
    return n * fact_recursive(n - 1)


@lru_cache(maxsize=None)
def fact_recursive_memo(n: int) -> int:
    """
    Рекурсивный факториал с мемоизацией (lru_cache).

    Сложность: O(n) по времени (первые вызовы), затем O(1).
    Память: кэширует все вычисленные значения.
    """
    if n == 0:
        return 1
    return n * fact_recursive_memo(n - 1)


def fact_iterative(n: int) -> int:
    """
    Итеративный факториал без мемоизации.

    Сложность: O(n) по времени, O(1) по памяти.
    """
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


@lru_cache(maxsize=None)
def fact_iterative_memo(n: int) -> int:
    """
    Итеративный факториал с мемоизацией (обёртка над итеративной логикой).

    При первом вызове считается итеративно, результат кэшируется.
    """
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


# Бенчмарк

def benchmark(func, n: int, number: int = 10000, repeat: int = 5) -> float:
    """
    Замеряет минимальное время выполнения func(n).

    Параметры:
    - func: тестируемая функция
    - n: аргумент функции
    - number: количество вызовов за один замер
    - repeat: количество повторных замеров

    Возвращает:
    - минимальное время в секундах (на один вызов)
    """
    # Для мемоизированных функций очищаем кэш перед каждым вызовом,
    # чтобы измерять время "холодного" запуска.
    if hasattr(func, "cache_clear"):
        func.cache_clear()

    stmt = lambda: func(n)
    times = timeit.repeat(stmt, number=number, repeat=repeat)
    return min(times) / number  # время одного вызова


# Сравнение 1: Рекурсивный vs Итеративный

def compare_recursive_vs_iterative(n_values, number=5000, repeat=5):
    """Сравнивает рекурсивный и итеративный подходы (оба без мемоизации)."""
    rec_times = []
    iter_times = []

    for n in n_values:
        rec_times.append(benchmark(fact_recursive, n, number, repeat))
        iter_times.append(benchmark(fact_iterative, n, number, repeat))

    return rec_times, iter_times


def compare_recursive_vs_iterative_memo(n_values, number=5000, repeat=5):
    """Сравнивает рекурсивный и итеративный подходы (оба с мемоизацией)."""
    rec_memo_times = []
    iter_memo_times = []

    for n in n_values:
        rec_memo_times.append(benchmark(fact_recursive_memo, n, number, repeat))
        iter_memo_times.append(benchmark(fact_iterative_memo, n, number, repeat))

    return rec_memo_times, iter_memo_times


# Сравнение 2: С мемоизацией vs Без мемоизации

def compare_memo_vs_non_memo_recursive(n_values, number=5000, repeat=5):
    """Сравнивает рекурсивный с мемоизацией и без (для каждого n замер "холодного" запуска)."""
    non_memo_times = []
    memo_times = []

    for n in n_values:
        non_memo_times.append(benchmark(fact_recursive, n, number, repeat))
        memo_times.append(benchmark(fact_recursive_memo, n, number, repeat))

    return non_memo_times, memo_times


def compare_memo_vs_non_memo_iterative(n_values, number=5000, repeat=5):
    """Сравнивает итеративный с мемоизацией и без."""
    non_memo_times = []
    memo_times = []

    for n in n_values:
        non_memo_times.append(benchmark(fact_iterative, n, number, repeat))
        memo_times.append(benchmark(fact_iterative_memo, n, number, repeat))

    return non_memo_times, memo_times


# Визуализация

def plot_results(n_values, rec_times, iter_times, title, filename):
    """Общая функция для построения графиков."""
    plt.figure(figsize=(10, 6))
    plt.plot(n_values, rec_times, marker='o', label='Рекурсивный', linewidth=2)
    plt.plot(n_values, iter_times, marker='s', label='Итеративный', linewidth=2)
    plt.xlabel('n (входное число)', fontsize=12)
    plt.ylabel('Время выполнения (секунды)', fontsize=12)
    plt.title(title, fontsize=14)
    plt.legend(fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(filename, dpi=150)
    plt.show()


def plot_comparison_two_panels(n_values, rec_non_memo, rec_memo, iter_non_memo, iter_memo):
    """Два графика: для рекурсивного и итеративного подходов (мемоизация vs без)."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    # График для рекурсивного
    ax1.plot(n_values, rec_non_memo, marker='o', label='Без мемоизации', linewidth=2)
    ax1.plot(n_values, rec_memo, marker='s', label='С мемоизацией', linewidth=2)
    ax1.set_xlabel('n')
    ax1.set_ylabel('Время (сек)')
    ax1.set_title('Рекурсивный факториал')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # График для итеративного
    ax2.plot(n_values, iter_non_memo, marker='o', label='Без мемоизации', linewidth=2)
    ax2.plot(n_values, iter_memo, marker='s', label='С мемоизацией', linewidth=2)
    ax2.set_xlabel('n')
    ax2.set_ylabel('Время (сек)')
    ax2.set_title('Итеративный факториал')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('comparison_memo_vs_non_memo.png', dpi=150)
    plt.show()


# Основная функция

def main():
    # Фиксированный набор чисел для тестирования
    n_values = list(range(10, 201, 10))  # от 10 до 200 с шагом 10
    # Для большей стабильности уменьшаем количество повторений для больших n
    number = 3000  # число вызовов за замер
    repeat = 5     # число замеров

    print("Запуск бенчмарков...")
    print(f"Тестируемые значения n: {n_values}")
    print(f"Параметры: number={number}, repeat={repeat}\n")

    # Сравнение 1: Рекурсивный vs Итеративный (без мемоизации)
    print("1. Сравнение рекурсивного и итеративного подходов (без мемоизации)...")
    rec_times, iter_times = compare_recursive_vs_iterative(n_values, number, repeat)
    plot_results(
        n_values, rec_times, iter_times,
        "Сравнение рекурсивного и итеративного факториала\n(без мемоизации)",
        "comparison_rec_vs_iter.png"
    )

    # Сравнение 1b: Рекурсивный vs Итеративный (с мемоизацией)
    print("2. Сравнение рекурсивного и итеративного подходов (с мемоизацией)...")
    rec_memo_times, iter_memo_times = compare_recursive_vs_iterative_memo(n_values, number, repeat)
    plot_results(
        n_values, rec_memo_times, iter_memo_times,
        "Сравнение рекурсивного и итеративного факториала\n(с мемоизацией, первый вызов)",
        "comparison_rec_vs_iter_memo.png"
    )

    # Сравнение 2: С мемоизацией vs Без (для каждого типа отдельно)
    print("3. Сравнение с мемоизацией и без для рекурсивного подхода...")
    rec_non_memo, rec_memo_compare = compare_memo_vs_non_memo_recursive(n_values, number, repeat)

    print("4. Сравнение с мемоизацией и без для итеративного подхода...")
    iter_non_memo, iter_memo_compare = compare_memo_vs_non_memo_iterative(n_values, number, repeat)

    plot_comparison_two_panels(n_values, rec_non_memo, rec_memo_compare, iter_non_memo, iter_memo_compare)

    # Вывод статистики
    print("\n" + "=" * 60)
    print("РЕЗУЛЬТАТЫ (среднее время выполнения на один вызов в секундах):")
    print("=" * 60)

    print(f"\nДля n = {n_values[-1]} (максимальное значение):")
    print(f"  Рекурсивный (без мемоизации):   {rec_times[-1]:.2e} сек")
    print(f"  Итеративный (без мемоизации):   {iter_times[-1]:.2e} сек")
    print(f"  Рекурсивный (с мемоизацией):    {rec_memo_times[-1]:.2e} сек")
    print(f"  Итеративный (с мемоизацией):    {iter_memo_times[-1]:.2e} сек")

    # Ускорение
    speedup = rec_times[-1] / iter_times[-1]
    print(f"\nУскорение итеративного подхода над рекурсивным (без мемоизации): {speedup:.1f}x")

    memo_speedup_rec = rec_times[-1] / rec_memo_times[-1] if rec_memo_times[-1] > 0 else 0
    print(f"Ускорение от мемоизации для рекурсивного подхода: {memo_speedup_rec:.1f}x")


if __name__ == "__main__":
    main()
