import tkinter as tk
from tkinter import messagebox, ttk
import random
import json
import os

# --- Константы ---
# Имя файла для сохранения полного списка задач (с типами), чтобы можно было расширять
TASKS_DATA_FILE = "tasks_data.json"
# Имя файла для сохранения истории сгенерированных задач
TASK_HISTORY_FILE = "task_history.json"

# Начальный список задач. Если файл TASKS_DATA_FILE не существует, используется этот.
# Каждая задача - это словарь с ключами 'task' (строка) и 'type' (строка).
INITIAL_TASKS_DATA = [
    {"task": "Прочитать статью по основам Python", "type": "Учёба"},
    {"task": "Сделать 15-минутную зарядку", "type": "Спорт"},
    {"task": "Ответить на три самых важных рабочих письма", "type": "Работа"},
    {"task": "Послушать эпизод образовательного подкаста", "type": "Учёба"},
    {"task": "Прогуляться на свежем воздухе 30 минут", "type": "Спорт"},
    {"task": "Написать план на следующий рабочий день", "type": "Работа"},
    {"task": "Изучить новый дизайн-паттерн", "type": "Учёба"},
    {"task": "Выполнить комплекс силовых упражнений", "type": "Спорт"},
    {"task": "Подготовить черновик отчета", "type": "Работа"},
    {"task": "Повторить основные концепции ООП", "type": "Учёба"},
    {"task": "Сделать растяжку после долгого сидения", "type": "Спорт"},
    {"task": "Организовать файлы на рабочем столе", "type": "Работа"},
    {"task": "Написать короткое эссе на заданную тему", "type": "Учёба"},
    {"task": "Посетить спортзал", "type": "Спорт"},
    {"task": "Запланировать рабочую встречу", "type": "Работа"},
    {"task": "Решить 5 задач по алгоритмам", "type": "Учёба"},
    {"task": "Утренняя пробежка", "type": "Спорт"},
    {"task": "Провести рефакторинг одного модуля кода", "type": "Работа"},
]

class RandomTaskGeneratorApp:
    def __init__(self, root):
        """Инициализация приложения."""
        self.root = root
        self.root.title("Random Task Generator")
        self.root.geometry("550x650") # Размер окна

        self.all_tasks_data = []      # Полный список всех доступных задач (с типами)
        self.task_history = []        # История сгенерированных задач
        self.filtered_task_pool = []  # Задачи, доступные для генерации после фильтрации
        self.task_types = []          # Список доступных типов задач для фильтрации
        self.selected_type = tk.StringVar() # Выбранный тип для фильтрации

        self.load_all_tasks_data()     # Загрузка данных задач
        self.load_task_history()       # Загрузка истории
        self.update_task_pool_and_filters() # Обновляем пул задач и устанавливаем фильтры

        self.create_widgets()          # Создание виджетов GUI

        self.refresh_history_display() # Отображение истории при запуске

    def load_all_tasks_data(self):
        """
        Загружает список всех доступных задач (с типами) из TASKS_DATA_FILE.
        Если файл не найден или имеет некорректный формат, использует INITIAL_TASKS_DATA.
        """
        if os.path.exists(TASKS_DATA_FILE):
            try:
                with open(TASKS_DATA_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # Проверка корректности структуры: список словарей с 'task' и 'type'
                    if isinstance(data, list) and all(isinstance(item, dict) and 'task' in item and 'type' in item for item in data):
                        self.all_tasks_data = data
                    else:
                        print(f"Предупреждение: Некорректный формат файла '{TASKS_DATA_FILE}'. Используются начальные задачи.")
                        self.all_tasks_data = INITIAL_TASKS_DATA
                        self.save_all_tasks_data() # Сохраняем правильный формат, чтобы избежать повторных предупреждений
            except (json.JSONDecodeError, IOError) as e:
                print(f"Ошибка при загрузке задач из '{TASKS_DATA_FILE}': {e}. Используются начальные задачи.")
                self.all_tasks_data = INITIAL_TASKS_DATA
                self.save_all_tasks_data()
        else:
            # Если файл не существует, используем начальные данные и сохраняем их.
            self.all_tasks_data = INITIAL_TASKS_DATA
            self.save_all_tasks_data()

    def save_all_tasks_data(self):
        """
        Сохраняет текущий список всех доступных задач (с типами) в TASKS_DATA_FILE.
        """
        try:
            with open(TASKS_DATA_FILE, 'w', encoding='utf-8') as f:
                # ensure_ascii=False для корректного отображения русских букв
                json.dump(self.all_tasks_data, f, indent=4, ensure_ascii=False)
        except IOError as e:
            print(f"Ошибка при сохранении данных задач: {e}")
            messagebox.showerror("Ошибка сохранения", f"Не удалось сохранить список доступных задач: {e}")

    def load_task_history(self):
        """
        Загружает историю сгенерированных задач из TASK_HISTORY_FILE.
        """
        if os.path.exists(TASK_HISTORY_FILE):
            try:
                with open(TASK_HISTORY_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # Проверка корректности структуры: список строк
                    if isinstance(data, list) and all(isinstance(item, str) for item in data):
                        self.task_history = data
                    else:
                        print(f"Предупреждение: Некорректный формат файла '{TASK_HISTORY_FILE}'. История будет пустой.")
                        self.task_history = []
            except (json.JSONDecodeError, IOError) as e:
                print(f"Ошибка при загрузке истории задач из '{TASK_HISTORY_FILE}': {e}. История будет пустой.")
                self.task_history = []
        else:
            self.task_history = [] # Если файла нет, история пуста

    def save_task_history(self):
        """
        Сохраняет текущую историю сгенерированных задач в TASK_HISTORY_FILE.
        """
        try:
            with open(TASK_HISTORY_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.task_history, f, indent=4, ensure_ascii=False)
        except IOError as e:
            print(f"Ошибка при сохранении истории задач: {e}")
            messagebox.showerror("Ошибка сохранения", f"Не удалось сохранить историю задач: {e}")

    def update_task_pool_and_filters(self):
        """
        Обновляет список доступных типов задач для фильтрации и формирует текущий пул задач.
        """
        # Получаем все уникальные типы задач из полного списка
        unique_types = sorted(list(set(task['type'] for task in self.all_tasks_data)))
        self.task_types = ["Все"] + unique_types # Добавляем опцию "Все"

        # Обновляем значения для выпадающего списка фильтров
        if hasattr(self, 'filter_combobox'): # Проверяем, существует ли уже виджет
            self.filter_combobox['values'] = self.task_types
            # Сбрасываем выбор фильтра на "Все", если он больше не актуален (например, если тип был удален)
            if self.selected_type.get() not in self.task_types:
                self.selected_type.set("Все")

        self.apply_filter() # Применяем текущий фильтр для установки filtered_task_pool

    def apply_filter(self, event=None):
        """
        Применяет выбранный тип задачи для фильтрации общего пула задач.
        Обновляет self.filtered_task_pool.
        """
        current_filter_type = self.selected_type.get()

        if current_filter_type == "Все":
            self.filtered_task_pool = self.all_tasks_data
        else:
            self.filtered_task_pool = [
                task for task in self.all_tasks_data if task['type'] == current_filter_type
            ]

        # Если после фильтрации не осталось задач, сообщаем пользователю и сбрасываем фильтр.
        if not self.filtered_task_pool:
            messagebox.showwarning("Нет задач", f"По выбранному типу '{current_filter_type}' нет задач.")
            self.selected_type.set("Все") # Сбрасываем на "Все"
            self.filtered_task_pool = self.all_tasks_data # Возвращаем полный пул

    def generate_task(self):
        """
        Выбирает случайную задачу из отфильтрованного пула,
        добавляет её в историю и обновляет отображение.
        """
        if not self.filtered_task_pool:
            messagebox.showinfo("Нет задач", "В текущем наборе нет доступных задач для генерации.")
            return

        # Выбираем случайную задачу из отфильтрованного пула
        selected_task_dict = random.choice(self.filtered_task_pool)
        selected_task_string = f"[{selected_task_dict['type']}] {selected_task_dict['task']}"

        # Добавляем задачу в историю
        self.task_history.append(selected_task_string)

        # Обновляем историю в файле
        self.save_task_history()

        # Обновляем отображение истории в Listbox
        self.refresh_history_display()

        # Показываем пользователю сгенерированную задачу (можно в отдельном окне или метке)
        messagebox.showinfo("Ваша задача:", selected_task_string)

    def refresh_history_display(self):
        """
        Очищает и перезаполняет Listbox с историей задач.
        """
        # Очищаем текущее содержимое Listbox
        self.history_listbox.delete(0, tk.END)
        # Добавляем задачи из истории, начиная с самой новой (с конца массива)
        for task_str in reversed(self.task_history):
            self.history_listbox.insert(tk.END, task_str)

    def create_widgets(self):
        """Создает все элементы графического интерфейса."""

        # --- Фрейм для настройки фильтров ---
        filter_frame = tk.Frame(self.root, padx=10, pady=10, relief=tk.GROOVE, borderwidth=2)
        filter_frame.pack(fill=tk.X, padx=10, pady=5)

        tk.Label(filter_frame, text="Фильтр по типу:", font=("Arial", 10)).grid(row=0, column=0, sticky="w", padx=5, pady=5)

        self.selected_type.set("Все") # Значение по умолчанию

        self.filter_combobox = ttk.Combobox(
            filter_frame,
            textvariable=self.selected_type,
            values=self.task_types,
            state="readonly", # Пользователь не может вводить текст, только выбирать
            width=20
        )
        self.filter_combobox.grid(row=0, column=1, padx=5, pady=5)
        self.filter_combobox.bind("<<ComboboxSelected>>", self.apply_filter) # Событие при выборе элемента

        self.generate_button = tk.Button(
            filter_frame,
            text="Сгенерировать задачу",
            command=self.generate_task,
            bg="#4CAF50", # Зеленый цвет
            fg="white",
            font=("Arial", 10, "bold"),
            relief=tk.RAISED,
            bd=2
        )
        self.generate_button.grid(row=0, column=2, padx=15, pady=5)


        # --- Фрейм для отображения истории ---
        history_frame = tk.Frame(self.root, padx=10, pady=10, relief=tk.GROOVE, borderwidth=2)
        history_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        tk.Label(history_frame, text="История сгенерированных задач:", font=("Arial", 12, "bold")).pack(pady=5)

        # Создаем Scrollbar для Listbox
        self.scrollbar = tk.Scrollbar(history_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.history_listbox = tk.Listbox(
            history_frame,
            height=20, # Высота списка
            font=("Arial", 10),
            yscrollcommand=self.scrollbar.set # Привязываем скроллбар
        )
        self.history_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.scrollbar.config(command=self.history_listbox.yview) # Настраиваем скроллбар

# --- Точка входа в приложение ---
if __name__ == "__main__":
    root = tk.Tk()
    app = RandomTaskGeneratorApp(root)
    root.mainloop()
