import streamlit as st

def run_add_user(authenticator):
    st.header("Ajouter un nouvel utilisateur")
    new_username = st.text_input("Nom d'utilisateur")
    new_email = st.text_input("Email")
    new_name = st.text_input("Nom complet")
    new_password = st.text_input("Mot de passe", type="password")
    new_role = st.selectbox("Rôle", options=["admin", "user"])
    add_user_button = st.button("Ajouter")

    if add_user_button:
        success = authenticator.db.add_user(new_username, new_email, new_name, new_password, new_role)
        if success:
            st.success(f"L'utilisateur {new_username} a été ajouté avec succès.")
        else:
            st.error("Le nom d'utilisateur existe déjà.")