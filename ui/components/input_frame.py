import customtkinter as ctk

class InputFrame(ctk.CTkFrame):
    def __init__(self, master, on_add, calendar_component):
        super().__init__(master, fg_color="transparent")
        
        self.on_add = on_add
        self.calendar = calendar_component

        # 1. Поле названия с "прослушкой" (валидацией)
        self.entry_title = ctk.CTkEntry(self, placeholder_text="Название задачи...", width=300)
        self.entry_title.pack(pady=5)
        # Привязываем событие отпускания клавиши к проверке текста
        self.entry_title.bind("<KeyRelease>", lambda e: self.validate_input())

        # 2. Поле описания
        self.entry_desc = ctk.CTkEntry(self, placeholder_text="Описание...", width=300)
        self.entry_desc.pack(pady=5)

        # 3. Контейнер для Кнопки и Даты (горизонтальный)
        self.action_cont = ctk.CTkFrame(self, fg_color="transparent")
        self.action_cont.pack(pady=10)

        # Кнопка (изначально выключена)
        self.add_btn = ctk.CTkButton(
            self.action_cont, 
            text="Добавить", 
            width=120, 
            state="disabled", # Блокировка при старте
            fg_color="gray",
            command=self.handle_add
        )
        self.add_btn.pack(side="left", padx=10)

        # Метка текущего выбранного дедлайна
        self.date_info = ctk.CTkLabel(
            self.action_cont, 
            text="📅 Срок: --.--.--", 
            font=("Arial", 12, "bold"),
            text_color="#000"
        )
        self.date_info.pack(side="left", padx=5)

        # Запускаем фоновое обновление даты
        self.update_date_info()

    def validate_input(self):
        """Проверяет наличие текста и включает/выключает кнопку"""
        text = self.entry_title.get().strip()
        if len(text) > 0:
            # Кнопка активна и синяя
            self.add_btn.configure(state="normal", fg_color="#1F6AA5")
        else:
            # Кнопка серая и не нажимается
            self.add_btn.configure(state="disabled", fg_color="gray")

    def update_date_info(self):
        """Раз в 500мс опрашивает календарь и обновляет надпись"""
        try:
            current_date = self.calendar.get_date()
            self.date_info.configure(text=f"📅 Срок: {current_date}")
        except:
            pass
        
        # Рекурсивный вызов через 500 миллисекунд (0.5 сек)
        self.after(500, self.update_date_info)

    def handle_add(self):
        """Сбор данных и отправка в логику"""
        title = self.entry_title.get()
        desc = self.entry_desc.get()
        deadline = self.calendar.get_date()
        
        # Вызываем логику добавления
        self.on_add(title, desc, deadline)
        
        # Очистка полей и сброс кнопки
        self.entry_title.delete(0, 'end')
        self.entry_desc.delete(0, 'end')
        self.validate_input()