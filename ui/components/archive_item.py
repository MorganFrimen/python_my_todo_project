from ui.components.base.base_item import BaseTaskItem
import customtkinter as ctk

class ArchiveItem(BaseTaskItem):
    def __init__(self, master, task):
        super().__init__(master, task)
        
        # Получаем статус завершения
        comp_status = task.get('completion_status', 'Удалено')
        
        # Цвета для разных статусов в архиве
        status_colors = {
            "Вовремя": "#2ECC71",      # Зеленый
            "С опозданием": "#E67E22", # Оранжевый
            "Удалено": "#95A5A6"       # Серый
        }
        s_color = status_colors.get(comp_status, "gray")

        # Добавляем метку статуса под описанием
        self.status_lbl = ctk.CTkLabel(
            self.text_cont, 
            text=f"📊 Статус: {comp_status}", 
            font=("Arial", 10, "bold"), 
            text_color=s_color,
            anchor="w"
        )
        self.status_lbl.pack(fill="x")

        # Дата удаления/завершения справа
        ctk.CTkLabel(self, text=f"⏱ {task.get('deleted_at', '-')}", 
                     font=("Arial", 10), text_color="gray").pack(side="right", padx=10)