from datetime import datetime

def print_logs(log: str = ""):
    log = str(log)
    now = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    log += f" Date and time: {now}"
    func_data_list("log.txt", (log,))




# -----------------------------------------------------------------------------------------
# Функция func_data_list - создает/добавляет/перезаписывает/считывает список базы данных стека или очереди,
# Входные параметры:
# filename_dl - название/путь к файлу списка
# in_list_dl - список имён для записи
# del_bl - флаг замены старого списка новыми данными
# -----------------------------------------------------------------------------------------
# Функция для создания базы данных - последовательный список для работы со стеком или очередью
def func_data_list(filename_dl: str, in_list_dl: tuple = (), del_dl: bool = False):
    # Открытие или создание файла если его нет для чтения
    in_list_dl = tuple(str(i1) for i1 in in_list_dl)  # Принудительное преобразование ссылок в кортеж
    f_list_dl: list = []
    try:
        if not del_dl:
            with open(filename_dl, "a+") as file_dl:
                file_dl.seek(0)  # Перевод указателя в начало файла
                # Считывание данных из файла с разбиением на строки
                f_list_dl = file_dl.read().splitlines()
            # Автозакрытие файла

        if del_dl:  # Проверка флага стирания старых имен
            f_list_dl = list(in_list_dl)  # Замена данных в старом списке на новые
        elif in_list_dl:
            # Иначе добавление элементов из нового списка
            f_list_dl.extend(in_list_dl)
            
        if in_list_dl == "" and not del_dl:
            return f_list_dl

        # Открытие или создание файла если его нет для перезаписи
        with open(filename_dl, "w") as file_dl:
            # Объединение списка в строку с добавлением символа начала новой строки
            #  и запись данных в файл
            file_dl.write("\n".join(f_list_dl))  # Запись обновленного списка
            # Автозакрытие файла
        # Возврат списка строк из файла
    except OSError:
            print("Ошибка файловой операции")
            return ("Error")
        
    return tuple(f_list_dl)


# --End func data_list