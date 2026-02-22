import customtkinter as ctk
from datetime import datetime

class TaskItem(ctk.CTkFrame):
    def __init__(self, master, task, index, on_done, on_delete):
        super().__init__(master)
        
        # 1. Объявляем переменные данных
        self.task = task
        self.index = index
        self.on_done = on_done
        self.on_delete = on_delete
        
        # Получаем дедлайн (если его нет в словаре, ставим прочерк)
        self.deadline_str = self.task.get('deadline', 'Не указан')
        
        # Определяем цвет дедлайна (вызываем внутренний метод)
        self.d_color = self.get_deadline_color()

        # 2. Создаем контейнер для текста (теперь он виден внутри __init__)
        self.text_cont = ctk.CTkFrame(self, fg_color="transparent")
        self.text_cont.pack(side="left", padx=10, fill="both", expand=True)

        # 3. Отрисовка элементов интерфейса
        self.create_widgets()

    def get_deadline_color(self):
        """Метод для расчета цвета текста дедлайна"""
        default_color = "#000283" # Золотистый
        error_color = "#E74C3C"   # Красный (просрочено)

        if self.task['status'] == "Выполнено" or self.deadline_str == 'Не указан':
            return "#2ECC71" # Зеленый, если уже готово

        try:
            # Превращаем строку из календаря в объект даты
            # ВАЖНО: формат %m/%d/%y должен совпадать с тем, что дает tkcalendar
            today = datetime.now().date()
            d_date = datetime.strptime(self.deadline_str, "%d.%m.%Y").date()
            
            if d_date < today:
                return error_color
        except Exception as e:
            # Если формат даты не подошел, просто оставляем желтый
            print(f"Ошибка парсинга даты: {e}")
            
        return default_color

    def create_widgets(self):
        """Метод для создания всех надписей и кнопок внутри карточки"""
        # Название
        status_icon = "✅" if self.task['status'] == "Выполнено" else "⏳"
        title_lbl = ctk.CTkLabel(self.text_cont, 
                                 text=f"{status_icon} {self.task['title']}", 
                                 font=("Arial", 14, "bold"), 
                                 anchor="w")
        title_lbl.pack(fill="x")

        # Описание
        desc_lbl = ctk.CTkLabel(self.text_cont, 
                                text=self.task['description'], 
                                font=("Arial", 12), 
                                text_color="gray", 
                                anchor="w")
        desc_lbl.pack(fill="x")

        # ДАТА ДЕДЛАЙНА (используем self.deadline_str и self.d_color)
        deadline_lbl = ctk.CTkLabel(self.text_cont, 
                                    text=f"⏰ Срок: {self.deadline_str}", 
                                    font=("Arial", 11, "italic"), 
                                    text_color=self.d_color, 
                                    anchor="w")
        deadline_lbl.pack(fill="x")

        # Кнопки (справа)
        btn_cont = ctk.CTkFrame(self, fg_color="transparent")
        btn_cont.pack(side="right", padx=5)
        
        ok_btn = ctk.CTkButton(btn_cont, text="OK", width=40, 
                               command=lambda: self.on_done(self.index))
        ok_btn.pack(side="top", pady=2)
        
        del_btn = ctk.CTkButton(btn_cont, text="🗑️", width=40, 
                                fg_color="#E74C3C", 
                                command=lambda: self.on_delete(self.index))
        del_btn.pack(side="top", pady=2)