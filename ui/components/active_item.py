from ui.components.base.base_item import BaseTaskItem
import customtkinter as ctk

class ActiveTaskItem(BaseTaskItem):
    def __init__(self, master, task, index, on_done, on_delete):
        super().__init__(master, task)

         # Добавляем специфику: кнопки справа
        self.btn_cont = ctk.CTkFrame(self, fg_color="transparent")
        self.btn_cont.pack(side="right", padx=5)

        self.ok_btn = ctk.CTkButton(
            self.btn_cont, 
            text="OK", 
            width=40, 
            fg_color="#2ECC71" if not self.is_done else "gray",
            state="normal" if not self.is_done else "disabled", # Блокировка!
            command=lambda: on_done(index)
        )
        ctk.CTkButton(
            self.btn_cont, 
            text="🗑️", 
            width=40, 
            fg_color="#E74C3C",
            command=lambda: on_delete(index)
        ).pack(side="top", pady=2)
        
        # Добавляем дедлайн (тоже специфика активных)
        deadline_text = f"⏰ Срок: {task.get('deadline', '-')}"
        ctk.CTkLabel(
            self.text_cont, 
            text=deadline_text, 
            font=("Arial", 10, "italic"), 
            text_color="gray" if self.is_done else "#FFCC00", 
            anchor="w"
        ).pack()