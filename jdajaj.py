import streamlit as st
import hashlib
import json
import os

USER_DB = "users.json"

# Завантаження користувачів
def load_users():
    if not os.path.exists(USER_DB):
        return {}
    with open(USER_DB, "r") as f:
        return json.load(f)

# Збереження користувачів
def save_users(users):
    with open(USER_DB, "w") as f:
        json.dump(users, f)

# Хешування паролю
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Реєстрація
def register_user(username, password):
    users = load_users()
    if username in users:
        return False, "Користувач вже існує!"
    users[username] = hash_password(password)
    save_users(users)
    return True, "Реєстрація успішна!"

# Вхід
def login_user(username, password):
    users = load_users()
    if username not in users:
        return False, "Користувача не знайдено."
    if users[username] == hash_password(password):
        return True, "Вхід успішний!"
    else:
        return False, "Невірний пароль."

# Головна функція
def main():
    st.set_page_config(page_title="Авторизація", page_icon="🔐")
    st.title("🔐 Авторизація користувача")

    menu = ["Вхід", "Реєстрація"]
    choice = st.sidebar.selectbox("Меню", menu)

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.username = ""

    if choice == "Вхід":
        st.subheader("Увійти")
        username = st.text_input("Ім'я користувача")
        password = st.text_input("Пароль", type="password")
        if st.button("Увійти"):
            success, msg = login_user(username, password)
            st.info(msg)
            if success:
                st.session_state.logged_in = True
                st.session_state.username = username

    elif choice == "Реєстрація":
        st.subheader("Реєстрація")
        new_user = st.text_input("Нове ім'я користувача")
        new_password = st.text_input("Новий пароль", type="password")
        if st.button("Зареєструватися"):
            success, msg = register_user(new_user, new_password)
            st.info(msg)

    if st.session_state.logged_in:
        st.success(f"👋 Вітаю, {st.session_state.username}!")
        if st.button("Вийти"):
            st.session_state.logged_in = False
            st.session_state.username = ""

# Запуск
if __name__ == "__main__":
    main()
