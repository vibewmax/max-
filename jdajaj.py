import streamlit as st
import json
import os

USER_DB = "users.json"

def load_users():
    if not os.path.exists(USER_DB):
        return {}
    with open(USER_DB, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USER_DB, "w") as f:
        json.dump(users, f)

def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed.encode())

def register_user(username, password):
    users = load_users()
    if username in users:
        return False, "Користувач вже існує!"
    users[username] = hash_password(password)
    save_users(users)
    return True, "Реєстрація успішна!"

def login_user(username, password):
    users = load_users()
    if username not in users:
        return False, "Користувача не знайдено."
    if verify_password(password, users[username]):
        return True, "Вхід успішний!"
    else:
        return False, "Невірний пароль."

def main():
    st.title("🔐 Авторизація користувача")

    menu = ["Вхід", "Реєстрація"]
    choice = st.sidebar.selectbox("Меню", menu)

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.username = ""

    if choice == "Вхід":
        st.subheader("Вхід")

        username = st.text_input("Ім'я користувача")
        password = st.text_input("Пароль", type="password")

        if st.button("Увійти"):
            success, message = login_user(username, password)
            st.info(message)
            if success:
                st.session_state.logged_in = True
                st.session_state.username = username

    elif choice == "Реєстрація":
        st.subheader("Створити обліковий запис")

        new_user = st.text_input("Ім'я користувача")
        new_password = st.text_input("Пароль", type="password")

        if st.button("Зареєструватися"):
            success, message = register_user(new_user, new_password)
            st.info(message)

    if st.session_state.logged_in:
        st.success(f"👋 Вітаю, {st.session_state.username}!")
        if st.button("Вийти"):
            st.session_state.logged_in = False
            st.session_state.username = ""

if __name__ == "__main__":
    main()
