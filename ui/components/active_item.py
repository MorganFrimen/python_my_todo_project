from ui.components.base.base_item import BaseTaskItem
import customtkinter as ctk

class ActiveTaskItem(BaseTaskItem):
    def __init__(self, master, task, index, on_done, on_delete, on_postpone):
        super().__init__(master, task)
        self.index = index
        self.on_done = on_done
        self.on_delete = on_delete
        self.on_postpone = on_postpone

        # Блокируем кнопки, если задача уже выполнена
        is_finished = task['status'] == "Выполнено"

        self.btn_cont = ctk.CTkFrame(self, fg_color="transparent")
        self.btn_cont.pack(side="right", padx=5)

        # 1. Кнопка ВЫПОЛНИТЬ
        self.ok_btn = ctk.CTkButton(
            self.btn_cont, text="OK", width=40, 
            fg_color="#2ECC71", state="normal" if not is_finished else "disabled",
            command=lambda: self.on_done(self.index)
        )
        self.ok_btn.pack(side="top", pady=2)

        # 2. Кнопка ПРОДЛИТЬ (Синяя)
        self.post_btn = ctk.CTkButton(
            self.btn_cont, text="📅", width=40, 
            fg_color="#3498DB", state="normal" if not is_finished else "disabled",
            command=lambda: self.on_postpone(self.index)
        )
        self.post_btn.pack(side="top", pady=2)

        # 3. Кнопка УДАЛИТЬ (Красная)
        ctk.CTkButton(
            self.btn_cont, text="🗑️", width=40, fg_color="#E74C3C",
            command=lambda: self.on_delete(self.index)
        ).pack(side="top", pady=2)