# ui/app_window.py
import customtkinter as ctk

# Импорт компонентов
from ui.components.input_frame import InputFrame
from ui.components.task_item import TaskItem
from ui.components.calendar_frame import CalendarFrame

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

        # Настройки главного окна
        self.title("My TODO Project v1.1")
        self.geometry("550x750")

        # 1. Создаем систему вкладок (Tabs)
        self.tabview = ctk.CTkTabview(self, width=520)
        self.tabview.pack(pady=10, padx=10, fill="both", expand=True)

        # Добавляем три вкладки
        self.tab_active = self.tabview.add("Активные")
        self.tab_archive = self.tabview.add("Архив задач")
        self.tab_calendar = self.tabview.add("Календарь")

        # 2. Создаем КАЛЕНДАРЬ (сначала его, чтобы передать в ввод)
        # Он живет только на вкладке "Календарь"
        self.calendar_view = CalendarFrame(self.tab_calendar)
        self.calendar_view.pack(pady=20, padx=20, fill="both", expand=True)

        # 3. Создаем ПОЛЕ ВВОДА на вкладке "Активные"
        # Передаем ссылку на календарь, чтобы забирать дату дедлайна
        self.input_area = InputFrame(
            self.tab_active, 
            on_add=self.add_logic, 
            calendar_component=self.calendar_view
        )
        self.input_area.pack(pady=10)

        # 4. Скролл-фреймы для списков
        # Список активных задач
        self.scroll_active = ctk.CTkScrollableFrame(self.tab_active, height=400)
        self.scroll_active.pack(pady=10, fill="both", expand=True)
        
        # Список архива
        self.scroll_archive = ctk.CTkScrollableFrame(self.tab_archive, height=600)
        self.scroll_archive.pack(pady=10, fill="both", expand=True)

        # Первичная отрисовка данных
        self.after(200, self.refresh_list)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def on_closing(self):
        """Метод для чистого выхода"""
        from storage.persistence import save_all
        save_all() # На всякий случай сохраняем всё перед выходом
        self.quit()
        self.destroy()

    def add_logic(self, title, desc, deadline):
        # Передаем ровно 3 аргумента в функцию из functions/add.py
        from functions.add import add_task
        from storage.persistence import save_all
        
        add_task(title, desc, deadline) # Используем deadline, который пришел из параметров
        save_all()
        self.refresh_list()

    def done_logic(self, n):
        """Логика отметки о выполнении"""
        if mark_as_done(n):
            save_all()
            self.refresh_list()

    def delete_logic(self, n):
        """Логика перемещения в архив"""
        if move_to_trash(n):
            save_all()
            self.refresh_list()

    def refresh_list(self):
        """Полная перерисовка всех списков интерфейса"""
        # --- Обновляем Активные задачи ---
        for widget in self.scroll_active.winfo_children():
            widget.destroy()
        
        # Отрисовка активных задач с использованием TaskItem
        for i, task in enumerate(active_tasks, 1):
            item = TaskItem(
                self.scroll_active, 
                task, 
                i, 
                on_done=self.done_logic, 
                on_delete=self.delete_logic
            )
            item.pack(fill="x", pady=5, padx=5)

        # --- Обновляем Архив ---
        for widget in self.scroll_archive.winfo_children():
            widget.destroy()
            
        if not archived_tasks:
            ctk.CTkLabel(self.scroll_archive, text="Архив пуст").pack(pady=20)
        else:
            for task in archived_tasks:
                arch_frame = ctk.CTkFrame(self.scroll_archive)
                arch_frame.pack(fill="x", pady=2, padx=5)

                text_container = ctk.CTkFrame(arch_frame, fg_color="transparent")
                text_container.pack(side="left", padx=10, pady=5, fill="x", expand=True)

                # Название задачи
                ctk.CTkLabel(
                    text_container, 
                    text=f"📂 {task['title']}", 
                    font=("Arial", 13, "bold"), 
                    anchor="w"
                ).pack(fill="x")

                # Описание на новой строке
                ctk.CTkLabel(
                    text_container, 
                    text=task['description'], 
                    font=("Arial", 11), 
                    text_color="gray", 
                    anchor="w"
                ).pack(fill="x")

if __name__ == "__main__":
    # Для теста можно запустить файл напрямую, но лучше через main.py
    app = TodoApp()
    app.mainloop()