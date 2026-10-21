# Тесты для проверки программы.
# Запуск: python tests.py

import os
import shutil

from main import is_armstrong, find_armstrong_numbers
import backup


print("Тест 1. Числа Армстронга определяются правильно")
assert is_armstrong(153) == True   # 1 + 125 + 27 = 153
assert is_armstrong(370) == True
assert is_armstrong(371) == True
assert is_armstrong(407) == True
assert is_armstrong(1634) == True  # 1 + 1296 + 81 + 256 = 1634
print("OK")

print("Тест 2. Обычные числа не считаются числами Армстронга")
assert is_armstrong(10) == False
assert is_armstrong(100) == False
assert is_armstrong(152) == False
assert is_armstrong(999) == False
print("OK")

print("Тест 3. Поиск чисел от 1 до 1000")
numbers = find_armstrong_numbers(1000)
assert numbers == [1, 2, 3, 4, 5, 6, 7, 8, 9, 153, 370, 371, 407]
print("OK, найдено:", len(numbers))

print("Тест 4. Поиск чисел от 1 до 10000")
numbers = find_armstrong_numbers(10000)
assert len(numbers) == 16  # добавляются 1634, 8208, 9474
print("OK, найдено:", len(numbers))

print("Тест 5. Резервное копирование и восстановление реестра")
# создаём временный реестр
f = open("registry.txt", "w", encoding="utf-8")
f.write("тестовая запись\n")
f.close()
backup.make_backup()
assert os.path.exists("backup")
# портим реестр и восстанавливаем его из копии
f = open("registry.txt", "w", encoding="utf-8")
f.write("испорчено\n")
f.close()
backup.restore_backup()
f = open("registry.txt", "r", encoding="utf-8")
content = f.read()
f.close()
assert "тестовая запись" in content
print("OK")

# убираем за собой тестовые файлы
os.remove("registry.txt")
shutil.rmtree("backup")

print()
print("Все тесты пройдены!")
