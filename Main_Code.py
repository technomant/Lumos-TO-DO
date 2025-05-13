#Как обычно придумал больше чем успел воплотить в код)

    #Импорт библиотек
import Class_Lib as Cl_
import Interface_Module as Int_m
import log_module as lm
from os import makedirs as mk, path 
from sys import exit, executable

#Обработка исключений
try:


    
    #Абсолютный путь к папке скрипта
    own_path = path.dirname(executable)
    #Путь к папке data
    data_path = path.join(own_path, "data")
    #Создание папки для хранения данных
    mk(data_path, exist_ok=True) 

    #Создание экземпляров класса ListTasks (в архив добавить пометку "сделано/ отменено, не актуально с разделителем CSV")
    rush_imp_tasks = Cl_.ListTasks(path.join(data_path, "Важные срочные задачи.csv"), 
                                            path.join(data_path, "Архив важных срочных задач.csv"))

    not_rush_imp_tasks = Cl_.ListTasks(path.join(data_path, "Важные не срочные задачи.csv"), 
                                                path.join(data_path, "Архив важных не срочных задач.csv"))

    rush_not_imp_tasks = Cl_.ListTasks(path.join(data_path, "Не важные срочные задачи.csv"), 
                                                path.join(data_path, "Архив не важных срочных задач.csv"))

    not_rush_not_imp_tasks = Cl_.ListTasks(path.join(data_path, "Не важные не срочные задачи.csv"), 
                                                    path.join(data_path, "Архив не важных не срочных задач.csv"))

    settings_obj = Cl_.Settings(path.join(data_path, "Настройки.csv"))

    #Настройки:
    if settings_obj.get_("imp_flag") is None:  
        settings_obj.set_("imp_flag", "1")
        settings_obj.set_("rest_flag", "0")
        settings_obj.set_("task_cycle", "1")
        settings_obj.set_("curr_task_type", "")
    
    #Переменные:
    current_task_type = settings_obj.get_("curr_task_type")
    current_task = ""
    #Загрузка текущей задачи
    if current_task_type == "r_i": current_task = rush_imp_tasks.get_task_stack()
    elif current_task_type == "nr_i": current_task = not_rush_imp_tasks.get_task_queue()
    elif current_task_type == "r_ni": current_task = rush_not_imp_tasks.get_all_tasks_stack("Придумать как оптимизировать эти задачи:")
    elif current_task_type == "nr_ni": current_task = not_rush_not_imp_tasks.get_all_tasks_queue("Придумать как перепоручить эти задачи:")
    elif current_task_type == "rest": current_task = "Поесть и отдохнуть 30 минут =)"

    while True:
        #Определение текущей задачи
        if current_task == "":
            for n in range(4):
                # Задача "rest"
                if settings_obj.get_("rest_flag") == "1":
                    current_task = "Поесть и отдохнуть 30 минут =)"
                    current_task_type = "rest"
                    settings_obj.set_("curr_task_type", current_task_type)
                # Задача "r_i"
                if settings_obj.get_("imp_flag") == "1" and rush_imp_tasks.get_task_stack() != "" and current_task == "":
                    current_task = rush_imp_tasks.get_task_stack()
                    current_task_type = "r_i"
                    settings_obj.set_("curr_task_type", current_task_type)
                # Задача "nr_i"
                if settings_obj.get_("task_cycle") == "1" and not_rush_imp_tasks.get_task_queue() != "" and current_task == "":
                    current_task = not_rush_imp_tasks.get_task_queue()
                    current_task_type = "nr_i"
                    settings_obj.set_("curr_task_type", current_task_type)
                # Задача "r_ni" 
                if settings_obj.get_("task_cycle") == "2" and rush_not_imp_tasks.get_task_stack() != "" and current_task == "":
                    current_task = rush_not_imp_tasks.get_all_tasks_stack("Придумать как оптимизировать эти задачи:")
                    current_task_type = "r_ni"
                    settings_obj.set_("curr_task_type", current_task_type)
                # Задача "nr_ni"
                if settings_obj.get_("task_cycle") == "3" and not_rush_not_imp_tasks.get_task_queue() != "" and current_task == "":
                    current_task = not_rush_not_imp_tasks.get_all_tasks_queue("Придумать как перепоручить эти задачи:")
                    current_task_type = "nr_ni"
                    settings_obj.set_("curr_task_type", current_task_type)
                
                # Напечатаем приветствие новой задаче
                if current_task != "": 
                    Int_m.show_new_task(current_task)  
                    break
                elif rush_imp_tasks.get_task_stack() != "": settings_obj.set_("imp_flag", "1")
                elif not_rush_imp_tasks.get_task_queue() != "": settings_obj.set_("task_cycle", "1")
                elif rush_not_imp_tasks.get_task_stack() != "": settings_obj.set_("task_cycle", "2")
                elif not_rush_not_imp_tasks.get_task_queue() != "": settings_obj.set_("task_cycle", "3")  
            
        #Запуск интерфейса
        match Int_m.main_interface(current_task):
            case "1": # Выполнить текущую задачу
                match current_task_type:
                    case "rest": 
                        settings_obj.set_("rest_flag", "0")
                        current_task = ""   
                        current_task_type = ""
                        settings_obj.set_("curr_task_type", "")
                    case "r_i":
                        if Int_m.task_done() in ["1", "2"]: 
                            rush_imp_tasks.remove_task_stack()
                            current_task = ""   
                            current_task_type = ""
                            settings_obj.set_("imp_flag", "0")
                            settings_obj.set_("rest_flag", "1")
                            settings_obj.set_("curr_task_type", "")
                    case "nr_i": 
                        if Int_m.task_done() in ["1", "2"]:
                            not_rush_imp_tasks.remove_task_queue()
                            current_task = ""   
                            current_task_type = ""
                            settings_obj.set_("imp_flag", "1")
                            settings_obj.set_("task_cycle", "2")
                            settings_obj.set_("rest_flag", "1")
                            settings_obj.set_("curr_task_type", "")
                    case "r_ni":
                        if Int_m.task_done() in ["1", "2"]:
                            not_rush_imp_tasks.remove_all_tasks()
                            current_task = ""   
                            current_task_type = ""
                            settings_obj.set_("imp_flag", "1")
                            settings_obj.set_("task_cycle", "3")
                            settings_obj.set_("rest_flag", "1")
                            settings_obj.set_("curr_task_type", "")
                    case "nr_ni":      
                        if Int_m.task_done() in ["1", "2"]:
                            not_rush_not_imp_tasks.remove_all_tasks()
                            current_task = ""   
                            current_task_type = ""
                            settings_obj.set_("imp_flag", "1")
                            settings_obj.set_("task_cycle", "1")
                            settings_obj.set_("rest_flag", "1")
                            settings_obj.set_("curr_task_type", "")
            
            case "2": # Перейти к следующей задаче
                
                if current_task_type != "" and Int_m.next_task() in ["1"]: 
                    match current_task_type:
                        case "r_i":
                            current_task = ""   
                            current_task_type = ""
                            settings_obj.set_("curr_task_type", "")
                            settings_obj.set_("imp_flag", "0")
                        case "nr_i": 
                            current_task = ""   
                            current_task_type = ""
                            settings_obj.set_("task_cycle", "2")
                            settings_obj.set_("curr_task_type", "")
                        case "r_ni":
                            current_task = ""   
                            current_task_type = ""
                            settings_obj.set_("task_cycle", "3")
                            settings_obj.set_("curr_task_type", "")
                        case "nr_ni":      
                            current_task = ""   
                            current_task_type = ""
                            settings_obj.set_("imp_flag", "1")
                            settings_obj.set_("task_cycle", "1")
                            settings_obj.set_("curr_task_type", "")
                        case "rest":
                            current_task = ""   
                            current_task_type = ""
                            settings_obj.set_("rest_flag", "0")
                            settings_obj.set_("curr_task_type", "")
                        
                        
                        
            case "3": # Добавить ещё задачи
                new_task_str = Int_m.input_task()
                match Int_m.add_task():
                    case "1": # Добавить задачу в срочный и важный список
                        rush_imp_tasks.add_task_stack(new_task_str)
                        settings_obj.set_("imp_flag", "1")
                        current_task = ""   
                        current_task_type = ""
                        Int_m.inp_task_ok(new_task_str)
                        
                    case "2": # Добавить задачу в не срочный но важный список
                        not_rush_imp_tasks.add_task_queue(new_task_str)
                        Int_m.inp_task_ok(new_task_str)
                        
                    case "3": # Добавить задачу в срочный но не важный список
                        rush_not_imp_tasks.add_task_stack(new_task_str)
                        Int_m.inp_task_ok(new_task_str)
                        
                    case "4": # Добавить задачу в не срочный и не важный список    
                        not_rush_not_imp_tasks.add_task_queue(new_task_str)
                        Int_m.inp_task_ok(new_task_str)            
                
            case "4": # Вывести список текущих задач
                match current_task_type:
                    case "r_i": 
                        Int_m.task_list(rush_imp_tasks.get_all_tasks_stack(), "Список текущих срочных и важных задач:")
                    case "nr_i": 
                        Int_m.task_list(not_rush_imp_tasks.get_all_tasks_queue(), "Список текущих не срочных но важных задач:")
                    case "r_ni":
                        Int_m.task_list(rush_not_imp_tasks.get_all_tasks_stack(), "Список текущих срочных но не важных задач:")
                    case "nr_ni":      
                        Int_m.task_list(not_rush_not_imp_tasks.get_all_tasks_queue(), "Список текущих не срочных и не важных задач:")
                
            case "5": # Вывести список архивных задач
                match current_task_type:
                    case "r_i": 
                        Int_m.task_list(rush_imp_tasks.get_all_completed_tasks(), "Список архивных срочных и важных задач:")
                    case "nr_i": 
                        Int_m.task_list(not_rush_imp_tasks.get_all_completed_tasks(), "Список архивных не срочных но важных задач:")
                    case "r_ni":
                        Int_m.task_list(rush_not_imp_tasks.get_all_completed_tasks(), "Список архивных срочных но не важных задач:")
                    case "nr_ni":      
                        Int_m.task_list(not_rush_not_imp_tasks.get_all_completed_tasks(), "Список архивных не срочных и не важных задач:")
                
                
except ValueError as err:   # Обработка всех остальных ошибок:  
        lm.print_logs(f"ValueError {err}")
        exit() 
except TypeError as err:   
        lm.print_logs(f"TypeError {err}")
        exit() 
except IndexError as err:  
        lm.print_logs(f"IndexError {err}") 
        exit() 
except KeyError as err:  
       lm.print_logs(f"KeyError {err}")
       exit() 
except AttributeError as err:  
       lm.print_logs(f"AttributeError {err}")
       exit() 









