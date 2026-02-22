import customtkinter as ctk

class InputFrame(ctk.CTkFrame):
    def __init__(self, master, on_add, calendar_component):
        super().__init__(master, fg_color="transparent")
        
        # Сохраняем ссылки на функцию и календарь в самом объекте
        self.on_add = on_add
        self.calendar = calendar_component

        self.entry_title = ctk.CTkEntry(self, placeholder_text="Название задачи...", width=300)
        self.entry_title.pack(pady=5)
        
        self.entry_desc = ctk.CTkEntry(self, placeholder_text="Описание...", width=300)
        self.entry_desc.pack(pady=5)
        
        # Исправляем команду: убираем передачу аргумента здесь, так как вызовем его внутри
        self.add_btn = ctk.CTkButton(self, text="Добавить задачу", command=self.handle_add)
        self.add_btn.pack(pady=10)

    def handle_add(self):
        # Теперь метод берет всё из self
        title = self.entry_title.get()
        desc = self.entry_desc.get()
        deadline = self.calendar.get_date() # Забираем дату из календаря
        
        if title:
            # Вызываем функцию, которую передали при создании
            self.on_add(title, desc, deadline)
            
            # Очищаем поля
            self.entry_title.delete(0, 'end')
            self.entry_desc.delete(0, 'end')