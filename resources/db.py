from tkinter import Tk, Label, Button, messagebox
from tkinter.ttk import Entry


class RecordField(Tk):
    def __init__(self, time: int, hearts: int, func):
        super().__init__()
        self.title("Добавление результата в базу данных")
        self.geometry('400x300')
        self.resizable(False, False)
        self.time, self.hearts = time, hearts
        self.stylesheet = {'label-font': 'PT_Sans_Bold 12 bold', 'entry-font': 'PT_Sans_Bold 16',
                           'pre-white': '#ededed', 'pre-black': '#121212', 'purple': '#c000c0'}
        self['bg'] = self.stylesheet['pre-black']
        self.widgets_init()
        self.new_record = func

    def widgets_init(self):
        # ssd - Style Sheet Dict
        ssd = self.stylesheet
        Label(self, text="Поздравляем с победой! Введите ваше имя\n"
                         "для занесения вашего результата\n в таблицу рекордов:",
              bg=ssd['pre-black'], fg=ssd['pre-white'], font=ssd['label-font']).pack(pady=5)
        self.entry = Entry(self, font=ssd['entry-font'], width=28)
        self.entry.pack(pady=5)
        self.button_yes = Button(self, text="Подтвердить", border=0, width=34, height=2, font=ssd['label-font'],
                                 command=self.entry_check, activebackground=ssd['purple'])
        self.button_yes.pack(pady=1)
        Label(self, text=f"Вы сломали все блоки за {self.time} миллисекунд",
              bg=ssd['pre-black'], fg=ssd['pre-white'], font=ssd['label-font']).pack(pady=5)
        Label(self, text=f"Оставшееся количетво жизней: {self.hearts}",
              bg=ssd['pre-black'], fg=ssd['pre-white'], font=ssd['label-font']).pack()
        self.button_no = Button(self, text="Не добавлять результат в базу данных", border=0, width=34, height=2,
                                font=ssd['label-font'], command=self.destroy, activebackground=ssd['purple'])
        self.button_no.pack(pady=5)

    def entry_check(self):
        self.name = self.entry.get()
        if self.name:
            self.destroy()
            self.new_record(self.name)
        else:
            messagebox.showerror("Ошибка", "Вы не ввели свое имя.\nВведите ваше имя.")
