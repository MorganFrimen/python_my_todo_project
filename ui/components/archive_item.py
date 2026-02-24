from ui.components.base.base_item import BaseTaskItem
import customtkinter as ctk

class ArchiveItem(BaseTaskItem): # Наследуемся!
    def __init__(self, master, task):
        super().__init__(master, task)
        
        # Специфика архива: только текст даты удаления справа
        self.title_lbl.configure(text=f"📂 {task['title']}") # Немного меняем заголовок
        
        ctk.CTkLabel(self, text=f"🗑️ {task.get('deleted_at', '-')}", 
                     font=("Arial", 10), text_color="gray").pack(side="right", padx=10)