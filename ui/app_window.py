# ui/app_window.py
import customtkinter as ctk

# Импорт компонентов из папки components
from ui.components.input_frame import InputFrame
from ui.components.active_item import ActiveTaskItem  # Новое имя
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

        # Настройки окна
        self.title("My TODO Project v1.6 [OOP Edition]")
        self.geometry("800x850")
        
        # Переменная для живого поиска
        self.current_search = ""

        # 1. ПОИСК (над всеми вкладками)
        self.search_bar = SearchFrame(self, on_search=self.update_search)
        self.search_bar.pack(pady=10, padx=20, fill="x")

        # 2. СИСТЕМА ВКЛАДОК
        self.tabview = ctk.CTkTabview(self, width=580)
        self.tabview.pack(pady=5, padx=10, fill="both", expand=True)

        self.tab_active = self.tabview.add("Активные")
        self.tab_archive = self.tabview.add("Архив")
        self.tab_calendar = self.tabview.add("Календарь")

        # 3. КАЛЕНДАРЬ
        self.calendar_view = CalendarFrame(self.tab_calendar)
        self.calendar_view.pack(pady=20, padx=20, fill="both", expand=True)

        # 4. ВКЛАДКА "АКТИВНЫЕ"
        self.input_area = InputFrame(
            self.tab_active, 
            on_add=self.add_logic, 
            calendar_component=self.calendar_view
        )
        self.input_area.pack(pady=10)

        self.scroll_active = ctk.CTkScrollableFrame(self.tab_active, height=450)
        self.scroll_active.pack(pady=10, fill="both", expand=True)

        # 5. ВКЛАДКА "АРХИВ"
        self.scroll_archive = ctk.CTkScrollableFrame(self.tab_archive, height=650)
        self.scroll_archive.pack(pady=10, fill="both", expand=True)

        # Первичная отрисовка
        self.after(200, self.refresh_list)

    # --- МЕТОДЫ ПОИСКА И ЛОГИКИ ---

    def update_search(self, query):
        self.current_search = query.lower()
        self.refresh_list()

    def add_logic(self, title, desc, deadline, priority):
        add_task(title, desc, deadline, priority)
        save_all()
        self.refresh_list()

    def done_logic(self, n):
        if mark_as_done(n):
            save_all()
            self.refresh_list()

    def delete_logic(self, n):
        if move_to_trash(n):
            save_all()
            self.refresh_list()

    # --- ГЛАВНЫЙ МЕТОД ОТРИСОВКИ ---

    def refresh_list(self):
        # Очистка
        for widget in self.scroll_active.winfo_children(): widget.destroy()
        for widget in self.scroll_archive.winfo_children(): widget.destroy()

        # 1. Фильтрация и отрисовка АКТИВНЫХ
        filtered_active = [
            t for t in active_tasks 
            if self.current_search in t['title'].lower() or self.current_search in t['description'].lower()
        ]
        
        for task in reversed (filtered_active):
            # Находим реальный индекс для функций DONE/DELETE
            real_idx = active_tasks.index(task) + 1
            # Используем НОВЫЙ класс-наследник
            ActiveTaskItem(
                self.scroll_active, 
                task, 
                real_idx, 
                self.done_logic, 
                self.delete_logic
            ).pack(fill="x", pady=5, padx=5)

        # 2. Фильтрация и отрисовка АРХИВА
        filtered_archive = [
            t for t in archived_tasks 
            if self.current_search in t['title'].lower() or self.current_search in t['description'].lower()
        ]
        
        for task in reversed(filtered_archive):
            # Используем класс-наследник для архива
            ArchiveItem(self.scroll_archive, task).pack(fill="x", pady=2, padx=5)

if __name__ == "__main__":
    app = TodoApp()
    app.mainloop()