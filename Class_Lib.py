# В данном модуле реализована концепция "безопасного программирования", где у программиста-пользователя
# есть доступ к данным только через специальные методы класса, а не напрямую

# Добавить списку время создания задачи и завершения и тип завершения, 
# поправить генерацию вывода списков с пометками "тип", "задача"
# поправить генерацию вывода архивов с пометками "тип", "задача", "создана", "завершена", "тип завершения"
# Добавить шифрование данных (настроек и базы данных введенным паролем, 
# а введенный пароль шифровать случайным паролем на каждый запуск программы)

#Класс для хранения списков задач
class ListTasks:
    #Конструктор класса
    def __init__(self, file_tasks:str, file_completed_tasks:str):
        #Загрузка списков задач из файлов
        self.__tasks:list = list(self.__func_data_list(file_tasks)) 
        self.__completed_tasks:list = list(self.__func_data_list(file_completed_tasks)) #Список выполненных задач
        self.__file_tasks:str = file_tasks #Файл для хранения списка задач
        self.__file_completed_tasks:str = file_completed_tasks #Файл для хранения списка выполненных задач
        
    # -----------------------------------------------------------------------------------------
    # Функция func_data_list - создает/добавляет/перезаписывает/считывает список базы данных стека или очереди,
    # Входные параметры:
    # filename_dl - название/путь к файлу списка
    # in_list_dl - список имён для записи
    # del_bl - флаг замены старого списка новыми данными
    # -----------------------------------------------------------------------------------------
    # Функция для создания базы данных - последовательный список для работы со стеком или очередью
    def __func_data_list(self, filename_dl: str, in_list_dl: tuple = (), del_dl: bool = False):
        # Открытие или создание файла если его нет для чтения
        in_list_dl = tuple(str(i1) for i1 in in_list_dl)  # Принудительное преобразование ссылок и строк в кортеж
        f_list_dl: list = []
        try:
            if not del_dl:
                with open(filename_dl, "a+") as file_dl:
                    file_dl.seek(0)  # Перевод указателя в начало файла
                    text1 = file_dl.read()
                    
                    # Считывание данных из файла с разбиением на строки
                    if text1: # Проверка на пустоту файла
                        f_list_dl = text1.splitlines()
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
                      
                      
                      
                      
                      
                      
                      
    #Метод для добавления задачи в список задач, стек
    def add_task_stack(self, task:str):
        self.__tasks.append(task) 
        self.__func_data_list(self.__file_tasks, tuple(self.__tasks), True)
        return self.__tasks[-1]
        
    #Метод для извлечения задачи из списка задач, стек
    def get_task_stack(self):
        if self.__tasks:
            return self.__tasks[-1]
        else:
            return ""
        
    #Метод для удаления задачи из списка задач, стек
    def remove_task_stack(self):
        if self.__tasks:
            r1 = self.__tasks.pop() 
            self.__func_data_list(self.__file_tasks, tuple(self.__tasks), True)
            self.add_completed_task(r1) # Добавление задачи в архив
            return r1 
        else: 
            return ""
        
      #Метод для извлечения всего списка задач стек в виде строки
    def get_all_tasks_stack(self, prefix: str = ""):
        if self.__tasks:
            _stack = self.__tasks.copy()  # Создаем копию списка
            _stack.reverse()  # Разворачиваем копию
            _stack = [f"{i + 1}. {task}" for i, task in enumerate(_stack)]  # Добавляем нумерацию
            if prefix != "": _stack.insert(0, prefix) # Добавляем префикс
            return str("\n".join(_stack))  # Возврат соединенной строки
        else:
            return ""
        
      
            
            
            
            
            
            
            
            
    #Метод для добавления задачи в список задач, очередь
    def add_task_queue(self, task: str):
        self.__tasks.append(task) 
        self.__func_data_list(self.__file_tasks, tuple(self.__tasks), True)
        return self.__tasks[-1]
        
    #Метод для извлечения задачи из списка задач, очередь
    def get_task_queue(self):
        if self.__tasks:
            return self.__tasks[0] 
        else:
            return ""
    
    #Метод для удаления задачи из списка задач, очередь
    def remove_task_queue(self):
        if self.__tasks: 
            r1 = self.__tasks.pop(0) 
            self.__func_data_list(self.__file_completed_tasks, tuple(self.__tasks), True)
            self.add_completed_task(r1) # Добавление задачи в архив
            # Обновление переменной архива
            
            return r1
        else:
            return ""
        
    #Метод для извлечения всего списка задач очередь в виде строки
    def get_all_tasks_queue(self, prefix: str = ""):
        if self.__tasks:
            _queue = [f"{i + 1}. {task}" for i, task in enumerate(self.__tasks)]  # Добавляем нумерацию
            if prefix != "": _queue.insert(0, prefix) # Добавляем префикс
            return "\n".join(_queue)
        else:
            return ""
            
            
            
       
    #Метод для перемещения всех задач в архив
    def remove_all_tasks(self):
        self.__completed_tasks.extend(self.__tasks) # Добавление задач в архив
        self.__func_data_list(self.__file_completed_tasks, tuple(self.__tasks)) # Сохранение архива
        self.__tasks.clear()    

            
            
            
    #Метод для добавления задачи в список выполненных задач
    def add_completed_task(self, task: str):
        self.__completed_tasks.append(task) 
        self.__func_data_list(self.__file_completed_tasks, (task,))
        return self.__completed_tasks[-1]
        
    #Метод для извлечения всего списка выполненных задач в виде строки
    def get_all_completed_tasks(self):
        if self.__completed_tasks:
            _comp_tasks = self.__completed_tasks.copy()
            _comp_tasks.reverse()
            return "\n".join(_comp_tasks) # Возврат списка выполненных задач от последнего к первому
        else:
            return ""
        
        
        
        
        
        
        
        
        
        
        
#Класс для хранения настроек программы
class Settings:
    #Конструктор класса Settings
    def __init__(self, file_settings: str):
        self.__settings: dict = dict()  #Словарь для хранения настроек программы
        self.__file_settings: str = file_settings  #Путь к файлу настроек
        self.__settings = self.__func_data_dict()  #Считывание настроек из файла
            
    
    # -----------------------------------------------------------------------------------------
    # Функция func_data_dict - создает/перезаписывает/считывает список настроек в виде словаря "ключ-значение",
    # Входные параметры:
    # filename_dl - название/путь к файлу списка
    # in_list_dl - список значений для записи
    # del_bl - флаг стирания старого списка
    # -----------------------------------------------------------------------------------------
    # Функция для создания базы данных - словарь "ключ-значение" для работы с настройками
    def __func_data_dict(self, in_list_dd: dict = dict(), del_dd: bool = False):
        # Открытие или создание файла если его нет для чтения
        f_dict_dd: dict = dict()
        try:
            if not del_dd:
                with open(self.__file_settings, "a+") as file_dd:
                    file_dd.seek(0)  # Перевод указателя в начало файла
                    text1: str = file_dd.read()
                    
                    # Считывание данных из файла с разбиением на строки
                    if text1: # Проверка на пустоту файла
                        f_dict_dd_list = text1.splitlines()
                        f_dict_dd = {x.split(";")[0]: x.split(";")[1] for x in f_dict_dd_list }
                    
                # Автозакрытие файла
            
            # Если файл пуст и нет данных для записи, то возврат пустого списка
            if not text1 and not in_list_dd:
                return f_dict_dd
                
            # Возврат списка настроек из файла
            if not in_list_dd and not del_dd:
                return f_dict_dd
            

            if del_dd:  # Проверка флага стирания старых имен
                f_dict_dd = dict(in_list_dd)  # Замена данных в старом словаре на новые
            else:
                f_dict_dd.update(in_list_dd)  # Добавление новых данных в старый словарь
          
            
            # Открытие или создание файла если его нет для перезаписи
            with open(self.__file_settings, "w") as file_dd:
                # Объединение словаря в строку с добавлением символа начала новой строки
                #  и запись данных в файл
                if f_dict_dd: 
                    file_dd.write("\n".join([x + ";" + f_dict_dd[x] for x in f_dict_dd.keys()]))  # Запись обновленного списка
                # Автозакрытие файла
            
        except OSError:
            print("Ошибка файловой операции")
            return ("Error")
            
        return f_dict_dd
    # --End func data_list  
    
    #Функция для записи новых настроек и изменения старых
    def set_(self, param_set, value_set):
        self.__settings[param_set] = value_set 
        self.__func_data_dict(self.__settings)
        return True
    
    #Функция для получения настройки программы
    def get_(self, param_get):
        return self.__settings.get(param_get)
    
        
        



