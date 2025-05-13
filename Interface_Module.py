# Модуль консольного интерфейса программы, его задача перевод желания пользователя
# в команды, понимаемые программой.

# Добавить функцию ввода пароля со * вместо символов и двойную проверку на корректность
# Переписать функции ввода и добавить авто локализацию на английский
# Использовать консольный библиотеки (colorama, termcolor, art, simple-term-menu, tabulate, Rich, alive-progress)

# Импорт графических библиотек
from termcolor import colored as col, cprint
from sys import exit
from os import system 

def clear():
    system('cls') # Функция очистки экрана

# Функция первого уровня интерфейса (ответы последующих уровней конкатенируются с ответом этого уровня)
def main_interface(current_task_= ""):
    
    while True:
        
        clear()
        cprint("\nLumos TO->DO", "blue", attrs=["bold"])
        cprint("Текущая задача:", "green", end=" ")
        
        if current_task_ == "": print("Ура, все задачи выполнены! Придумай ещё =)", end="\n\n")
        else: print(current_task_, end="\n\n")
        
        print("Выберите команду:\n",
            "[1] Выполнить текущую задачу\n",
            "[2] Перейти к следующей задаче\n",
            "[3] Добавить ещё задачи\n",
            "[4] Вывести список задач\n",
            "[5] Вывести список архивных задач\n",
            "[0] Выход\n",
        )

        inp = input("Введите номер команды цифрой: ")
        if inp not in ["1", "2", "3", "4", "5", "0"]:
            print("Неверный ввод")
            input("Press Enter to continue...")
            continue
        elif inp == "1" and current_task_ != "":
            return inp
            
        elif inp == "2" and current_task_ != "":
            return inp 
           
        elif inp == "3":
            return inp
        elif inp == "4":
            return inp
        elif inp == "5":
            return inp
        elif inp == "0":
            cprint("\nДо свидания!", attrs=["bold"])
            input("Press Enter to continue...")
            exit()
        else:
            return inp


def task_done():  # Функция выполнения задачи
    while True:
        clear()
        cprint("Что случилось с задачей?", "yellow")
        print("[1] Задача успешно выполнена")
        print("[2] Задача более неактуальна")
        print("[0] Назад")
        inp = input("Введите номер команды цифрой: ")
        if inp not in ["1", "2", "0"]:
            print("Неверный ввод")
            input("Press Enter to continue...")
            continue
        elif inp in ["1", "2"]:
            cprint("\nЗадача завершена и перемещена в архив!", attrs=["bold"])
            input("Press Enter to continue...")
            return inp
        else:  # inp == "0"
            return inp
        
def show_new_task(new_task_str: str = ""):  # Функция новой задачи
    clear()
    cprint(f"Да здравствует следующая задача:", "green")
    print(f"-> {new_task_str}")
    input("Press Enter to continue...")

def input_task():  # Функция ввода задачи
    clear()
    cprint("Введите новую задачу:", "light_blue")
    task = input("->")
    return task

def task_list(list_str: str = "", prefix: str = "Список задач:"):  # Функция вывода списка задач
    clear()
    if list_str == "":  list_str = "Список задач пуст!"
    cprint(prefix, attrs=["bold"])
    print(list_str)
    input("Press Enter to continue...")

def inp_task_ok(task_str: str):  # Функция подтверждения ввода задачи
    print(f"Задача, {task_str}, успешно добавлена!")
    input("Press Enter to continue...")

def next_task():  # Функция перехода к следующей задаче
    while True:
        clear()
        cprint("Перейти к следующей задаче?", "yellow")
        print("[1] Да")
        print("[0] Нет")
        inp = input("Введите номер команды цифрой: ")
        if inp not in ["1", "0"]:
            print("\nНеверный ввод")
            input("Press Enter to continue...")
            continue
        else:
            break
    return inp


def add_task():  # Функция добавления задачи
    while True:
        clear()
        cprint("Куда добавить задачу?", "blue")
        print("[1] в срочный и важный список")
        print("[2] в не срочный но важный список")
        print("[3] в срочный но не важный список")
        print("[4] в не срочный и не важный список")
        print("[5] не знаю в какой...")
        print("[0] Назад")
        inp = input("Введите номер команды цифрой: ")
        if inp not in ["1", "2", "3", "4", "5", "0"]:
            print("Неверный ввод")
            input("Press Enter to continue...")
            continue
        elif inp == "5":
            inp = auto_task()
            return inp
        else:
            return inp


# Функция автоопределения задачи
def auto_task():
    immediate = 0
    important = 0
    while True:
        clear()
        print("Если эта задача не выполнится в срок, то станет хуже?")
        print("[1] Да")
        print("[2] Нет")
        inp2 = input("Введите номер команды цифрой: ")
        if inp2 not in ["1", "2"]:
            print("Неверный ввод")
            input("Press Enter to continue...")
            continue
        elif inp2 == "1":
            immediate = 1
            break
        else:
            break

    while True:
        clear()
        print("Если эта задача выполнится в срок, то станет лучше?")
        print("[1] Да")
        print("[2] Нет")
        inp2 = input("Введите номер команды цифрой: ")
        if inp2 not in ["1", "2"]:
            print("Неверный ввод")
            input("Press Enter to continue...")
            continue
        elif inp2 == "1":
            important = 1
            break
        else:
            break

    if immediate == 1 and important == 1:
        return "1"
    elif immediate == 0 and important == 1:
        return "2"
    elif immediate == 1 and important == 0:
        return "3" 
    else:
        return "4" 
