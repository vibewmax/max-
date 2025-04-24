import tkinter as tk
from tkinter import messagebox, ttk
import hashlib
import json
import os
from tkinter import font as tkfont

class AuthSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Система авторизації")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f2f5")
        self.root.resizable(False, False)
        
        # Стилі
        self.style = ttk.Style()
        self.style.configure("TFrame", background="#f0f2f5")
        self.style.configure("TLabel", background="#f0f2f5", font=("Arial", 10))
        self.style.configure("TButton", font=("Arial", 10), padding=6)
        self.style.map("TButton",
                      foreground=[('pressed', 'white'), ('active', 'white')],
                      background=[('pressed', '#3a7bd5'), ('active', '#3a7bd5')])
        
        # Кольори
        self.primary_color = "#3a7bd5"
        self.secondary_color = "#00d2ff"
        self.success_color = "#4BB543"
        self.error_color = "#ff3333"
        
        # Шрифти
        self.title_font = tkfont.Font(family="Arial", size=24, weight="bold")
        self.subtitle_font = tkfont.Font(family="Arial", size=14)
        self.normal_font = tkfont.Font(family="Arial", size=12)
        
        # База даних користувачів
        self.users_file = "users.json"
        self.users = self.load_users()
        
        # Змінні для зберігання введених даних
        self.username = tk.StringVar()
        self.password = tk.StringVar()
        
        # Створення елементів GUI
        self.create_login_widgets()
    
    def load_users(self):
        """Завантаження користувачів з файлу"""
        if os.path.exists(self.users_file):
            with open(self.users_file, "r") as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    return {}
        return {}
    
    def save_users(self):
        """Збереження користувачів у файл"""
        with open(self.users_file, "w") as f:
            json.dump(self.users, f)
    
    def hash_password(self, password):
        """Хешування паролю за допомогою SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def create_login_widgets(self):
        """Створення елементів інтерфейсу для входу"""
        # Очистити вікно
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Верхній бар
        header = tk.Frame(self.root, bg=self.primary_color, height=80)
        header.pack(fill="x")
        
        # Текстове лого
        logo_label = tk.Label(header, text="Auth System", font=self.title_font, 
                             fg="white", bg=self.primary_color)
        logo_label.pack(pady=20)
        
        # Основний фрейм
        main_frame = ttk.Frame(self.root)
        main_frame.pack(pady=20, padx=40, fill="both", expand=True)
        
        # Заголовок
        title_label = tk.Label(main_frame, text="Вхід в систему", font=self.title_font, 
                             fg=self.primary_color, bg="#f0f2f5")
        title_label.pack(pady=(0, 20))
        
        # Форма входу
        form_frame = ttk.Frame(main_frame)
        form_frame.pack(pady=10)
        
        # Поле логіна
        tk.Label(form_frame, text="Логін:", font=self.normal_font).grid(row=0, column=0, pady=5, sticky="e")
        username_entry = ttk.Entry(form_frame, textvariable=self.username, font=self.normal_font, width=30)
        username_entry.grid(row=0, column=1, pady=5, padx=10)
        
        # Поле паролю
        tk.Label(form_frame, text="Пароль:", font=self.normal_font).grid(row=1, column=0, pady=5, sticky="e")
        password_entry = ttk.Entry(form_frame, textvariable=self.password, show="*", font=self.normal_font, width=30)
        password_entry.grid(row=1, column=1, pady=5, padx=10)
        
        # Кнопки
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=20)
        
        login_btn = ttk.Button(button_frame, text="Увійти", command=self.login, style="TButton")
        login_btn.pack(side="left", padx=10)
        
        register_btn = ttk.Button(button_frame, text="Реєстрація", command=self.register)
        register_btn.pack(side="left", padx=10)
        
        # Фокус на першому полі
        username_entry.focus_set()
    
    def create_project_page(self):
        """Створення сторінки курсового проекту"""
        # Очистити вікно
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Змінити розмір вікна
        self.root.geometry("900x700")
        
        # Верхній бар
        header = tk.Frame(self.root, bg=self.primary_color, height=80)
        header.pack(fill="x")
        
        # Текстове лого
        logo_label = tk.Label(header, text="Курсовий проект", font=self.title_font, 
                            fg="white", bg=self.primary_color)
        logo_label.pack(pady=20)
        
        # Основний фрейм
        main_frame = ttk.Frame(self.root)
        main_frame.pack(pady=40, padx=60, fill="both", expand=True)
        
        # Заголовок
        title_label = tk.Label(main_frame, text="Курсовий проект", font=self.title_font, 
                             fg=self.primary_color, bg="#f0f2f5")
        title_label.pack(pady=(0, 30))
        
        # Картка з інформацією
        card_frame = ttk.Frame(main_frame, style="TFrame")
        card_frame.pack(pady=20, padx=40, fill="both", expand=True)
        
        # Інформація про проект
        project_info = """
        Курсант: НН4-23-203
        Курсовий проект на тему:
        "Розробка системи авторизації користувачів у GUI"
        
        Цей проект демонструє створення сучасної системи авторизації
        з використанням Python та бібліотеки Tkinter. Система включає:
        - Реєстрацію нового користувача
        - Вхід в систему
        - Зберігання даних у зашифрованому вигляді
        - Сучасний інтерфейс
        
        Ви успішно авторизувалися в системі!
        """
        
        info_label = tk.Label(card_frame, text=project_info, font=self.subtitle_font, 
                            justify="left", bg="white", bd=2, relief="groove", padx=20, pady=20)
        info_label.pack(fill="both", expand=True)
        
        # Кнопка виходу (повернення до авторизації)
        logout_frame = ttk.Frame(main_frame)
        logout_frame.pack(pady=20)
        
        logout_btn = ttk.Button(logout_frame, text="Вийти з системи", 
                               command=self.create_login_widgets,
                               style="TButton")
        logout_btn.pack()
    
    def login(self):
        """Обробка входу користувача"""
        username = self.username.get()
        password = self.password.get()
        
        if not username or not password:
            messagebox.showerror("Помилка", "Будь ласка, заповніть всі поля", parent=self.root)
            return
        
        hashed_password = self.hash_password(password)
        
        if username in self.users and self.users[username] == hashed_password:
            messagebox.showinfo("Успіх", f"Вітаємо, {username}!\nВи успішно увійшли.", parent=self.root)
            self.create_project_page()  # Перехід на сторінку проекту
        else:
            messagebox.showerror("Помилка", "Невірний логін або пароль", parent=self.root)
    
    def register(self):
        """Обробка реєстрації нового користувача"""
        username = self.username.get()
        password = self.password.get()
        
        if not username or not password:
            messagebox.showerror("Помилка", "Будь ласка, заповніть всі поля", parent=self.root)
            return
        
        if username in self.users:
            messagebox.showerror("Помилка", "Користувач з таким іменем вже існує", parent=self.root)
            return
        
        hashed_password = self.hash_password(password)
        self.users[username] = hashed_password
        self.save_users()
        
        messagebox.showinfo("Успіх", "Реєстрація пройшла успішно.\nТепер ви можете увійти.", parent=self.root)

if __name__ == "__main__":
    root = tk.Tk()
    app = AuthSystem(root)
    root.mainloop()