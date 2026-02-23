# ui/app_window.py
import customtkinter as ctk

# Импорт компонентов
from ui.components.input_frame import InputFrame
from ui.components.task_item import TaskItem
from ui.components.archive_item import ArchiveItem
from ui.components.calendar_frame import CalendarFrame
from ui.components.search_frame import SearchFrame

# Импорт логики и данных
from functions.add import add_task
from functions.complete import mark_as_done
from functions.delete import move_to_trash
from storage.tasks_db import active_tasks
from storage.history_tasks import archived_tasks
from storage.persistence import save_all

class TodoApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.current_search = ""

        # Настройки окна
        self.title("My TODO Project v1.4 [Git Edition]")
        self.geometry("800x800")

        self.search_bar = SearchFrame(self, on_search=self.update_search)
        self.search_bar.pack(pady=10, padx=20, fill="x")

        # 1. СИСТЕМА ВКЛАДОК
        self.tabview = ctk.CTkTabview(self, width=580)
        self.tabview.pack(pady=10, padx=10, fill="both", expand=True)

        self.tab_active = self.tabview.add("Активные")
        self.tab_archive = self.tabview.add("Архив")
        self.tab_calendar = self.tabview.add("Календарь")

        # 2. ИНИЦИАЛИЗАЦИЯ КАЛЕНДАРЯ
        # Создаем один раз на его вкладке
        self.calendar_view = CalendarFrame(self.tab_calendar)
        self.calendar_view.pack(pady=20, padx=20, fill="both", expand=True)

        # 3. ВКЛАДКА "АКТИВНЫЕ"
        # Компонент ввода (передаем ссылку на календарь)
        self.input_area = InputFrame(
            self.tab_active, 
            on_add=self.add_logic, 
            calendar_component=self.calendar_view
        )
        self.input_area.pack(pady=10)

        # Скролл-список для активных задач
        self.scroll_active = ctk.CTkScrollableFrame(self.tab_active, height=450)
        self.scroll_active.pack(pady=10, fill="both", expand=True)

        # 4. ВКЛАДКА "АРХИВ"
        # Скролл-список для архива
        self.scroll_archive = ctk.CTkScrollableFrame(self.tab_archive, height=650)
        self.scroll_archive.pack(pady=10, fill="both", expand=True)

        # 5. ПЕРВИЧНАЯ ОТРИСОВКА
        # Используем after, чтобы избежать зависания при первом запуске в VS 2022
        self.after(200, self.refresh_list)

    # --- МЕТОДЫ ЛОГИКИ (СВЯЗКА С ФУНКЦИЯМИ) ---

    # 4. Метод обновления поиска
    def update_search(self, query):
        self.current_search = query.lower() # Сохраняем в нижнем регистре для поиска
        self.refresh_list()

    def add_logic(self, title, desc, deadline):
        """Добавление задачи и сохранение"""
        add_task(title, desc, deadline)
        save_all()
        self.refresh_list()

    def done_logic(self, n):
        """Выполнение задачи и сохранение"""
        if mark_as_done(n):
            save_all()
            self.refresh_list()

    def delete_logic(self, n):
        """Удаление в архив и сохранение"""
        if move_to_trash(n):
            save_all()
            self.refresh_list()

    # --- МЕТОД ОТРИСОВКИ ИНТЕРФЕЙСА ---

    def refresh_list(self):
        """Полная перерисовка списков на основе данных из storage"""
        
        # 1. Очищаем виджеты на обеих вкладках
        for widget in self.scroll_active.winfo_children(): widget.destroy()
        for widget in self.scroll_archive.winfo_children(): widget.destroy()

        # ФИЛЬТРАЦИЯ АКТИВНЫХ
        filtered_active = [
            t for t in active_tasks 
            if self.current_search in t['title'].lower() or self.current_search in t['description'].lower()
        ]
    
        for i, task in enumerate(filtered_active, 1):
            # Находим реальный индекс в исходном списке для кнопок
            real_idx = active_tasks.index(task) + 1
            Item = TaskItem(self.scroll_active, task, real_idx, self.done_logic, self.delete_logic)
            Item.pack(fill="x", pady=5, padx=5)

        filtered_archive = [
            t for t in archived_tasks 
            if self.current_search in t['title'].lower() or self.current_search in t['description'].lower()
        ]
    
        for task in reversed(filtered_archive):
            ArchiveItem(self.scroll_archive, task).pack(fill="x", pady=2, padx=5)



        # 2. Рисуем АКТИВНЫЕ ЗАДАЧИ (через TaskItem)
        if not active_tasks:
            ctk.CTkLabel(self.scroll_active, text="Список задач пуст 😴", font=("Arial", 14)).pack(pady=20)
        else:
            for i, task in enumerate(active_tasks, 1):
                item = TaskItem(
                    self.scroll_active, 
                    task, 
                    i, 
                    on_done=self.done_logic, 
                    on_delete=self.delete_logic
                )
                item.pack(fill="x", pady=5, padx=5)


        # 3. Рисуем АРХИВ (через ArchiveItem)
        if not archived_tasks:
            ctk.CTkLabel(self.scroll_archive, text="В архиве пока ничего нет 📂", font=("Arial", 14)).pack(pady=20)
        else:
            # Выводим архив (в обратном порядке, чтобы новые удаления были сверху)
            for task in reversed(archived_tasks):
                ArchiveItem(self.scroll_archive, task).pack(fill="x", pady=2, padx=5)

if __name__ == "__main__":
    # Запуск для отладки
    app = TodoApp()
    app.mainloop()