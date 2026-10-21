# Учебная практика ПМ.06, вариант 13
# Программа ищет числа Армстронга в диапазоне от 1 до N.
# Число Армстронга - это число, которое равно сумме своих цифр,
# возведённых в степень, равную количеству цифр.
# Например: 153 = 1^3 + 5^3 + 3^3 = 1 + 125 + 27

import os
import datetime

import backup

REGISTRY_FILE = "registry.txt"  # реестр найденных чисел


def is_armstrong(n):
    # проверяем, является ли число n числом Армстронга
    digits = str(n)
    power = len(digits)  # сколько цифр в числе
    total = 0
    for d in digits:
        total += int(d) ** power
    return total == n


def find_armstrong_numbers(limit):
    # ищем все числа Армстронга от 1 до limit
    result = []
    for n in range(1, limit + 1):
        if is_armstrong(n):
            result.append(n)
    return result


def save_to_registry(limit, numbers):
    # дописываем результат поиска в реестр
    now = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    f = open(REGISTRY_FILE, "a", encoding="utf-8")
    f.write(now + " | от 1 до " + str(limit) + " | найдено " +
            str(len(numbers)) + ": " + ", ".join(str(n) for n in numbers) + "\n")
    f.close()


def search_from_console():
    # пункт 1: вводим N с клавиатуры, числа выводим на экран
    while True:
        try:
            limit = int(input("Введите верхнюю границу N: "))
        except ValueError:
            print("Ошибка: нужно целое число")
            continue
        if limit < 1:
            print("Ошибка: число должно быть не меньше 1")
            continue
        break
    numbers = find_armstrong_numbers(limit)
    print("Найдено чисел Армстронга:", len(numbers))
    print(", ".join(str(n) for n in numbers))
    save_to_registry(limit, numbers)
    print("Результат добавлен в реестр (" + REGISTRY_FILE + ")")


def search_from_file():
    # пункт 2: читаем N из файла input.txt, результат пишем в output.txt
    f = open("input.txt", "r", encoding="utf-8")
    limit = int(f.read().strip())
    f.close()
    print("Из файла input.txt прочитано N =", limit)
    numbers = find_armstrong_numbers(limit)
    f = open("output.txt", "w", encoding="utf-8")
    f.write("Числа Армстронга от 1 до " + str(limit) + ":\n")
    for n in numbers:
        f.write(str(n) + "\n")
    f.close()
    save_to_registry(limit, numbers)
    print("Найдено чисел:", len(numbers))
    print("Результат записан в файл output.txt")


def show_registry():
    # пункт 3: показываем содержимое реестра
    if not os.path.exists(REGISTRY_FILE):
        print("Реестр пуст. Сначала выполните поиск (пункты 1 или 2)")
        return
    f = open(REGISTRY_FILE, "r", encoding="utf-8")
    lines = f.readlines()
    f.close()
    if len(lines) == 0:
        print("Реестр пуст")
        return
    print("РЕЕСТР НАЙДЕННЫХ ЧИСЕЛ (файл " + REGISTRY_FILE + "):")
    for line in lines:
        print(line.rstrip())


def main():
    print("Программа поиска чисел Армстронга (учебная практика, вариант 13)")
    while True:
        print()
        print("1 - поиск чисел (ввод N с консоли)")
        print("2 - поиск чисел (ввод N из файла input.txt, вывод в output.txt)")
        print("3 - показать реестр найденных чисел")
        print("4 - резервная копия реестра")
        print("5 - восстановить реестр из копии")
        print("0 - выход")
        choice = input("Выберите пункт: ").strip()
        if choice == "1":
            search_from_console()
        elif choice == "2":
            try:
                search_from_file()
            except FileNotFoundError:
                print("Файл input.txt не найден")
            except ValueError:
                print("Ошибка: в файле должно быть целое число")
        elif choice == "3":
            show_registry()
        elif choice == "4":
            backup.make_backup()
        elif choice == "5":
            backup.restore_backup()
        elif choice == "0":
            print("Работа программы завершена")
            break
        else:
            print("Нет такого пункта, введите число от 0 до 5")


if __name__ == "__main__":
    main()
