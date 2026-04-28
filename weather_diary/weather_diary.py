import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

DATA_FILE = "weather_data.json"

class WeatherDiary:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather Diary - Дневник погоды")
        self.root.geometry("700x500")

        # Данные
        self.entries = self.load_data()

        # Поля ввода
        self.create_input_frame()

        # Таблица для отображения
        self.create_treeview()

        # Кнопки управления
        self.create_buttons()

        # Фильтры
        self.create_filter_frame()

        self.refresh_table()

    # ------------------ Ввод данных ------------------
    def create_input_frame(self):
        frame = tk.LabelFrame(self.root, text="Добавить запись", padx=10, pady=10)
        frame.pack(fill="x", padx=10, pady=5)

        tk.Label(frame, text="Дата (ГГГГ-ММ-ДД):").grid(row=0, column=0, sticky="e")
        self.date_entry = tk.Entry(frame, width=15)
        self.date_entry.grid(row=0, column=1, padx=5, pady=2)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))

        tk.Label(frame, text="Температура (°C):").grid(row=0, column=2, sticky="e")
        self.temp_entry = tk.Entry(frame, width=10)
        self.temp_entry.grid(row=0, column=3, padx=5, pady=2)

        tk.Label(frame, text="Описание:").grid(row=1, column=0, sticky="e")
        self.desc_entry = tk.Entry(frame, width=30)
        self.desc_entry.grid(row=1, column=1, columnspan=3, padx=5, pady=2, sticky="ew")

        self.precip_var = tk.BooleanVar()
        self.precip_check = tk.Checkbutton(frame, text="Осадки", variable=self.precip_var)
        self.precip_check.grid(row=1, column=4, padx=10)

    # ------------------ Таблица ------------------
    def create_treeview(self):
        self.tree = ttk.Treeview(self.root, columns=("date", "temp", "desc", "precip"), show="headings")
        self.tree.heading("date", text="Дата")
        self.tree.heading("temp", text="Температура (°C)")
        self.tree.heading("desc", text="Описание")
        self.tree.heading("precip", text="Осадки")
        self.tree.column("date", width=100)
        self.tree.column("temp", width=100)
        self.tree.column("desc", width=300)
        self.tree.column("precip", width=80)
        self.tree.pack(fill="both", expand=True, padx=10, pady=5)

    # ------------------ Кнопки ------------------
    def create_buttons(self):
        frame = tk.Frame(self.root)
        frame.pack(fill="x", padx=10, pady=5)

        tk.Button(frame, text="➕ Добавить запись", command=self.add_entry).pack(side="left", padx=5)
        tk.Button(frame, text="💾 Сохранить в JSON", command=self.save_to_file).pack(side="left", padx=5)
        tk.Button(frame, text="📂 Загрузить из JSON", command=self.load_from_file).pack(side="left", padx=5)
        tk.Button(frame, text="❌ Очистить фильтры", command=self.clear_filters).pack(side="left", padx=5)

    # ------------------ Фильтры ------------------
    def create_filter_frame(self):
        frame = tk.LabelFrame(self.root, text="Фильтрация", padx=10, pady=10)
        frame.pack(fill="x", padx=10, pady=5)

        # Фильтр по дате
        tk.Label(frame, text="Фильтр по дате (ГГГГ-ММ-ДД):").grid(row=0, column=0, sticky="e")
        self.filter_date_entry = tk.Entry(frame, width=15)
        self.filter_date_entry.grid(row=0, column=1, padx=5)

        # Фильтр по температуре
        tk.Label(frame, text="Температура выше (°C):").grid(row=0, column=2, sticky="e")
        self.filter_temp_entry = tk.Entry(frame, width=10)
        self.filter_temp_entry.grid(row=0, column=3, padx=5)

        tk.Button(frame, text="🔍 Применить фильтры", command=self.apply_filters).grid(row=0, column=4, padx=10)

    # ------------------ Основная логика ------------------
    def add_entry(self):
        date = self.date_entry.get().strip()
        temp_str = self.temp_entry.get().strip()
        desc = self.desc_entry.get().strip()
        precip = self.precip_var.get()

        # Валидация
        if not desc:
            messagebox.showerror("Ошибка", "Описание погоды не может быть пустым")
            return

        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Ошибка", "Неверный формат даты. Используйте ГГГГ-ММ-ДД")
            return

        try:
            temp = float(temp_str)
        except ValueError:
            messagebox.showerror("Ошибка", "Температура должна быть числом")
            return

        self.entries.append({
            "date": date,
            "temperature": temp,
            "description": desc,
            "precipitation": precip
        })

        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.temp_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)
        self.precip_var.set(False)

        self.refresh_table()

    def refresh_table(self, filtered_entries=None):
        for row in self.tree.get_children():
            self.tree.delete(row)

        data = filtered_entries if filtered_entries is not None else self.entries
        for e in data:
            precip_str = "Да" if e["precipitation"] else "Нет"
            self.tree.insert("", "end", values=(e["date"], e["temperature"], e["description"], precip_str))

    def apply_filters(self):
        filter_date = self.filter_date_entry.get().strip()
        filter_temp_str = self.filter_temp_entry.get().strip()

        filtered = self.entries[:]

        if filter_date:
            filtered = [e for e in filtered if e["date"] == filter_date]

        if filter_temp_str:
            try:
                temp_threshold = float(filter_temp_str)
                filtered = [e for e in filtered if e["temperature"] > temp_threshold]
            except ValueError:
                messagebox.showerror("Ошибка", "Температура для фильтра должна быть числом")
                return

        self.refresh_table(filtered)

    def clear_filters(self):
        self.filter_date_entry.delete(0, tk.END)
        self.filter_temp_entry.delete(0, tk.END)
        self.refresh_table()

    # ------------------ Работа с JSON ------------------
    def load_data(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                return []
        return []

    def save_to_file(self):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(self.entries, f, ensure_ascii=False, indent=4)
        messagebox.showinfo("Успех", f"Сохранено {len(self.entries)} записей в {DATA_FILE}")

    def load_from_file(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    self.entries = json.load(f)
                self.clear_filters()
                messagebox.showinfo("Успех", "Данные загружены из файла")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить: {e}")
        else:
            messagebox.showwarning("Нет файла", "Файл с данными не найден")

# ------------------ Запуск ------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherDiary(root)
    root.mainloop()