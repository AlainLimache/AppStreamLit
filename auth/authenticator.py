import streamlit as st
import streamlit_authenticator as stauth
from .database import UserDatabase
import random
import string

class Authenticator:
    key = 'unique_key'
    cookie_name = 'some_cookie_name'
    def __init__(self):
        self.db = UserDatabase()
        self.db.create_connection()
        self.authenticator = stauth.Authenticate(
            self.db.get_credentials(),
            cookie_name=self.cookie_name,
            key=self.key,
            cookie_expiry_days=30,
        )

        self.username = None
        self.name = None
        self.authentication_status = None

    def login(self):
        self.name, self.authentication_status, self.username = self.authenticator.login(
            "Se connecter", "main"
        )
        if self.authentication_status:
            self.username = self.username
        return self.name, self.authentication_status, self.username

    def logout(self):
        self.authenticator.logout("Déconnexion", "sidebar", key=self.key)
        self.username = None
        self.name = None
        self.authentication_status = None

    def register_user(self):
        try:
            if self.authenticator.register_user('Register user', preauthorization=False):
                st.success('User registered successfully')
        except Exception as e:
            st.error(e)

    def get_role(self, username):
        role = self.db.get_role(username)
        return role
