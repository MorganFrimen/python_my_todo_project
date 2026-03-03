import customtkinter as ctk

class BaseTaskItem(ctk.CTkFrame):
    def __init__(self, master, task):
        # Светлый "бумажный" стиль
        super().__init__(
            master, 
            corner_radius=16,
            fg_color="#F9F8F6",
            border_width=2,
            border_color="#E0DDD5"
        )
        self.task = task
        self.is_done = task.get('status') == "Выполнено"

        # 1. Индикатор приоритета
        colors = {"Высокий": "#E74C3C", "Средний": "#F1C40F", "Низкий": "#2ECC71"}
        p_color = colors.get(task.get('priority'), "#555555")
        
        self.marker = ctk.CTkFrame(self, width=5, corner_radius=10, fg_color=p_color)
        self.marker.pack(side="left", fill="y", padx=(12, 0), pady=12)

        # 2. Контейнер текста
        self.text_cont = ctk.CTkFrame(self, fg_color="transparent")
        self.text_cont.pack(side="left", fill="both", expand=True, padx=15, pady=10)

        t_color = "#2C2C2C" if not self.is_done else "#888888"
        
        self.title_lbl = ctk.CTkLabel(self.text_cont, text=task['title'], 
                                     font=("Segoe UI", 15, "bold"), text_color=t_color, anchor="w")
        self.title_lbl.pack(fill="x")
        
        self.desc_lbl = ctk.CTkLabel(self.text_cont, text=task['description'], 
                                    font=("Segoe UI", 12), text_color="#636363", anchor="w")
        self.desc_lbl.pack(fill="x")

        # --- КОРРЕКТНЫЙ ХОВЕР ---
        self.setup_hover_events()

    def setup_hover_events(self):
        # Список всех элементов, которые должны реагировать
        widgets = [self, self.text_cont, self.title_lbl, self.desc_lbl, self.marker]
        
        for w in widgets:
            w.bind("<Enter>", self.on_hover)
            w.bind("<Leave>", self.on_leave)

    def on_hover(self, event=None):
        self.configure(border_color="#BDBBB0", fg_color="#FFFFFF")

    def on_leave(self, event=None):
        self.configure(border_color="#E0DDD5", fg_color="#F9F8F6")