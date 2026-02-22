import customtkinter as ctk

class ArchiveItem(ctk.CTkFrame):
    def __init__(self, master, task):
        super().__init__(master)
        
        # Контейнер для текста
        self.text_cont = ctk.CTkFrame(self, fg_color="transparent")
        self.text_cont.pack(side="left", padx=10, pady=5, fill="both", expand=True)

        # Заголовок (Название)
        ctk.CTkLabel(self.text_cont, text=f"📂 {task['title']}", 
                     font=("Arial", 13, "bold"), anchor="w").pack(fill="x")
        
        # Описание (на второй строке)
        ctk.CTkLabel(self.text_cont, text=task['description'], 
                     font=("Arial", 11), text_color="gray", anchor="w").pack(fill="x")

        # Дата удаления (справа)
        ctk.CTkLabel(self, text=f"🗑️ {task.get('deleted_at', '—')}", 
                     font=("Arial", 10), text_color="#555555").pack(side="right", padx=10)