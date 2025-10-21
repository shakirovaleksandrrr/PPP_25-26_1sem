def main():
    # Ввод команд
    commands_input = input("Введите команды через пробел: ").strip()
    commands = commands_input.split()

    # Ввод строки
    input_string = input("Введите строку для обработки: ").strip()

    # Обработка команд
    result, steps = process_commands(input_string, commands)

    # Вывод результатов
    print(f"Исходная строка: {input_string}")
    print(f"Результат: {result}")

    print("\nПошаговое изменение:")
    for i, (command, string) in enumerate(steps):
        if command == "start":
            print(f"Шаг {i}: начальная строка = '{string}'")
        else:
            print(f"Шаг {i}: после '{command}' = '{string}'")

        # Изменения для первого символа в формате a:a -> a:b -> a:y -> a:z -> a:a
    if input_string:
        first_char = input_string[0]
        char_changes = get_step_by_step_changes(steps, first_char)
        if char_changes:
            changes_str = " -> ".join([f"{first_char}:{char}" for command, char in char_changes])
            print(f"\nИзменения для символа '{first_char}': {changes_str}")


def process_commands(input_string, commands):
    # Обрабатывает последовательность команд над строкой
    steps = []
    current_string = input_string

    # Сохраняем исходное состояние
    steps.append(("start", current_string))

    for command in commands:
        # Валидация команды
        is_valid, cmd_type, param = validate_command(command)
        if not is_valid:
            raise ValueError(f"Некорректная команда: {command}")

        try:
            if cmd_type == 'c':
                # Шифр Цезаря
                current_string = caesar_cipher(current_string, param)
                steps.append((f"c{param}", current_string))
            elif cmd_type == 'r':
                # Реверс строки
                current_string = reverse_string(current_string)
                steps.append(("r", current_string))

        except Exception as e:
            raise RuntimeError(f"Ошибка при выполнении команды {command}: {str(e)}")

    return current_string, steps


def validate_command(command):
    # Валидация команды (валидна, тип, параметр)
    if not command:
        return False, '', 0

    # Определяем тип команды
    cmd_type = command[0]

    if cmd_type == 'r':
        # Для 'r' не должно быть параметров
        if len(command) > 1:
            return False, '', 0
        return True, 'r', 0

    elif cmd_type == 'c':
        # Для 'c' должен быть параметр
        if len(command) <= 1:
            return False, '', 0

        param_str = command[1:]

        # Параметр целое число?
        if param_str.startswith('-'):
            # Отрицательное число
            if len(param_str) == 1 or not param_str[1:].isdigit():
                return False, '', 0
        else:
            # Положительное число
            if not param_str.isdigit():
                return False, '', 0

        try:
            param = int(param_str)
            return True, 'c', param
        except ValueError:
            return False, '', 0

    return False, '', 0


def caesar_cipher(text, shift):
    # Шифр Цезаря
    result = []
    for char in text:
        if char.isalpha():
            # Сдвиг буквы по модулю 26
            base = ord('A') if char.isupper() else ord('a')
            shifted_char = chr((ord(char) - base + shift) % 26 + base)
            result.append(shifted_char)
        else:
            result.append(char)
    return ''.join(result)


def reverse_string(text):
    # Реверс строки
    return text[::-1]


def get_step_by_step_changes(steps, original_char):
    # Возвращает поэтапные изменения для конкретного символа
    if not steps:
        return []

    char_changes = []
    current_char = original_char

    for step in steps:
        command, full_string = step

        if command == "start":
            char_changes.append(("start", current_char))
            continue

        # Находим позицию символа в исходной строке
        if steps[0][1]:
            original_string = steps[0][1]
            if original_char in original_string:
                char_index = original_string.index(original_char)
                if char_index < len(full_string):
                    current_char = full_string[char_index]
                    char_changes.append((command, current_char))

    return char_changes


if __name__ == "__main__":
    main()
