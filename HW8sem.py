from csv import DictWriter, DictReader
from os.path import exists


class NameError(Exception):
    def __init__(self, txt):
        self.txt = txt


def get_data():
    flag = False
    while not flag:
        try:
            first_name = input("Введите имя: ")
            if len(first_name) < 2:
                raise NameError("Слишком короткое имя")
            last_name = input("Введите имя: ")
            if len(last_name) < 5:
                raise NameError("Слишком короткая фамилия")
        except NameError as err:
            print(err)
        else:
            flag = True
    phone = "+73287282037"
    return [first_name, last_name, phone]


def create_file(filename):
    with open(filename, 'w', encoding='utf-8') as data:
        f_w = DictWriter(data, fieldnames=['Имя', 'Фамилия', 'Телефон'])
        f_w.writeheader()


def read_file(filename):
    with open(filename, 'r', encoding='utf-8') as data:
        f_r = DictReader(data)
        return list(f_r)


def write_file(filename, lst):
    res = read_file(filename)
    obj = {'Имя': lst[0], 'Фамилия': lst[1], 'Телефон': lst[2]}
    res.append(obj)
    standart_write(filename,res)


def row_search(filename):
    last_name = input("Введите фамилию: ")
    res = read_file(filename)
    for row in res:
        if last_name == row['Фамилия']:
            return row
    return "Запись не найдена"


def delete_row(filename):
    row_number = int(input("Введите номер строки: "))
    res = read_file(filename)
    res.pop(row_number-1)
    standart_write(filename, res)


def standart_write(filename, res):
    with open(filename, 'w', encoding='utf-8') as data:
        f_w = DictWriter(data, fieldnames=['Имя', 'Фамилия', 'Телефон'])
        f_w.writeheader()
        f_w.writerows(res)


def change_row(filename):
    row_number = int(("Введите номер строки: "))
    res = read_file(filename)
    data = get_data()
    res[row_number-1]["Имя"] = data [0]
    res[row_number-1]["Фамилия"] = data [1]
    res[row_number-1]["Телефон"] = data [2]
    standart_write(filename, res)

def select_element_from_list(my_list, to_print_list, message):
    if len(my_list) == 0:
        return -1
    else:
        if to_print_list:
            print(f"{message}:")
            for i in range(len(my_list)):
                print(i + 1, end="\t")
                print(my_list[i])
        while True:
            try:
                number = int(input("Введите номер для выбор строки: "))
                if 0 < number <= len(my_list):
                    return number - 1
                else:
                    print("В списке нет строки с таким номером.")
            except ValueError:
                print("Необходимо ввести целое число из списка.")

class FileNameLength(Exception):
    def __init__(self, txt):
        self.txt = txt

class WrongFileName(Exception):
    def __init__(self, txt):
        self.txt = txt

def enter_file_name():
    while True:
        try:
            result = input("Введите имя, под которым файл будет сохранен: ").replace("\r\n", " ") + ".csv"
            directory_path = os.getcwd()
            full_path = directory_path + result
            if (len(full_path)) > 255:
                raise FileNameLength("Путь к файлу не может быть длиннее 255 символов. Сократите имя файла.")
            else:
                for ch in result:
                    if ch in {"<", ">", ":", "\"", "/", "\\", "|", "?", "*"}:
                        raise WrongFileName("Имя файла не может содержать символы < > : \" / \\ | ? *")
            return result
        except FileNameLength as error:
            print(error)
        except WrongFileName as error:
            print(error)

def look_up_for_tables():
    files_list = list()
    for entry in os.scandir(os.getcwd()):
        if entry.is_file():
            if os.path.splitext(entry.path)[1] == ".csv":
                files_list.append(entry.name)
    return files_list

def move_contact(contacts_list):
    if len(contacts_list) == 0:
        print("Список контактов пуст.")
    else:
        index = select_element_from_list(contacts_list, False, "")
        while True:
            print("Перенести контакт: \"n\" – в новый список, \"o\" – в существующий.")
            command = input("Введите команду: ").lower()
            if command == "n":
                file_name = enter_file_name()
                write_file(file_name, [contacts_list[index]])
                break
            elif command == "o":
                files_list = look_up_for_tables()
                if len(files_list) > 0:
                    file_name = files_list[select_element_from_list(files_list, True, "Список файлов")]
                    another_contacts_list = read_file(file_name)
                    another_contacts_list.append(contacts_list[index])
                    write_file(file_name, another_contacts_list)
                    break
                else:
                    print("В текущей директории нет подходящих файлов.")

filename = 'phone.csv'


def main():
    while True:
        command = input("Введите команду: ")
        if command == "q":
            break
        elif command == "w":
            if not exists(filename):
                create_file(filename)
                write_file(filename, get_data())
        elif command == "r":
            if not exists(filename):
                print("Файл не существует. Создайте его.")
                continue
            print(read_file(filename))
        elif command == "f":
            if not exists(filename):
                print("Файл не существует. Создайте его.")
                continue
            print(row_search(filename))
        elif command == "d":
            if not exists(filename):
                print("Файл не существует. Создайте его.")
                continue
            delete_row(filename)
        elif command == "c":
            if not exists(filename):
                print("Файл не существует. Создайте его.")
                continue
            change_row(filename)
        elif command == "m":
            move_contact(filename)


main()