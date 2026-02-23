import customtkinter as ctk

class SearchFrame(ctk.CTkFrame):
    def __init__(self, master, on_search):
        super().__init__(master, fg_color="transparent")
        self.on_search = on_search

        # Поле ввода поиска
        self.entry = ctk.CTkEntry(
            self, 
            placeholder_text="🔍 Быстрый поиск по названию или описанию...", 
            width=400
        )
        self.entry.pack(side="left", padx=10, fill="x", expand=True)
        
        # Привязываем событие отпускания клавиши (KeyRelease)
        self.entry.bind("<KeyRelease>", lambda e: self.on_search(self.entry.get()))

        # Кнопка очистки
        self.clear_btn = ctk.CTkButton(
            self, text="✖", width=30, 
            fg_color="transparent", text_color="gray",
            command=self.clear_search
        )
        self.clear_btn.pack(side="right")

    def clear_search(self):
        self.entry.delete(0, 'end')
        self.on_search("") # Сбрасываем фильтр