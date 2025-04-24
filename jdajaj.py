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

# Стилізація
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

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

# Головна функція
def main():
    # Завантажуємо CSS
    local_css("style.css")
    
    # Ініціалізація стану сесії
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'users' not in st.session_state:
        st.session_state.users = load_users()
    
    # Якщо користувач авторизований - показуємо сторінку проекту
    if st.session_state.authenticated:
        show_project_page()
    else:
        # Інакше показуємо сторінку авторизації
        show_auth_page()

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
                    if username in st.session_state.users and st.session_state.users[username] == hashed_password:
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
                elif new_username in st.session_state.users:
                    st.error("Користувач з таким іменем вже існує")
                else:
                    hashed_password = hash_password(new_password)
                    st.session_state.users[new_username] = hashed_password
                    save_users(st.session_state.users)
                    st.success("Реєстрація пройшла успішно. Тепер ви можете увійти.")

# Сторінка проекту
def show_project_page():
    st.title("📚 Курсовий проект")
    
    # Інформація про проект
    st.markdown("""
    **Курсант:** НН4-23-203  
    **Курсовий проект на тему:**  
    "Розробка системи авторизації користувачів у GUI"
    
    Ви успішно авторизувалися в системі!
    """)
    
    # Кнопка виходу
    if st.button("Вийти з системи"):
        st.session_state.authenticated = False
        del st.session_state.current_user
        st.rerun()
    
    # Додаткова інформація
    st.markdown("---")
    st.markdown("### Додаткова інформація")
    st.markdown("""
    - Використані технології: Python, Streamlit, SHA-256
    - Дані зберігаються у файлі `users.json`
    - Паролі хешуються перед збереженням
    """)

if __name__ == "__main__":
    main()
