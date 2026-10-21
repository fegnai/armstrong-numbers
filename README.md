# Поиск чисел Армстронга

Учебный проект по ПМ.06 «Сопровождение информационных систем» (учебная практика, вариант 13).
Программа на Python ищет все числа Армстронга в диапазоне от 1 до N, введённого пользователем.

**Число Армстронга** — число, которое равно сумме своих цифр, возведённых в степень, равную количеству цифр.
Например: 153 = 1³ + 5³ + 3³ = 1 + 125 + 27.

## Установка

Программу устанавливать не нужно — достаточно, чтобы на компьютере стоял Python 3 и была папка проекта.

1. Если Python 3 не установлен, скачайте его с сайта https://www.python.org/downloads/ и установите.
2. Проверьте, что Python работает:

```
python --version
```

3. Скачайте папку проекта с GitHub (зелёная кнопка Code → Download ZIP) и распакуйте её в любое место.

## Как запустить

Сторонние библиотеки не используются. Откройте командную строку в папке проекта и выполните:

```
python main.py
```

## Как пользоваться

Программа показывает меню:

1. Вводим N с клавиатуры — числа выводятся на экран.
2. N читается из файла `input.txt`, результат записывается в `output.txt`.
3. Показать реестр всех найденных чисел (файл `registry.txt`).
4. Сделать резервную копию реестра (папка `backup`).
5. Восстановить реестр из последней копии.
0. Выход.

## Проверка тестами

```
python tests.py
```

Все тесты должны пройти (сообщение «Все тесты пройдены!»).

## Файлы проекта

| Файл | Назначение |
|------|------------|
| `main.py` | основная программа |
| `backup.py` | резервное копирование и восстановление реестра |
| `tests.py` | тесты |
| `input.txt` | пример файла для ввода N |
| `ТЗ.md` | техническое задание |
| `Регламент_ТО.md` | регламент технического обслуживания |

Автор: Арюткин Максим Сергеевич, группа ИСП-31, 3 курс.

Версия программы: 1.0

---

# Armstrong Numbers Search

Educational project for PM.06 "Information Systems Support" (internship, task 13).
A Python program that finds all Armstrong numbers in the range from 1 to N entered by the user.

An **Armstrong number** is a number that equals the sum of its digits, each raised to the power of the number of digits.
Example: 153 = 1³ + 5³ + 3³ = 1 + 125 + 27.

## Installation

The program does not need to be installed — you only need Python 3 and the project folder.

1. If Python 3 is not installed, download it from https://www.python.org/downloads/ and install it.
2. Check that Python works:

```
python --version
```

3. Download the project folder from GitHub (green Code button → Download ZIP) and unpack it anywhere.

## How to run

No third-party libraries are used. Open a terminal in the project folder and run:

```
python main.py
```

## How to use

The program shows a menu:

1. Enter N from the keyboard — the numbers are printed on the screen.
2. N is read from the file `input.txt`, the result is written to `output.txt`.
3. Show the registry of all found numbers (file `registry.txt`).
4. Make a backup copy of the registry (folder `backup`).
5. Restore the registry from the latest copy.
0. Exit.

## Tests

```
python tests.py
```

All tests must pass (the message "Все тесты пройдены!").

## Project files

| File | Purpose |
|------|---------|
| `main.py` | main program |
| `backup.py` | backup and restore of the registry |
| `tests.py` | tests |
| `input.txt` | example input file for N |
| `ТЗ.md` | technical specification (in Russian) |
| `Регламент_ТО.md` | maintenance regulations (in Russian) |

Author: Maxim Arutykin, group ISP-31, 3rd year.

Program version: 1.0
