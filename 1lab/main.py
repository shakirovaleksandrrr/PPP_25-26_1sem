from random import randint as rnd


def make_field(n, m):
    #Генерация поля
    field = []
    for i in range(n):
        row = []
        for j in range(m):
            row.append(rnd(0, 1))
        field.append(row)
    return field


def show_field(f):
    #Вывод поля
    for r in f: print(' '.join(map(str, r)))
    print()


def island_size(field, i, j, visited):
    #замер острова
    if i < 0 or j < 0:
        return 0
    if i >= len(field) or j >= len(field[0]):
        return 0
    if field[i][j] == 0 or visited[i][j]:
        return 0

    visited[i][j] = True
    size = 1
    # Проверка всех соседних клеток и добавление к размеру
    size += island_size(field, i - 1, j, visited)
    size += island_size(field, i + 1, j, visited)
    size += island_size(field, i, j - 1, visited)
    size += island_size(field, i, j + 1, visited)

    return size


def get_all_islands(field):
    #сбор списка островов
    if not field:
        return []

    n = len(field)
    m = len(field[0])

    visited = []
    for i in range(n):
        visited.append([False] * m)

    islands = []

    for i in range(n):
        for j in range(m):
            if field[i][j] == 1 and not visited[i][j]:
                size = island_size(field, i, j, visited)
                islands.append(size)

    return islands


def count_rows_with_many_ones(field):
    #Подсчёт количества строк, где встречается более 3 единиц
    count = 0
    for row in field:
        ones = sum(row)
        if ones > 3:
            count += 1
    return count


def count_cols_with_many_ones(field):
    # Подсчёт количества столбцов, где встречается более 3 единиц
    if not field:
        return 0

    n = len(field)
    m = len(field[0])
    count = 0

    for j in range(m):
        ones = 0
        for i in range(n):
            ones += field[i][j]
        if ones > 3:
            count += 1

    return count


def main():

    try:
        n = int(input("Введите N: "))
        m = int(input("Введите M: "))

        if n <= 0 or m <= 0:
            print("Ошибка: размеры должны быть больше 0")
            return

    except ValueError:
        print("Ошибка: введите целые числа")
        return

    field = make_field(n, m)

    print("Поле:")
    show_field(field)

    islands = get_all_islands(field)

    print("Размеры островов:")
    if islands:
        for i, size in enumerate(islands, 1):
            print(f"Остров {i}: {size}")
    else:
        print("Островов нет")

    print(f"Всего островов: {len(islands)}")

    row_count = count_rows_with_many_ones(field)
    col_count = count_cols_with_many_ones(field)

    print(f"Строк с >3 единиц: {row_count}")
    print(f"Столбцов с >3 единиц: {col_count}")

    total_ones = 0
    for row in field:
        total_ones += sum(row)

    print(f"Всего единиц на поле: {total_ones}")


if __name__ == "__main__":
    main()