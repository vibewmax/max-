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

# Вбудовані CSS стилі
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

# Функція для завантаження користувачів з безпечною обробкою помилок
def load_users():
    try:
        if os.path.exists("users.json"):
            with open("users.json", "r") as f:
                return json.load(f)
        return {}
    except Exception:
        return {}

# Функція для збереження користувачів з безпечною обробкою помилок
def save_users(users):
    try:
        with open("users.json", "w") as f:
            json.dump(users, f)
        return True
    except Exception:
        return False

# Хешування паролю
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Сторінка авторизації
def show_auth_page():
    st.title("🔐 Система авторизації")
    
    tab1, tab2 = st.tabs(["Увійти", "Реєстрація"])
    
    with tab1:
        with st.form("login_form"):
            st.subheader("Вхід в систему")
            username = st.text_input("Логін", key="login_username")
            password = st.text_input("Пароль", type="password", key="login_password")
            
            if st.form_submit_button("Увійти"):
                if not username or not password:
                    st.error("Будь ласка, заповніть всі поля")
                else:
                    users = load_users()
                    if username in users and users[username] == hash_password(password):
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
            
            if st.form_submit_button("Зареєструватися"):
                if not new_username or not new_password:
                    st.error("Будь ласка, заповніть всі поля")
                elif new_password != confirm_password:
                    st.error("Паролі не співпадають")
                else:
                    users = load_users()
                    if new_username in users:
                        st.error("Користувач з таким іменем вже існує")
                    else:
                        users[new_username] = hash_password(new_password)
                        if save_users(users):
                            st.success("Реєстрація пройшла успішно. Тепер ви можете увійти.")
                        else:
                            st.error("Помилка збереження даних")

# Сторінка проекту
def show_project_page():
    st.title("📚 Курсовий проект")
    
    st.markdown(f"""
    **Курсант:** НН4-23-203  
    **Користувач:** {st.session_state.current_user}
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
    
    if st.button("Вийти з системи"):
        st.session_state.authenticated = False
        st.session_state.current_user = None
        st.rerun()

# Головна функція
def main():
    # Ініціалізація стану сесії
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'current_user' not in st.session_state:
        st.session_state.current_user = None
    
    # Вибір сторінки для відображення
    if st.session_state.authenticated:
        show_project_page()
    else:
        show_auth_page()

if __name__ == "__main__":
    main()
