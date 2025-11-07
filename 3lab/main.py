def generate_permutations(elements):
    """
    Рекурсивная генерация всех перестановок элементов
    """
    steps = []  # Шаги вычислений
    partial_results = []  # Собранные частичные результаты
    final_results = []  # Итоговые комбинации

    def recursive_permutation(current, remaining):
        # Фиксируем шаг вычисления
        step = f"текущие={current}, оставшиеся={remaining}"
        steps.append(step)

        # Фиксируем частичный результат (текущее состояние)
        partial_results.append({
            'текущие': current.copy(),
            'оставшиеся': remaining.copy(),
            'глубина': len(current)
        })

        if len(remaining) == 0:
            # Фиксируем итоговый результат
            result = current.copy()
            final_results.append(result)
            return

        for i in range(len(remaining)):
            recursive_permutation(
                current + [remaining[i]],
                remaining[:i] + remaining[i + 1:]
            )

    recursive_permutation([], elements)

    # Возвращаем все коллекции для анализа
    return {
        'шаги': steps,
        'частичные_результаты': partial_results,
        'итоговые_результаты': final_results
    }


def generate_combinations(elements, k):
    """
    Рекурсивная генерация всех комбинаций из n элементов по k
    """
    steps = []  # Шаги вычислений
    partial_results = []  # Собранные частичные результаты
    final_results = []  # Итоговые комбинации

    def recursive_combination(start, current_comb):
        # Фиксируем шаг вычисления
        step = f"старт={start}, текущие={current_comb}"
        steps.append(step)

        # Фиксируем частичный результат
        partial_results.append({
            'текущие': current_comb.copy(),
            'стартовый_индекс': start,
            'глубина': len(current_comb)
        })

        if len(current_comb) == k:
            # Фиксируем итоговый результат
            result = current_comb.copy()
            final_results.append(result)
            return

        for i in range(start, len(elements)):
            recursive_combination(i + 1, current_comb + [elements[i]])

    recursive_combination(0, [])

    # Возвращаем все коллекции для анализа
    return {
        'шаги': steps,
        'частичные_результаты': partial_results,
        'итоговые_результаты': final_results
    }


if __name__ == "__main__":
    print("ГЕНЕРАЦИЯ ПЕРЕСТАНОВОК И КОМБИНАЦИЙ")
    print("=" * 40)

    # Ввод данных
    print("\nВведите элементы (через пробел):")
    user_input = input().split()
    elements = []
    for item in user_input:
        try:
            elements.append(int(item))
        except ValueError:
            elements.append(item)

    print("\nВыберите тип генерации:")
    print("1 - Перестановки")
    print("2 - Комбинации")
    choice = input("Введите 1 или 2: ")

    if choice == "1":
        # Генерация и анализ перестановок
        print("\n" + "=" * 50)
        print("АНАЛИЗ ПЕРЕСТАНОВОК:")
        data = generate_permutations(elements)

        print(f"Всего шагов: {len(data['шаги'])}")
        print(f"Частичных результатов: {len(data['частичные_результаты'])}")
        print(f"Итоговых перестановок: {len(data['итоговые_результаты'])}")

        print("\nПервые 10 шагов вычислений:")
        for i, step in enumerate(data['шаги'][:10], 1):
            print(f"  Шаг {i}: {step}")

        if len(data['шаги']) > 10:
            print(f"  ... и еще {len(data['шаги']) - 10} шагов")

        print("\nПервые 10 частичных результатов:")
        for i, partial in enumerate(data['частичные_результаты'][:10], 1):
            print(f"  {i}. текущие={partial['текущие']}, глубина={partial['глубина']}")

        if len(data['частичные_результаты']) > 10:
            print(f"  ... и еще {len(data['частичные_результаты']) - 10} результатов")

        print(f"\nВсе перестановки: {data['итоговые_результаты']}")

    elif choice == "2":
        print("\nВведите размер комбинаций k:")
        k = int(input())

        # Генерация и анализ комбинаций
        print("\n" + "=" * 50)
        print("АНАЛИЗ КОМБИНАЦИЙ:")
        data = generate_combinations(elements, k)

        print(f"Всего шагов: {len(data['шаги'])}")
        print(f"Частичных результатов: {len(data['частичные_результаты'])}")
        print(f"Итоговых комбинаций: {len(data['итоговые_результаты'])}")

        print("\nВсе шаги вычислений:")
        for i, step in enumerate(data['шаги'], 1):
            print(f"  Шаг {i}: {step}")

        print("\nВсе частичные результаты:")
        for i, partial in enumerate(data['частичные_результаты'], 1):
            print(
                f"  {i}. текущие={partial['текущие']}, старт={partial['стартовый_индекс']}, глубина={partial['глубина']}")

        print(f"\nВсе комбинации: {data['итоговые_результаты']}")

    else:
        print("Неверный выбор!")
