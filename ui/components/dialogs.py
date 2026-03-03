import customtkinter as ctk

class ConfirmDialog(ctk.CTkToplevel):
    def __init__(self, master, title, message, on_confirm):
        super().__init__(master)
        
        self.title(title)
        self.geometry("350x180")
        self.on_confirm = on_confirm

        # Поверх всех окон
        self.attributes("-topmost", True)
        self.grab_set() # Блокирует основное окно, пока не ответим

        # Текст вопроса
        self.label = ctk.CTkLabel(self, text=message, wraplength=300, font=("Arial", 14))
        self.label.pack(pady=30, padx=20)

        # Контейнер для кнопок
        self.btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.btn_frame.pack(pady=10)

        # Кнопка "Да"
        self.yes_btn = ctk.CTkButton(self.btn_frame, text="Да", width=100, 
                                     fg_color="#E74C3C", hover_color="#C0392B",
                                     command=self.confirm)
        self.yes_btn.pack(side="left", padx=10)

        # Кнопка "Отмена"
        self.no_btn = ctk.CTkButton(self.btn_frame, text="Отмена", width=100, 
                                    fg_color="gray", command=self.destroy)
        self.no_btn.pack(side="left", padx=10)

    def confirm(self):
        self.on_confirm() # Выполняем переданную функцию
        self.destroy()    # Закрываем окно