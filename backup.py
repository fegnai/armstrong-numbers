# Резервное копирование и восстановление реестра найденных чисел.
# Копия реестра кладётся в папку backup, в имени файла - дата и время.
# Можно запустить отдельно: python backup.py

import os
import shutil
import datetime

REGISTRY_FILE = "registry.txt"
BACKUP_DIR = "backup"


def make_backup():
    # делаем копию файла реестра
    if not os.path.exists(REGISTRY_FILE):
        print("Файла реестра нет, копировать нечего")
        return
    if not os.path.exists(BACKUP_DIR):
        os.mkdir(BACKUP_DIR)
    now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    copy_name = BACKUP_DIR + "/registry_" + now + ".txt"
    shutil.copy(REGISTRY_FILE, copy_name)
    print("Копия реестра создана:", copy_name)


def restore_backup():
    # восстанавливаем реестр из последней копии
    if not os.path.exists(BACKUP_DIR):
        print("Папки backup нет, восстанавливать нечего")
        return
    copies = os.listdir(BACKUP_DIR)
    if len(copies) == 0:
        print("Резервных копий нет")
        return
    copies.sort()
    last = copies[-1]
    shutil.copy(BACKUP_DIR + "/" + last, REGISTRY_FILE)
    print("Реестр восстановлен из копии:", last)


if __name__ == "__main__":
    print("1 - сделать резервную копию реестра")
    print("2 - восстановить реестр из копии")
    choice = input("Выберите пункт: ").strip()
    if choice == "1":
        make_backup()
    elif choice == "2":
        restore_backup()
    else:
        print("Нет такого пункта")
