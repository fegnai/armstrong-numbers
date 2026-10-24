# Учебная практика ПМ.06, вариант 13.
# Программа ищет числа Армстронга - это числа, которые равны сумме своих
# цифр, возведённых в степень количества цифр.
# Например: 153 = 1 в кубе + 5 в кубе + 3 в кубе = 1 + 125 + 27.

import os          # проверка существования файлов
import logging     # запись журнала работы
import datetime    # текущая дата и время

import backup      # наш модуль резервного копирования (пункты меню 4 и 5)

REGISTRY_FILE = "registry.txt"   # имя файла-реестра, куда пишутся результаты

# --- ЖУРНАЛ РАБОТЫ -------------------------------------------------------
# Все события программы записываются в файл app.log.
# Каждая строка журнала выглядит так:  дата | время | действие
# format=  - что писать в строке: сначала дату со временем, потом действие
# datefmt= - как оформлять дату и время: день.месяц.год часы:минуты:секунды
# (эти две строки - стандартная запись модуля logging, по-другому нельзя)
logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s | %(message)s",
    datefmt="%d.%m.%Y %H:%M:%S",
    encoding="utf-8",
)


def time_now_text():
    # Собираем из текущих даты и времени строку вида "24.10.2026 14:30:05".
    # zfill(2) значит "добить нулём слева до двух знаков":
    # чтобы было "03:05", а не "3:5".
    now = datetime.datetime.now()
    day = str(now.day).zfill(2)
    month = str(now.month).zfill(2)
    year = str(now.year)
    hour = str(now.hour).zfill(2)
    minute = str(now.minute).zfill(2)
    second = str(now.second).zfill(2)
    return day + "." + month + "." + year + " " + hour + ":" + minute + ":" + second


def numbers_as_text(numbers):
    # Превращаем список чисел в текст: [1, 2, 3] превращается в "1, 2, 3".
    parts = []
    for n in numbers:
        parts.append(str(n))       # каждое число превращаем в строку
    return ", ".join(parts)        # склеиваем все строки через запятую


def is_armstrong(n):
    # Проверяем число n: равно ли оно сумме своих цифр, каждая из которых
    # возведена в степень, равную количеству цифр.
    digits = str(n)        # превращаем число в строку, чтобы пройтись по цифрам
    power = len(digits)    # сколько цифр в числе - такая и будет степень
    total = 0
    for d in digits:                       # берём каждую цифру по очереди
        total = total + int(d) ** power    # ** означает возведение в степень
    return total == n


def find_armstrong_numbers(limit):
    # Ищем все числа Армстронга от 1 до limit и возвращаем их списком.
    result = []
    for n in range(1, limit + 1):    # range даёт числа 1, 2, 3, ..., limit
        if is_armstrong(n):
            result.append(n)
    return result


def save_to_registry(limit, numbers):
    # Дописываем результат поиска в конец файла-реестра.
    stamp = time_now_text()          # дата и время поиска
    numbers_text = numbers_as_text(numbers)
    # "a" значит "дописать в конец файла", не стирая то, что там было
    with open(REGISTRY_FILE, "a", encoding="utf-8") as f:
        f.write(f"{stamp} | от 1 до {limit} | найдено {len(numbers)}: {numbers_text}\n")
    logging.info("Результат поиска добавлен в реестр")


def search_from_console():
    # Пункт 1: вводим границу N с клавиатуры,
    # ищем числа и показываем их на экране.
    while True:
        answer = input("Введите верхнюю границу N: ")
        try:
            limit = int(answer)      # пытаемся превратить введённый текст в число
        except ValueError:
            # int() не справился - значит, введено не число
            print("Ошибка: нужно целое число")
            logging.warning("Некорректный ввод N: не целое число")
            continue                 # возвращаемся к началу цикла - просим заново
        if limit < 1:
            print("Ошибка: число должно быть не меньше 1")
            logging.warning(f"Некорректный ввод N: {limit} (меньше 1)")
            continue
        break                        # число нормальное - выходим из цикла
    numbers = find_armstrong_numbers(limit)
    print("Найдено чисел Армстронга:", len(numbers))
    print(numbers_as_text(numbers))
    logging.info(f"Поиск с клавиатуры: от 1 до {limit}, найдено {len(numbers)}")
    save_to_registry(limit, numbers)
    print(f"Результат добавлен в реестр ({REGISTRY_FILE})")


def search_from_file():
    # Пункт 2: читаем границу N из файла input.txt,
    # найденные числа записываем в файл output.txt.
    with open("input.txt", "r", encoding="utf-8") as f:
        text = f.read().strip()      # strip убирает лишние пробелы и переводы строк
    limit = int(text)
    print("Из файла input.txt прочитано N =", limit)
    logging.info(f"Из файла input.txt прочитано N = {limit}")
    numbers = find_armstrong_numbers(limit)
    # "w" значит "записать файл заново", старое содержимое стирается
    with open("output.txt", "w", encoding="utf-8") as f:
        f.write(f"Числа Армстронга от 1 до {limit}:\n")
        for n in numbers:
            f.write(str(n) + "\n")
    logging.info(f"Поиск из файла: от 1 до {limit}, найдено {len(numbers)}")
    save_to_registry(limit, numbers)
    print("Найдено чисел:", len(numbers))
    print("Результат записан в файл output.txt")


def show_registry():
    # Пункт 3: показываем всё, что накопилось в реестре.
    if not os.path.exists(REGISTRY_FILE):
        print("Реестр пуст. Сначала выполните поиск (пункты 1 или 2)")
        return
    with open(REGISTRY_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()        # читаем все строки файла в список
    if len(lines) == 0:
        print("Реестр пуст")
        return
    print(f"РЕЕСТР НАЙДЕННЫХ ЧИСЕЛ (файл {REGISTRY_FILE}):")
    for line in lines:
        print(line.rstrip())         # rstrip убирает перевод строки в конце


def main():
    print("Программа поиска чисел Армстронга (учебная практика, вариант 13)")
    logging.info("Программа запущена")
    while True:
        print()
        print("1 - поиск чисел (ввод N с клавиатуры)")
        print("2 - поиск чисел (ввод N из файла input.txt, результат в output.txt)")
        print("3 - показать реестр найденных чисел")
        print("4 - сделать резервную копию реестра")
        print("5 - восстановить реестр из копии")
        print("0 - выход")
        choice = input("Выберите пункт: ").strip()
        logging.info(f"Выбран пункт меню: {choice}")
        if choice == "1":
            search_from_console()
        elif choice == "2":
            try:
                search_from_file()
            except FileNotFoundError:
                print("Файл input.txt не найден")
                logging.error("Файл input.txt не найден")
            except ValueError:
                print("Ошибка: в файле должно быть целое число")
                logging.error("Некорректное число в файле input.txt")
        elif choice == "3":
            show_registry()
        elif choice == "4":
            backup.make_backup()
        elif choice == "5":
            backup.restore_backup()
        elif choice == "0":
            print("Работа программы завершена")
            logging.info("Работа программы завершена")
            break
        else:
            print("Нет такого пункта, введите число от 0 до 5")
            logging.warning(f"Нет такого пункта: {choice}")


if __name__ == "__main__":
    main()