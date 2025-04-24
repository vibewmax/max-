import streamlit as st
import hashlib
import json
import os

# Налаштування сторінки
st.set_page_config(
    page_title="Система авторизації",
    page_icon="🔒",
    layout="centered"
)

# Вбудовані CSS стилі (без зовнішнього файлу)
def set_css():
    st.markdown("""
    <style>
        .stTextInput input, .stTextInput label, .stPassword input, .stPassword label {
            color: #4a4a4a;
        }
        .stButton>button {
            background-color: #4a8cff;
            color: white;
            border-radius: 5px;
            padding: 0.5rem 1rem;
            border: none;
        }
        .stButton>button:hover {
            background-color: #3a7bd5;
            color: white;
        }
        .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
            color: #4a8cff;
        }
        .stAlert {
            border-radius: 5px;
        }
    </style>
    """, unsafe_allow_html=True)

# Завантаження користувачів
def load_users():
    users_file = "users.json"
    if os.path.exists(users_file):
        with open(users_file, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}

# Збереження користувачів
def save_users(users):
    with open("users.json", "w") as f:
        json.dump(users, f)

# Хешування паролю
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Сторінка авторизації
def show_auth_page():
    st.title("🔐 Система авторизації")
    
    # Вибір між входом і реєстрацією
    tab1, tab2 = st.tabs(["Увійти", "Реєстрація"])
    
    with tab1:
        with st.form("login_form"):
            st.subheader("Вхід в систему")
            username = st.text_input("Логін", key="login_username")
            password = st.text_input("Пароль", type="password", key="login_password")
            
            submitted = st.form_submit_button("Увійти")
            if submitted:
                if not username or not password:
                    st.error("Будь ласка, заповніть всі поля")
                else:
                    hashed_password = hash_password(password)
                    users = load_users()
                    if username in users and users[username] == hashed_password:
                        st.session_state.authenticated = True
                        st.session_state.current_user = username
                        st.rerun()
                    else:
                        st.error("Невірний логін або пароль")
    
    with tab2:
        with st.form("register_form"):
            st.subheader("Реєстрація нового користувача")
            new_username = st.text_input("Логін", key="reg_username")
            new_password = st.text_input("Пароль", type="password", key="reg_password")
            confirm_password = st.text_input("Підтвердіть пароль", type="password", key="reg_confirm")
            
            submitted = st.form_submit_button("Зареєструватися")
            if submitted:
                if not new_username or not new_password:
                    st.error("Будь ласка, заповніть всі поля")
                elif new_password != confirm_password:
                    st.error("Паролі не співпадають")
                else:
                    users = load_users()
                    if new_username in users:
                        st.error("Користувач з таким іменем вже існує")
                    else:
                        hashed_password = hash_password(new_password)
                        users[new_username] = hashed_password
                        save_users(users)
                        st.success("Реєстрація пройшла успішно. Тепер ви можете увійти.")

# Сторінка проекту
def show_project_page():
    st.title("📚 Курсовий проект")
    
    # Інформація про проект
    st.markdown("""
    **Курсант:** НН4-23-203  
    **Курсовий проект на тему:**  
    "Розробка системи авторизації користувачів"
    
    Цей проект демонструє створення сучасної системи авторизації
    з використанням Python та Streamlit. Система включає:
    - Реєстрацію нового користувача
    - Вхід в систему
    - Зберігання даних у зашифрованому вигляді
    - Сучасний веб-інтерфейс
    
    Ви успішно авторизувалися в системі!
    """)
    
    # Кнопка виходу
    if st.button("Вийти з системи"):
        st.session_state.authenticated = False
        if 'current_user' in st.session_state:
            del st.session_state.current_user
        st.rerun()

# Головна функція
def main():
    # Встановлюємо CSS стилі
    set_css()
    
    # Ініціалізація стану сесії
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    
    # Вибір сторінки для відображення
    if st.session_state.authenticated:
        show_project_page()
    else:
        show_auth_page()

if __name__ == "__main__":
    main()
