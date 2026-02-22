import customtkinter as ctk
from tkcalendar import Calendar

class CalendarFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        
        self.label = ctk.CTkLabel(self, text="📅 Календарь дедлайнов", font=("Arial", 16, "bold"))
        self.label.pack(pady=20)

        # Создаем календарь (он из чистого tkinter, поэтому цвета задаем вручную)
        self.cal = Calendar(self, selectmode='day', 
                            locale='ru_RU', 
                            background='#DEDEDE', 
                            foreground='#727272', 
                            headersbackground='#FFFFFF')
        self.cal.pack(pady=16, padx=16, fill="both", expand=True)

    def get_date(self):
        return self.cal.get_date()