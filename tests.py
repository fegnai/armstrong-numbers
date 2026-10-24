# Автоматические тесты для программы (pytest + Faker).
# Faker генерирует случайные данные (числа и слова), pytest запускает тесты.
# Перед запуском установить библиотеки:  pip install pytest faker
# Запуск:  pytest tests.py -v   (или просто:  python tests.py)
# Данные случайные, но повторяемые: задано фиксированное зерно (seed 13).

import re
import sys

import pytest
from faker import Faker

import backup
import main
from main import (is_armstrong, find_armstrong_numbers, save_to_registry,
                  search_from_console, search_from_file, show_registry)

fake = Faker("ru_RU")
fake.seed_instance(13)  # фиксированное зерно: при каждом запуске данные одинаковые

# все числа Армстронга от 1 до 10000 - известный заранее правильный ответ
ALL_TO_10000 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 153, 370, 371, 407, 1634, 8208, 9474]


def test_known_numbers():
    # тест 1: контрольные числа определяются правильно
    assert is_armstrong(153) == True   # 1 + 125 + 27 = 153
    assert is_armstrong(370) == True
    assert is_armstrong(371) == True
    assert is_armstrong(407) == True
    assert is_armstrong(1634) == True  # 1 + 1296 + 81 + 256 = 1634
    assert is_armstrong(9474) == True
    assert is_armstrong(8208) == True  # 8 + 32 + 0 + 32768 = 8208
    assert is_armstrong(548834) == True  # шестизначное число Армстронга
    # обычные числа не считаются числами Армстронга
    assert is_armstrong(10) == False
    assert is_armstrong(152) == False
    assert is_armstrong(154) == False
    assert is_armstrong(999) == False
    assert is_armstrong(548835) == False


def test_random_numbers_against_formula():
    # тест 2: для 50 случайных чисел результат совпадает
    # с независимой проверкой по формуле из определения
    for _ in range(50):
        n = fake.random_int(min=1, max=9999)
        expected = sum(int(d) ** len(str(n)) for d in str(n)) == n
        assert is_armstrong(n) == expected


def test_random_range():
    # тест 3: поиск по случайной границе даёт правильный список
    for _ in range(10):
        limit = fake.random_int(min=1, max=10000)
        numbers = find_armstrong_numbers(limit)
        # каждое найденное число действительно удовлетворяет свойству
        for n in numbers:
            assert is_armstrong(n) == True
        # список отсортирован и без повторов
        assert numbers == sorted(set(numbers))
        # при границе не меньше 9 однозначные числа обязаны найтись
        if limit >= 9:
            assert numbers[:9] == [1, 2, 3, 4, 5, 6, 7, 8, 9]


def test_boundaries():
    # тест 4: граничные значения верхней границы N
    assert find_armstrong_numbers(0) == []      # ничего не ищем
    assert find_armstrong_numbers(1) == [1]     # только единица
    assert find_armstrong_numbers(9) == [1, 2, 3, 4, 5, 6, 7, 8, 9]
    assert find_armstrong_numbers(10) == [1, 2, 3, 4, 5, 6, 7, 8, 9]  # 10 - не Армстронг


def test_full_list_up_to_10000():
    # тест 5: при N = 10000 список совпадает с известным правильным ответом
    assert find_armstrong_numbers(10000) == ALL_TO_10000


def test_save_to_registry(tmp_path, monkeypatch):
    # тест 6: результат случайного поиска попадает в реестр
    registry = tmp_path / "registry.txt"
    monkeypatch.setattr(main, "REGISTRY_FILE", str(registry))
    limit = fake.random_int(min=100, max=500)
    numbers = find_armstrong_numbers(limit)
    save_to_registry(limit, numbers)
    text = registry.read_text(encoding="utf-8")
    assert f"от 1 до {limit}" in text
    assert f"найдено {len(numbers)}" in text


def test_registry_line_format(tmp_path, monkeypatch):
    # тест 7: строка реестра имеет формат "дата | время | от 1 до N | найдено M: ..."
    registry = tmp_path / "registry.txt"
    monkeypatch.setattr(main, "REGISTRY_FILE", str(registry))
    limit = fake.random_int(min=1, max=1000)
    numbers = find_armstrong_numbers(limit)
    save_to_registry(limit, numbers)
    line = registry.read_text(encoding="utf-8").strip()
    pattern = (r"^\d{2}\.\d{2}\.\d{4} \d{2}:\d{2}:\d{2}"
               r" \| от 1 до \d+ \| найдено \d+: ")
    assert re.match(pattern, line), "формат строки реестра нарушен: " + line


def test_show_registry_output(tmp_path, monkeypatch, capsys):
    # тест 8: пустой реестр и заполненный реестр показываются правильно
    registry = tmp_path / "registry.txt"
    monkeypatch.setattr(main, "REGISTRY_FILE", str(registry))
    show_registry()
    out = capsys.readouterr().out
    assert "Реестр пуст" in out                     # файла ещё нет
    line1 = fake.date_object().strftime("%d.%m.%Y") + " | " + fake.word()
    line2 = fake.date_object().strftime("%d.%m.%Y") + " | " + fake.word()
    registry.write_text(line1 + "\n" + line2 + "\n", encoding="utf-8")
    show_registry()
    out = capsys.readouterr().out
    assert "РЕЕСТР НАЙДЕННЫХ ЧИСЕЛ" in out          # заголовок выводится
    assert line1 in out and line2 in out            # обе записи на экране


def test_search_from_file(tmp_path, monkeypatch):
    # тест 9: поиск по файлу - N читается из input.txt, результат в output.txt
    registry = tmp_path / "registry.txt"
    monkeypatch.setattr(main, "REGISTRY_FILE", str(registry))
    monkeypatch.chdir(tmp_path)                     # работаем во временной папке
    limit = fake.random_int(min=10, max=500)
    (tmp_path / "input.txt").write_text(str(limit), encoding="utf-8")
    search_from_file()
    out_text = (tmp_path / "output.txt").read_text(encoding="utf-8")
    assert f"Числа Армстронга от 1 до {limit}" in out_text
    numbers = find_armstrong_numbers(limit)
    for n in numbers:                               # каждое число попало в output.txt
        assert str(n) in out_text
    assert f"найдено {len(numbers)}" in registry.read_text(encoding="utf-8")


def test_search_from_file_bad_content(tmp_path, monkeypatch):
    # тест 10: слово в input.txt вместо числа даёт ошибку ValueError
    monkeypatch.chdir(tmp_path)
    (tmp_path / "input.txt").write_text(fake.word(), encoding="utf-8")
    with pytest.raises(ValueError):
        search_from_file()


def test_wrong_input(monkeypatch, tmp_path, capsys):
    # тест 11: слово вместо числа не ломает программу,
    # после ошибки программа принимает правильное число
    registry = tmp_path / "registry.txt"
    monkeypatch.setattr(main, "REGISTRY_FILE", str(registry))
    answers = iter([fake.word(), str(fake.random_int(min=1, max=300))])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(answers))
    search_from_console()  # не должно вызвать аварийное завершение
    out = capsys.readouterr().out
    assert "Ошибка: нужно целое число" in out   # слово отвергнуто
    assert "Найдено чисел Армстронга" in out    # затем поиск выполнен


def test_menu_wrong_choice_and_exit(monkeypatch, capsys):
    # тест 12: неверный пункт меню не ломает программу, выход по пункту 0
    answers = iter([fake.word(), "0"])          # сначала мусор, потом "0"
    monkeypatch.setattr("builtins.input", lambda prompt="": next(answers))
    main.main()
    out = capsys.readouterr().out
    assert "Нет такого пункта" in out
    assert "Работа программы завершена" in out


def test_backup_and_restore(tmp_path, monkeypatch):
    # тест 13: копия реестра создаётся и восстанавливается
    registry = tmp_path / "registry.txt"
    backup_dir = tmp_path / "backup"
    monkeypatch.setattr(main, "REGISTRY_FILE", str(registry))
    monkeypatch.setattr(backup, "REGISTRY_FILE", str(registry))
    monkeypatch.setattr(backup, "BACKUP_DIR", str(backup_dir))
    # случайная запись в реестре (данные генерирует Faker)
    session = fake.date_object().strftime("%d.%m.%Y") + " | " + fake.word()
    registry.write_text(session, encoding="utf-8")
    backup.make_backup()
    assert backup_dir.exists()               # копия создана
    registry.write_text("испорчено", encoding="utf-8")
    backup.restore_backup()
    # реестр вернулся к исходному содержимому
    assert registry.read_text(encoding="utf-8") == session


def test_backup_missing_files(tmp_path, monkeypatch, capsys):
    # тест 14: копирование и восстановление без файлов не ломают программу
    monkeypatch.setattr(backup, "REGISTRY_FILE", str(tmp_path / "нет.txt"))
    monkeypatch.setattr(backup, "BACKUP_DIR", str(tmp_path / "нет_папки"))
    backup.make_backup()                         # файла реестра нет
    backup.restore_backup()                      # папки backup нет
    out = capsys.readouterr().out
    assert "Файла реестра нет" in out
    assert "Папки backup нет" in out


def test_restore_takes_latest_copy(tmp_path, monkeypatch):
    # тест 15: при нескольких копиях восстанавливается самая поздняя
    registry = tmp_path / "registry.txt"
    backup_dir = tmp_path / "backup"
    backup_dir.mkdir()
    monkeypatch.setattr(backup, "REGISTRY_FILE", str(registry))
    monkeypatch.setattr(backup, "BACKUP_DIR", str(backup_dir))
    # две копии с разными датами (данные генерирует Faker)
    old_text = fake.date_object().strftime("%d.%m.%Y") + " | " + fake.word()
    new_text = fake.date_object().strftime("%d.%m.%Y") + " | " + fake.word()
    (backup_dir / "registry_2026-10-10_10-00-00.txt").write_text(old_text, encoding="utf-8")
    (backup_dir / "registry_2026-10-11_11-00-00.txt").write_text(new_text, encoding="utf-8")
    registry.write_text("испорчено", encoding="utf-8")
    backup.restore_backup()
    # вернулась именно последняя копия, а не старая
    assert registry.read_text(encoding="utf-8") == new_text


if __name__ == "__main__":
    # чтобы тесты запускались и простой командой python tests.py
    print("Запуск тестов через pytest...")
    sys.exit(pytest.main(["-v", __file__]))
