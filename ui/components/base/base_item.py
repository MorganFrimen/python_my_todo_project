import customtkinter as ctk

class BaseTaskItem(ctk.CTkFrame):
    def __init__(self, master, task):
        super().__init__(master)
        self.task = task

        self.is_done = task['status'] == "Выполнено"
        self.text_color = "gray" if self.is_done else "white"

        # Общий контейнер для текстов
        self.text_cont = ctk.CTkFrame(self, fg_color="transparent")
        self.text_cont.pack(side="left", padx=10, pady=5, fill="both", expand=True)

        # Заголовок (Название)
        self.title_lbl = ctk.CTkLabel(self.text_cont, text=task['title'], 
                                     font=("Arial", 14, "bold"), anchor="w")
        self.title_lbl.pack(fill="x")
        
        # Описание
        self.desc_lbl = ctk.CTkLabel(self.text_cont, text=task['description'], 
                                    font=("Arial", 12), text_color="gray", anchor="w")
        self.desc_lbl.pack(fill="x")

        status_icon = "✅ " if self.is_done else "⏳ "
        self.title_lbl = ctk.CTkLabel(
            self.text_cont, 
            text=status_icon + task['title'], 
            font=("Arial", 14, "bold"), 
            text_color=self.text_color,
            anchor="w"
        )
        self.title_lbl.pack(fill="x")
        
        # Описание
        self.desc_lbl = ctk.CTkLabel(
            self.text_cont, 
            text=task['description'], 
            font=("Arial", 12), 
            text_color="gray", 
            anchor="w"
        )
        self.desc_lbl.pack(fill="x")