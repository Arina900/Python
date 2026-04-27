import tkinter as tk
import json
from tkinter import messagebox
import os

window = tk.Tk()
window.title("Movie Library - Личная кинотека")
window.geometry("600x700")

title_label = tk.Label(window, text="Название фильма:").pack()
title_entry = tk.Entry(window, width=40)
title_entry.pack()


def load_movies():
    try:
        if os.path.exists("movies.json"):
            with open("movies.json", "r", encoding="utf-8") as f:
                return json.load(f)
        return []
    except (json.JSONDecodeError, IOError) as e:
        messagebox.showerror("Ошибка", f"Не удалось загрузить данные: {e}")
        return []


def save_movies():
    try:
        with open("movies.json", "w", encoding="utf-8") as f:
            json.dump(movies, f, ensure_ascii=False, indent=2)
        return True
    except IOError as e:
        messagebox.showerror("Ошибка", f"Не удалось сохранить данные: {e}")
        return False


movies = load_movies()


def update_list():
    listbox.delete(0, tk.END)
    genre_filter = filter_genre_entry.get().lower()
    year_filter = filter_year_entry.get()

    filtered_movies = []
    for m in movies:
        if genre_filter and genre_filter not in m["Жанр"].lower():
            continue
        if year_filter:
            if year_filter == ">2000" and int(m["Год"]) <= 2000:
                continue
            if year_filter == "<2000" and int(m["Год"]) >= 2000:
                continue
            if year_filter == "2000-2020" and (int(m["Год"]) < 2000 or int(m["Год"]) > 2020):
                continue
        filtered_movies.append(m)
        listbox.insert(tk.END, f"{m['Название']} - {m['Жанр']} ({m['Год']}) - Рейтинг: {m['Рейтинг']}")

    counter_label.config(text=f"Показано: {len(filtered_movies)} / Всего: {len(movies)}")


def on_genre_filter_change(event):
    update_list()


def on_year_filter_change(value):
    update_list()


def add_movie():
    title = title_entry.get()
    genre = genre_entry.get()
    year = year_entry.get()
    rating = rating_entry.get()

    if not title or not genre or not year or not rating:
        messagebox.showwarning("Ошибка", "Заполните все поля!")
        return

    if not year.isdigit():
        messagebox.showwarning("Ошибка", "Год должен быть числом!")
        return

    try:
        rating_val = float(rating)
        if rating_val < 0 or rating_val > 10:
            messagebox.showwarning("Ошибка", "Рейтинг должен быть от 0 до 10!")
            return
    except ValueError:
        messagebox.showwarning("Ошибка", "Рейтинг должен быть числом!")
        return

    movies.append({"Название": title, "Жанр": genre, "Год": year, "Рейтинг": rating})
    save_movies()
    update_list()

    title_entry.delete(0, tk.END)
    genre_entry.delete(0, tk.END)
    year_entry.delete(0, tk.END)
    rating_entry.delete(0, tk.END)


def delete_movie():
    if not listbox.curselection():
        messagebox.showwarning("Ошибка", "Выберите фильм для удаления!")
        return
    selected = listbox.get(listbox.curselection()[0])
    for i, m in enumerate(movies):
        if f"{m['Название']} - {m['Жанр']} ({m['Год']}) - Рейтинг: {m['Рейтинг']}" == selected:
            del movies[i]
            break
    save_movies()
    update_list()


def clear_filters():
    filter_genre_entry.delete(0, tk.END)
    filter_year_var.set("Все годы")
    update_list()


tk.Label(window, text="Жанр:").pack()
genre_entry = tk.Entry(window, width=40)
genre_entry.pack()

tk.Label(window, text="Год выпуска:").pack()
year_entry = tk.Entry(window, width=40)
year_entry.pack()

tk.Label(window, text="Рейтинг (0-10):").pack()
rating_entry = tk.Entry(window, width=40)
rating_entry.pack()

tk.Button(window, text="Добавить фильм", bg="green", command=add_movie, fg="white").pack(pady=5)
tk.Button(window, text="Удалить фильм", bg="red", command=delete_movie, fg="white").pack(pady=5)

listbox = tk.Listbox(window, width=75, height=12)
listbox.pack(pady=10)

tk.Label(window, text="--- ФИЛЬТРАЦИЯ ---").pack(pady=5)
tk.Label(window, text="Фильтр по жанру:").pack()
filter_genre_entry = tk.Entry(window, width=30)
filter_genre_entry.pack()
filter_genre_entry.bind("<KeyRelease>", on_genre_filter_change)

tk.Label(window, text="Фильтр по году:").pack()
filter_year_var = tk.StringVar(value="Все годы")
filter_year = tk.OptionMenu(window, filter_year_var, "Все годы", ">2000", "<2000", "2000-2020",
                            command=on_year_filter_change)
filter_year.pack()

tk.Button(window, text="Сбросить фильтры", bg="orange", command=clear_filters, fg="white").pack(pady=5)

counter_label = tk.Label(window, text="Показано: 0 / Всего: 0", font=("Arial", 10, "bold"), fg="blue")
counter_label.pack(pady=5)

update_list()
window.mainloop()